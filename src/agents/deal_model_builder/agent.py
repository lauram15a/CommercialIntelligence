"""
src/agents/deal_model_builder/agent.py
=========================================
Deal Model Builder Agent (opcional) -- Agente 3 de 5 del pipeline Deal Intelligence.

Extrae indicadores clave y tendencias estructurales del texto generado
por el Earnings Reviewer Agent.

Es OPCIONAL: si no hay earnings_summary devuelve {"disponible": False}.
"""

import json

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.deal_model_builder.prompt import get_system_prompt

logger = get_logger("deal")


def run_deal_model_builder_agent(
    company_name: str,
    earnings_summary: str,
) -> dict:
    """
    company_name:     nombre de la empresa objetivo.
    earnings_summary: texto del Earnings Reviewer Agent.

    Devuelve dict con indicadores, tendencias e interpretacion.
    Si earnings_summary esta vacio, devuelve {"disponible": False}.
    """
    logger.info("=== [Model Builder Agent - Deal] Inicio (empresa=%s) ===", company_name)

    if not earnings_summary or not earnings_summary.strip():
        logger.info("[Model Builder Agent - Deal] sin earnings_summary: agente omitido")
        logger.info("=== [Model Builder Agent - Deal] Fin (omitido) ===")
        return {
            "disponible": False,
            "indicadores_clave": [],
            "tendencias_estructurales": [],
            "interpretacion": "",
        }

    system_prompt = get_system_prompt(
        extra=f"Empresa objetivo: {company_name}"
    )

    user_msg = (
        f"Empresa objetivo: {company_name}\n\n"
        f"Analisis del Earnings Reviewer Agent:\n{earnings_summary}"
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
        ],
        profile="gpt52",
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
        result["disponible"] = True
    except json.JSONDecodeError:
        logger.warning("[Model Builder Agent - Deal] respuesta no-JSON")
        result = {
            "disponible": False,
            "indicadores_clave": [],
            "tendencias_estructurales": [],
            "interpretacion": "",
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    logger.info(
        "[Model Builder Agent - Deal] %d indicadores, %d tendencias",
        len(result.get("indicadores_clave", [])),
        len(result.get("tendencias_estructurales", [])),
    )
    logger.info("=== [Model Builder Agent - Deal] Fin ===")
    return result