"""
src/prompt_loader.py
======================
Carga system prompts y skills desde los ficheros .md de plugins/.

Estructura esperada en el repo:
    plugins/agent-plugins/<slug>/agents/<slug>.md     <- system prompt del agente
    plugins/agent-plugins/<slug>/skills/<skill>/SKILL.md  <- skills del agente

Uso:
    from prompt_loader import PromptLoader
    loader = PromptLoader()
    system_prompt = loader.build_system_prompt("kyc-screener", ["kyc-doc-parse", "kyc-rules"])
"""

from pathlib import Path

# Raiz del proyecto (dos niveles arriba desde src/)
_REPO_ROOT = Path(__file__).resolve().parent.parent
_PLUGINS_DIR = _REPO_ROOT / "plugins" / "agent-plugins"


class PromptLoader:

    def __init__(self):
        self._cache: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Lectura de ficheros .md
    # ------------------------------------------------------------------

    def load_agent_md(self, agent_slug: str) -> str:
        """
        Lee plugins/agent-plugins/<agent_slug>/agents/<agent_slug>.md
        y devuelve su contenido como string.

        agent_slug: el nombre de la carpeta del agente, por ejemplo
                    "kyc-screener", "model-builder", "pitch-agent"

        Si el fichero no existe lanza FileNotFoundError con un mensaje
        claro para facilitar el diagnostico.
        """
        cache_key = f"agent:{agent_slug}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        path = _PLUGINS_DIR / agent_slug / "agents" / f"{agent_slug}.md"
        if not path.exists():
            raise FileNotFoundError(
                f"No se encontro el prompt del agente '{agent_slug}'.\n"
                f"Ruta buscada: {path}\n"
                f"Comprueba que el slug coincide exactamente con el nombre "
                f"de la carpeta en plugins/agent-plugins/."
            )

        content = path.read_text(encoding="utf-8")
        self._cache[cache_key] = content
        return content

    def load_skill_md(self, agent_slug: str, skill_name: str) -> str:
        """
        Lee plugins/agent-plugins/<agent_slug>/skills/<skill_name>/SKILL.md
        y devuelve su contenido.

        Si no existe, devuelve un string vacio (las skills son opcionales:
        si faltan el agente sigue funcionando con el prompt base).
        """
        cache_key = f"skill:{agent_slug}:{skill_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        path = _PLUGINS_DIR / agent_slug / "skills" / skill_name / "SKILL.md"
        if not path.exists():
            return ""

        content = path.read_text(encoding="utf-8")
        self._cache[cache_key] = content
        return content

    # ------------------------------------------------------------------
    # Construccion del system prompt completo
    # ------------------------------------------------------------------

    def build_system_prompt(
        self,
        agent_slug: str,
        skill_names: list[str],
        extra_instructions: str = "",
    ) -> str:
        """
        Construye el system prompt completo para un agente combinando:
          1. El .md principal del agente (su identidad, outputs esperados, reglas)
          2. Las skills solicitadas (conocimiento de dominio especifico)
          3. Instrucciones extra opcionales (contexto especifico del pipeline)

        agent_slug:         "kyc-screener", "model-builder", etc.
        skill_names:        lista de nombres de skills a incluir,
                            por ejemplo ["kyc-doc-parse", "kyc-rules"]
        extra_instructions: texto adicional a anadir al final del prompt
                            (usado para pasar contexto del pipeline, como
                            el nombre de la empresa o el sector)

        Devuelve el system prompt completo como string.
        """
        parts = []

        # 1. Prompt base del agente
        agent_md = self.load_agent_md(agent_slug)
        parts.append(agent_md.strip())

        # 2. Skills de dominio
        loaded_skills = []
        for skill_name in skill_names:
            skill_content = self.load_skill_md(agent_slug, skill_name)
            if skill_content:
                loaded_skills.append((skill_name, skill_content.strip()))

        if loaded_skills:
            parts.append("\n\n---\n# Skills aplicables\n")
            for skill_name, skill_content in loaded_skills:
                parts.append(f"\n## {skill_name}\n\n{skill_content}")

        # 3. Instrucciones extra del pipeline
        if extra_instructions:
            parts.append(f"\n\n---\n# Contexto de la ejecucion actual\n\n{extra_instructions.strip()}")

        return "\n".join(parts)


# Instancia global reutilizable (evita releer ficheros en cada llamada)
_loader: PromptLoader | None = None


def get_loader() -> PromptLoader:
    global _loader
    if _loader is None:
        _loader = PromptLoader()
    return _loader


def build_system_prompt(
    agent_slug: str,
    skill_names: list[str],
    extra_instructions: str = "",
) -> str:
    """Atajo para usar el loader global sin instanciarlo manualmente."""
    return get_loader().build_system_prompt(agent_slug, skill_names, extra_instructions)