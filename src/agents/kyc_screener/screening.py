"""
agents/kyc_screener/screening.py
==================================
Equivalente a la parte "Screen" del agente kyc-screener.md (screening MCP).

En el repo original esto se hace vía un MCP server de un proveedor de screening
(World-Check / Refinitiv / Dow Jones / LSEG...). Aquí se modela como una función
de "tool" que GPT-5 puede invocar via function calling, con dos implementaciones:

- mock_screening_lookup: usa los JSON locales (listas_sanciones.json) para
  desarrollo/demo, sin llamadas externas.
- real_screening_lookup: placeholder para tu proveedor real (World-Check API,
  Dow Jones Risk & Compliance, etc.) -- sustituye el TODO por la llamada real.
"""

import json
from pathlib import Path

from src.logging_utils import get_logger

logger = get_logger()

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


def local_screening_lookup(name: str) -> dict:
    """
    Búsqueda en la BBDD local contra data/listas_sanciones.json.
    Estructura esperada del JSON: lista de dicts con "nombre", "tipo" (sanciones/pep),
    "lista", "confianza".
    """
    bbdd_path = DATA_DIR / "bbdd.json"
    registros = []
    if bbdd_path.exists():
        with open(bbdd_path, encoding="utf-8") as f:
            bbdd = json.load(f)
        registros = bbdd.get("listas_sanciones", []) or []

    if not registros:
        sanciones_path = DATA_DIR / "listas_sanciones.json"
        if not sanciones_path.exists():
            return {"name": name, "hits": [], "source": "local_db", "note": "fichero de sanciones no encontrado"}
        with open(sanciones_path, encoding="utf-8") as f:
            registros = json.load(f)

    name_lower = name.strip().lower()
    hits = [
        r for r in registros
        if name_lower and name_lower in r.get("nombre", "").lower()
    ]
    return {
        "name": name,
        "hits": hits,
        "source": "local_db",
        "note": (
            "Resultado basado en fuente local de demo; repetir screening en fuente operativa "
            "actualizada (UE/OFAC/ONU/HMT y/o proveedor interno) para cierre concluyente."
        ),
        "confidence": "non_conclusive" if not hits else "review_required",
    }


def real_screening_lookup(name: str) -> dict:
    """
    Conector de screening para entorno "real" de esta demo.
    Mientras no haya proveedor externo, usa la BBDD local.

    Ejemplo de integración con World-Check One (Refinitiv) vía REST:

        import requests
        resp = requests.post(
            f"{WORLDCHECK_ENDPOINT}/v1/cases/{case_id}/screeningRequest",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": name, "providerTypes": ["WATCHLIST"]},
        )
        return resp.json()

    Mientras no esté configurado, lanza NotImplementedError para evitar
    falsos negativos silenciosos en producción.
    """
    return local_screening_lookup(name)


SCREENING_TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "screening_lookup",
        "description": (
            "Busca un nombre de persona o entidad en listas de sanciones, PEP y "
            "adverse media. Devuelve los hits encontrados con nivel de confianza."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Nombre completo de la persona o entidad a screenear",
                }
            },
            "required": ["name"],
        },
    },
}


def run_screening_tool(arguments: dict, use_mock: bool = False) -> dict:
    """Dispatcher invocado cuando GPT-5 llama a la tool screening_lookup."""
    name = arguments.get("name", "")
    logger.info("[KYC Screener Agent] screening: %s (use_mock=%s)", name, use_mock)
    if use_mock:
        result = local_screening_lookup(name)
    else:
        result = real_screening_lookup(name)
    logger.info("[KYC Screener Agent] screening: %s -> %d hits", name, len(result.get("hits", [])))
    return result