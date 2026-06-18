"""
src/agents/model_builder/agent.py
====================================
Model Builder Agent -- Agente 2 de 5 del pipeline KYC + Credit Risk Intelligence.

Normaliza los estados financieros a un modelo multi-periodo y calcula
los ratios de riesgo clave.
"""

import json

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.model_builder.prompt import get_system_prompt

logger = get_logger("kyc")


def run_model_builder_agent(extracted_entities: list[dict]) -> dict:
    """
    extracted_entities: lista de entidades extraidas por el KYC Screener Agent.

    Devuelve:
        {
          "periodos": [{"periodo": "2024", "ebitda": ..., "deuda_financiera": ..., ...}],
          "resumen": "...",
          "audit_flags": [...]
        }
    """
    logger.info("=== [Model Builder Agent] Inicio (%d entidades) ===", len(extracted_entities))

    system_prompt = get_system_prompt(
        extra="Normaliza los datos financieros disponibles en las entidades extraidas."
    )

    user_msg = (
        "Entidades extraidas por el KYC Screener Agent:\n\n"
        + json.dumps(extracted_entities, ensure_ascii=False, indent=2)
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
        logger.warning("[Model Builder Agent] respuesta no-JSON")
        result = {
            "periodos": [],
            "resumen": "",
            "audit_flags": [],
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    logger.info(
        "[Model Builder Agent] %d periodos, %d audit_flags",
        len(result.get("periodos", [])),
        len(result.get("audit_flags", [])),
    )
    logger.info("=== [Model Builder Agent] Fin ===")
    return result