"""
src/agents/valuation_reviewer/agent.py
=========================================
Valuation Reviewer Agent -- Agente 4 de 5 del pipeline KYC + Credit Risk Intelligence.

Calcula ratios de riesgo, los compara con el historico del cliente y
genera una interpretacion cualitativa.
"""

import json

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.valuation_reviewer.prompt import get_system_prompt

logger = get_logger("kyc")


def run_valuation_reviewer_agent(modelo_financiero: dict, historial: dict) -> dict:
    """
    modelo_financiero: output del Model Builder Agent.
    historial:         historial bancario del cliente desde bbdd.json.

    Devuelve:
        {
          "ratios": {
            "ratios_por_periodo": [...],
            "variacion": {...}
          },
          "interpretacion": "..."
        }
    """
    logger.info("=== [Valuation Reviewer Agent] Inicio ===")

    system_prompt = get_system_prompt(
        extra="Analiza el modelo financiero y compara con el historial bancario del cliente."
    )

    user_msg = (
        "Modelo financiero normalizado (Model Builder Agent):\n"
        + json.dumps(modelo_financiero, ensure_ascii=False, indent=2)
        + "\n\nHistorial bancario del cliente:\n"
        + json.dumps(historial, ensure_ascii=False, indent=2)
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
    except json.JSONDecodeError:
        logger.warning("[Valuation Reviewer Agent] respuesta no-JSON")
        result = {
            "ratios": {"ratios_por_periodo": [], "variacion": {}},
            "interpretacion": "",
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    logger.info("[Valuation Reviewer Agent] interpretacion generada")
    logger.info("=== [Valuation Reviewer Agent] Fin ===")
    return result