"""Centralized Azure client factory with Managed Identity support.

Este módulo provee:
- Una clase `Clients` que construye clientes para Azure OpenAI (chat/completions,
  embeddings), Azure Document Intelligence, Azure AI Search, Azure Blob Storage
  y el recurso dedicado de Deep Research (o3-deep-research).
- Funciones de conveniencia (`get_azure_client`, `get_deployment_name`,
  `chat_completion`) que mantienen la interfaz simple usada por los agentes
  del pipeline KYC + Credit Risk Intelligence (perfiles "gpt52" / "gpt41").

Autenticación SIN API keys, vía azure-identity:
- Entorno local      -> DefaultAzureCredential (AZ CLI / VS Code), Managed Identity excluida.
- Entorno Azure host -> ManagedIdentityCredential (user-assigned si hay client_id).
"""

from __future__ import annotations

import base64
import json
import logging
import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.identity import (
    DefaultAzureCredential,
    ManagedIdentityCredential,
    get_bearer_token_provider,
)
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    from services.AiSearch import get_ai_search  # type: ignore
except Exception:
    get_ai_search = None

try:
    from services.BlobStorage import get_blob_storage  # type: ignore
except Exception:
    get_blob_storage = None

logger = logging.getLogger(__name__)

# Ensure auth logs from this module are visible even when app-level logging
# is not configured for INFO.
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.disabled = False
logger.propagate = False
logger.info("[AUTH] clients logger initialized")

# User-assigned managed identity client id.
# If AZURE_CLIENT_ID is not present in runtime env, this value will be used.
MANAGED_IDENTITY_CLIENT_ID = os.getenv("MANAGED_IDENTITY_CLIENT_ID", "").strip()


