"""
src/agents/opportunity_researcher/agent.py
=============================================
Opportunity Researcher Agent -- Agente 1 de 5 del pipeline Deal Intelligence.

Identifica y prioriza empresas con potencial de financiacion o asesoramiento
dentro de un sector concreto.
"""

import json
from pathlib import Path

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.opportunity_researcher.prompt import get_system_prompt

logger = get_logger("deal")

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


def run_opportunity_researcher_agent(sector: str, use_mock: bool = True) -> dict:
    """
    sector: nombre del sector a analizar (p.ej. "Industrial").

    Devuelve:
        {
          "sector": "...",
          "oportunidades": [{"empresa", "motivo", "prioridad", ...}],
          "resumen": "..."
        }
    """
    logger.info("=== [Opportunity Researcher Agent] Inicio (sector=%s) ===", sector)

    # Cargar empresas del sector desde bbdd.json
    empresas = _load_empresas_sector(sector)

    system_prompt = get_system_prompt(
        extra=f"Sector a analizar en esta ejecucion: {sector}"
    )

    user_msg = (
        f"Sector: {sector}\n\n"
        f"Empresas detectadas en la base de datos:\n"
        + json.dumps(empresas, ensure_ascii=False, indent=2)
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
        ],
        profile="gpt52",
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        logger.warning("[Opportunity Researcher Agent] respuesta no-JSON")
        result = {
            "sector": sector,
            "oportunidades": [],
            "resumen": "",
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    logger.info(
        "[Opportunity Researcher Agent] %d oportunidades para sector '%s'",
        len(result.get("oportunidades", [])), sector,
    )
    logger.info("=== [Opportunity Researcher Agent] Fin ===")
    return result


def _load_empresas_sector(sector: str) -> list[dict]:
    """Carga las empresas de un sector desde bbdd.json."""
    bbdd_path = DATA_DIR / "bbdd.json"
    if not bbdd_path.exists():
        return []
    try:
        with open(bbdd_path, encoding="utf-8") as f:
            bbdd = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    empresas_deal = bbdd.get("empresas_deal", {})
    empresas = empresas_deal.get(sector)

    # Si no hay match exacto, buscar case-insensitive
    if empresas is None:
        sector_lower = sector.strip().lower()
        for key, val in empresas_deal.items():
            if key.lower() == sector_lower:
                empresas = val
                break

    # Si el sector no existe en bbdd, devolver todas las empresas disponibles
    # para que el agente tenga algo con lo que trabajar
    if empresas is None:
        all_empresas = []
        for val in empresas_deal.values():
            all_empresas.extend(val)
        return all_empresas

    return empresas