@dataclass
class ClientsConfig:
    """Centralized configuration that mirrors the current .env variables."""

    # OpenAI (gpt-4.1)
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = ""
    azure_openai_api_version: str = ""

    # Document Intelligence
    azure_docint_endpoint: str = ""

    # AI Search
    azure_search_endpoint: str = ""
    azure_search_index_name: str = ""

    # Embeddings
    azure_openai_embedding_endpoint: str = ""
    azure_openai_embedding_deployment: str = ""
    azure_openai_embedding_api_version: str = ""

    # GPT-5.2
    azure_openai_gpt52_endpoint: str = ""
    azure_openai_gpt52_deployment: str = ""
    azure_openai_gpt52_api_version: str = ""

    # Deep Research (recurso dedicado)
    azure_openai_o3dr_endpoint: str = ""
    azure_openai_o3dr_deployment: str = ""
    azure_openai_o3dr_api_version: str = ""

    # User-assigned managed identity
    azure_client_id: str = ""

    # Optional blob
    azure_storage_blob_account_url: str = ""
    azure_openai_timeout_s: float = 60.0

    @classmethod
    def from_env(cls) -> "ClientsConfig":
        """Load runtime config from environment variables."""
        return cls(
            azure_openai_endpoint=(os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip(),
            azure_openai_deployment=(os.getenv("AZURE_OPENAI_DEPLOYMENT") or "").strip(),
            azure_openai_api_version=(os.getenv("AZURE_OPENAI_API_VERSION") or "").strip(),
            azure_docint_endpoint=(os.getenv("AZURE_DOCINT_ENDPOINT") or "").strip().strip("'\""),
            azure_search_endpoint=(os.getenv("AZURE_SEARCH_ENDPOINT") or "").strip(),
            azure_search_index_name=(os.getenv("AZURE_SEARCH_INDEX_NAME") or "").strip(),
            azure_openai_embedding_endpoint=(os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT") or "").strip(),
            azure_openai_embedding_deployment=(os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or "").strip(),
            azure_openai_embedding_api_version=(os.getenv("AZURE_OPENAI_EMBEDDING_API_VERSION") or "").strip(),
            azure_openai_gpt52_endpoint=(os.getenv("AZURE_OPENAI_GPT52_ENDPOINT") or "").strip(),
            azure_openai_gpt52_deployment=(os.getenv("AZURE_OPENAI_GPT52_DEPLOYMENT") or "").strip(),
            azure_openai_gpt52_api_version=(os.getenv("AZURE_OPENAI_GPT52_API_VERSION") or "").strip(),
            azure_openai_o3dr_endpoint=(
                os.getenv("AZURE_OPENAI_DEEP_RESEARCH_ENDPOINT")
                or os.getenv("AZURE_OPENAI_O3DR_ENDPOINT")
                or ""
            ).strip(),
            azure_openai_o3dr_deployment=(
                os.getenv("AZURE_OPENAI_DEEP_RESEARCH_DEPLOYMENT")
                or os.getenv("AZURE_OPENAI_O3DR_DEPLOYMENT")
                or ""
            ).strip(),
            azure_openai_o3dr_api_version=(
                os.getenv("AZURE_OPENAI_DEEP_RESEARCH_API_VERSION")
                or os.getenv("AZURE_OPENAI_O3DR_API_VERSION")
                or ""
            ).strip(),
            azure_client_id=(os.getenv("AZURE_CLIENT_ID") or MANAGED_IDENTITY_CLIENT_ID).strip(),
            azure_storage_blob_account_url=(os.getenv("AZURE_STORAGE_BLOB_ACCOUNT_URL") or "").strip(),
            azure_openai_timeout_s=float((os.getenv("AZURE_OPENAI_TIMEOUT_S") or "60").strip() or "60"),
        )


class Clients:
    """Class that manages Azure clients in a centralized place."""

    COGNITIVE_SCOPE = "https://cognitiveservices.azure.com/.default"

    # Env vars that only exist inside an Azure-hosted environment (Container Apps, App Service, Functions…)
    _AZURE_HOST_IDENTITY_HINTS = (
        "IDENTITY_ENDPOINT",
        "MSI_ENDPOINT",
        "WEBSITE_INSTANCE_ID",
        "CONTAINER_APP_NAME",
        "FUNCTIONS_EXTENSION_VERSION",
    )

    # Known Azure CLI install paths on Windows that may not be on PATH
    # when running as a subprocess (writing index builder, pipeline scripts, etc.)
    _AZ_CLI_CANDIDATE_DIRS = [
        r"C:\Tools\azure-cli-2.86.0-x64\bin",
        r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin",
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin",
    ]

    def __init__(
        self,
        AZURE_SEARCH_ENDPOINT: str = "",
        AZURE_OPENAI_ENDPOINT: str = "",
        AZURE_OPENAI_API_VERSION: str = "",
        AZURE_DOC_INT_ENDPOINT: str = "",
        *,
        config: Optional[ClientsConfig] = None,
    ) -> None:
        if config is None:
            config = ClientsConfig(
                azure_search_endpoint=(AZURE_SEARCH_ENDPOINT or "").strip(),
                azure_openai_endpoint=(AZURE_OPENAI_ENDPOINT or "").strip(),
                azure_openai_api_version=(AZURE_OPENAI_API_VERSION or "").strip(),
                azure_docint_endpoint=(AZURE_DOC_INT_ENDPOINT or "").strip().strip("'\""),
            )

        self.config = config

        self.AZURE_SEARCH_ENDPOINT = self.config.azure_search_endpoint
        self.AZURE_OPENAI_ENDPOINT = (
            self.config.azure_openai_gpt52_endpoint or self.config.azure_openai_endpoint
        )
        self.AZURE_OPENAI_API_VERSION = (
            self.config.azure_openai_gpt52_api_version or self.config.azure_openai_api_version
        )
        self.AZURE_DOC_INT_ENDPOINT = self.config.azure_docint_endpoint

        self._credential = None
        self._token_provider = None

        # Cache de clientes AzureOpenAI por perfil ("gpt52" / "gpt41")
        self._oai_clients: dict[str, AzureOpenAI] = {}

    @classmethod
    def from_env(cls) -> "Clients":
        """Build a Clients instance from environment variables."""
        logger.info("[AUTH] Clients.from_env() called")
        return cls(config=ClientsConfig.from_env())

    @classmethod
    def from_config(cls, config: ClientsConfig) -> "Clients":
        """Build a Clients instance from an explicit config object."""
        return cls(config=config)

    def _is_running_in_azure_host(self) -> bool:
        return any((os.getenv(k) or "").strip() for k in self._AZURE_HOST_IDENTITY_HINTS)

    def _log_credential_identity(self, credential) -> None:
        """Decode the JWT token to log which identity is actually authenticating."""
        try:
            token = credential.get_token("https://management.azure.com/.default")
            payload_b64 = token.token.split(".")[1]
            payload_b64 += "=" * (4 - len(payload_b64) % 4)  # fix base64 padding
            claims = json.loads(base64.urlsafe_b64decode(payload_b64))
            identity = (
                claims.get("upn")            # human user (AZ CLI / VS Code)
                or claims.get("unique_name")
                or claims.get("appid")       # service principal / managed identity
                or claims.get("oid")         # object-id fallback
                or "unknown"
            )
            logger.info(
                "[AUTH] Authenticated as: %s  (oid=%s, tid=%s)",
                identity, claims.get("oid", "?"), claims.get("tid", "?"),
            )
        except Exception as exc:
            logger.warning("[AUTH] Could not resolve identity from token: %s", exc)

    @classmethod
    def _ensure_az_cli_on_path(cls) -> None:
        """Add Azure CLI bin dir to PATH if not already resolvable."""
        import shutil
        if shutil.which("az") or shutil.which("az.cmd"):
            return  # already on PATH
        current_path = os.environ.get("PATH", "")
        for candidate in cls._AZ_CLI_CANDIDATE_DIRS:
            if os.path.isdir(candidate) and candidate not in current_path:
                os.environ["PATH"] = candidate + os.pathsep + current_path
                logger.info("[AUTH] Added Azure CLI dir to PATH: %s", candidate)
                return

    def _build_credential(self):
        """
        - Local environment  ->  DefaultAzureCredential (AZ CLI / VS Code), MI excluded.
        - Azure host         ->  ManagedIdentityCredential (user-assigned if client_id present).
        """
        client_id = (self.config.azure_client_id or "").strip() or None
        in_azure = self._is_running_in_azure_host()

        if in_azure:
            if client_id:
                logger.info(
                    "[AUTH] Azure host detected -> ManagedIdentityCredential "
                    "(user-assigned, client_id=%s)", client_id
                )
                credential = ManagedIdentityCredential(client_id=client_id)
            else:
                logger.info("[AUTH] Azure host detected -> ManagedIdentityCredential (system-assigned)")
                credential = ManagedIdentityCredential()
        else:
            self._ensure_az_cli_on_path()
            logger.info(
                "[AUTH] Local environment detected -> DefaultAzureCredential "
                "(AZ CLI / VS Code / Shared cache, Managed Identity EXCLUDED)"
            )
            credential = DefaultAzureCredential(exclude_managed_identity_credential=True)

        self._log_credential_identity(credential)
        return credential

    def _get_credential(self):
        if self._credential is None:
            self._credential = self._build_credential()
        return self._credential

    def _get_cognitive_token_provider(self):
        if self._token_provider is None:
            self._token_provider = get_bearer_token_provider(
                self._get_credential(),
                self.COGNITIVE_SCOPE,
            )
        return self._token_provider

    # ------------------------------------------------------------------
    # Azure OpenAI (chat/completions)
    # ------------------------------------------------------------------

    def get_oai_client(self, max_retries: int = 6) -> AzureOpenAI:
        """Get Azure OpenAI client for chat/completions (perfil GPT-5.2 / default)."""
        endpoint = self.AZURE_OPENAI_ENDPOINT
        api_version = self.AZURE_OPENAI_API_VERSION

        if not endpoint or not api_version:
            raise ValueError("OpenAI endpoint/api_version is not configured")

        logger.info("[AUTH] Building Azure OpenAI client (chat/completions)")

        return AzureOpenAI(
            azure_ad_token_provider=self._get_cognitive_token_provider(),
            api_version=api_version,
            azure_endpoint=endpoint,
            max_retries=max_retries,
        )

    def get_oai_client_for_profile(self, profile: str = "gpt52", max_retries: int = 6) -> AzureOpenAI:
        """
        Get Azure OpenAI client for a specific deployment profile used by the
        multiagent pipeline:

            "gpt52" -> AZURE_OPENAI_GPT52_*  (orquestador, los 5 agentes)
            "gpt41" -> AZURE_OPENAI_*        (gpt-4.1, doc-reader / workers ligeros)
        """
        if profile in self._oai_clients:
            return self._oai_clients[profile]

        if profile == "gpt52":
            endpoint = self.config.azure_openai_gpt52_endpoint
            api_version = self.config.azure_openai_gpt52_api_version
        elif profile == "gpt41":
            endpoint = self.config.azure_openai_endpoint
            api_version = self.config.azure_openai_api_version
        else:
            raise ValueError(f"Perfil desconocido: {profile}")

        if not endpoint or not api_version:
            raise ValueError(f"Endpoint/api_version no configurados para el perfil '{profile}'")

        logger.info("[AUTH] Building Azure OpenAI client (profile=%s)", profile)

        client = AzureOpenAI(
            azure_ad_token_provider=self._get_cognitive_token_provider(),
            api_version=api_version,
            azure_endpoint=endpoint,
            max_retries=max_retries,
        )
        self._oai_clients[profile] = client
        return client

    def get_deployment_name(self, profile: str = "gpt52") -> str:
        """Devuelve el nombre del deployment para el perfil indicado."""
        if profile == "gpt52":
            return self.config.azure_openai_gpt52_deployment
        elif profile == "gpt41":
            return self.config.azure_openai_deployment
        raise ValueError(f"Perfil desconocido: {profile}")

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    def get_embedding_oai_client(self, max_retries: int = 6) -> AzureOpenAI:
        """Get Azure OpenAI client for embeddings."""
        endpoint = (
            self.config.azure_openai_embedding_endpoint
            or self.config.azure_openai_gpt52_endpoint
            or self.config.azure_openai_endpoint
        )
        api_version = (
            self.config.azure_openai_embedding_api_version
            or self.config.azure_openai_gpt52_api_version
            or self.config.azure_openai_api_version
        )

        if not endpoint or not api_version:
            raise ValueError("Embedding OpenAI endpoint/api_version is not configured")

        logger.info("[AUTH] Building Azure OpenAI client (embeddings)")

        return AzureOpenAI(
            azure_ad_token_provider=self._get_cognitive_token_provider(),
            api_version=api_version,
            azure_endpoint=endpoint,
            max_retries=max_retries,
        )

    # ------------------------------------------------------------------
    # Document Intelligence
    # ------------------------------------------------------------------

    def get_docint_client(self):
        """Get Azure Document Intelligence client."""
        if not self.AZURE_DOC_INT_ENDPOINT:
            raise ValueError("Document Intelligence endpoint is not configured")

        logger.info("[AUTH] Building Azure Document Intelligence client")

        from azure.ai.documentintelligence import DocumentIntelligenceClient

        return DocumentIntelligenceClient(
            endpoint=self.AZURE_DOC_INT_ENDPOINT,
            credential=self._get_credential(),
        )

    # ------------------------------------------------------------------
    # AI Search
    # ------------------------------------------------------------------

    def get_search_client(self, index_name: str):
        """Get Azure AI Search query client for an index."""
        if not self.AZURE_SEARCH_ENDPOINT:
            raise ValueError("Search endpoint is not configured")

        if get_ai_search is not None:
            return get_ai_search(endpoint=self.AZURE_SEARCH_ENDPOINT).get_search_client(index_name)

        from azure.search.documents import SearchClient

        return SearchClient(
            endpoint=self.AZURE_SEARCH_ENDPOINT,
            index_name=index_name,
            credential=self._get_credential(),
        )

    def get_default_search_client(self):
        """Get SearchClient using configured AZURE_SEARCH_INDEX_NAME."""
        if not self.config.azure_search_index_name:
            raise ValueError("Search index name is not configured")
        return self.get_search_client(index_name=self.config.azure_search_index_name)

    def get_index_client(self):
        """Get Azure AI Search index management client."""
        if not self.AZURE_SEARCH_ENDPOINT:
            raise ValueError("Search endpoint is not configured")

        if get_ai_search is not None:
            return get_ai_search(endpoint=self.AZURE_SEARCH_ENDPOINT).get_index_client()

        from azure.search.documents.indexes import SearchIndexClient

        return SearchIndexClient(
            endpoint=self.AZURE_SEARCH_ENDPOINT,
            credential=self._get_credential(),
        )

    # ------------------------------------------------------------------
    # Blob Storage
    # ------------------------------------------------------------------

    def get_blob_service_client(self):
        """Get BlobServiceClient using managed identity."""
        if not self.config.azure_storage_blob_account_url:
            raise ValueError("Blob account URL is not configured")

        from azure.storage.blob import BlobServiceClient

        return BlobServiceClient(
            account_url=self.config.azure_storage_blob_account_url,
            credential=self._get_credential(),
        )

    def get_blob_client(self, container: str, blob: str):
        """Get blob client from container/blob name."""
        if get_blob_storage is not None:
            return get_blob_storage().service_client.get_blob_client(container=container, blob=blob)

        service_client = self.get_blob_service_client()
        return service_client.get_blob_client(container=container, blob=blob)

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def get_gpt_deployment(self) -> str:
        """Get default GPT deployment name from config."""
        return self.config.azure_openai_gpt52_deployment or self.config.azure_openai_deployment

    def get_embedding_deployment(self) -> str:
        """Get default embedding deployment name from config."""
        return self.config.azure_openai_embedding_deployment

    def get_timeout_s(self) -> float:
        """Get configured OpenAI timeout in seconds."""
        return self.config.azure_openai_timeout_s

    # ------------------------------------------------------------------
    # Deep Research
    # ------------------------------------------------------------------

    def get_deep_research_config(self) -> tuple[str, str, str]:
        """Get Deep Research endpoint, deployment and api_version from config.

        Falls back to empty values if not configured.
        """
        return (
            (self.config.azure_openai_o3dr_endpoint or "").strip(),
            (self.config.azure_openai_o3dr_deployment or "").strip(),
            (self.config.azure_openai_o3dr_api_version or "").strip(),
        )

    def get_deep_research_oai_client(self, max_retries: int = 3) -> tuple[OpenAI, str]:
        """Get OpenAI client for the dedicated Deep Research resource (/openai/v1/).

        El endpoint de deep research usa la Responses API con base_url /openai/v1/,
        que acepta un Bearer token de Azure AD como api_key (no AzureOpenAI).
        Se obtiene un token fresco en cada llamada para evitar expiración.
        """
        endpoint, deployment, _ = self.get_deep_research_config()

        if not endpoint or not deployment:
            raise ValueError(
                "Deep Research endpoint/deployment not configured "
                "(AZURE_OPENAI_DEEP_RESEARCH_ENDPOINT / AZURE_OPENAI_DEEP_RESEARCH_DEPLOYMENT)"
            )

        logger.info("[AUTH] Building OpenAI client (deep-research, base_url=%s)", endpoint)
        # Token fresco en cada llamada (los tokens expiran ~1h; no se cachea este cliente)
        token = self._get_credential().get_token(self.COGNITIVE_SCOPE)
        client = OpenAI(
            base_url=endpoint,
            api_key=token.token,
            max_retries=max_retries,
        )
        return client, deployment


# ----------------------------------------------------------------------
# Capa de conveniencia para el pipeline multiagente (interfaz simple usada
# por agents/*/agent.py: get_azure_client / get_deployment_name / chat_completion)
# ----------------------------------------------------------------------

@lru_cache(maxsize=1)
def _get_clients() -> Clients:
    """Singleton de Clients para toda la aplicación."""
    return Clients.from_env()


def get_azure_client(profile: str = "gpt52") -> AzureOpenAI:
    """
    Devuelve un cliente AzureOpenAI configurado para el perfil indicado:

        "gpt52" -> AZURE_OPENAI_GPT52_*  (orquestador, los 5 agentes del pipeline)
        "gpt41" -> AZURE_OPENAI_*        (gpt-4.1, doc-reader / workers ligeros)
    """
    return _get_clients().get_oai_client_for_profile(profile)


def get_deployment_name(profile: str = "gpt52") -> str:
    """Devuelve el nombre del deployment correspondiente al perfil."""
    return _get_clients().get_deployment_name(profile)


def chat_completion(messages, profile: str = "gpt52", tools=None, tool_choice=None, **kwargs):
    """
    Wrapper fino sobre client.chat.completions.create(), usado por todos los
    agentes del pipeline.

    messages: lista de dicts {"role": ..., "content": ...}
    profile: "gpt52" o "gpt41"
    tools: lista de definiciones de function-calling (formato OpenAI)
    """
    client = get_azure_client(profile)
    deployment = get_deployment_name(profile)

    params = {
        "model": deployment,
        "messages": messages,
        **kwargs,
    }
    if tools:
        params["tools"] = tools
    if tool_choice:
        params["tool_choice"] = tool_choice

    return client.chat.completions.create(**params)