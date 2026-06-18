"""
src/agents/credit_risk_report/agent.py
=========================================
Credit Risk Report Agent -- Agente 5 de 5 del pipeline KYC + Credit Risk Intelligence.

Sintetiza los outputs de todos los agentes anteriores en el informe final
de riesgo de credito para el comite de riesgos.
"""

import json

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.credit_risk_report.prompt import get_system_prompt

logger = get_logger("kyc")


def run_credit_risk_report_agent(
    entity_name: str,
    kyc_output: dict,
    modelo_financiero: dict,
    valuation_output: dict,
    market_research_output: str,
) -> str:
    """
    Recibe todos los outputs del pipeline y devuelve el informe final
    en formato markdown.
    """
    logger.info("=== [Credit Risk Report Agent] Inicio (empresa=%s) ===", entity_name)

    system_prompt = get_system_prompt(
        extra=f"Empresa analizada: {entity_name}"
    )

    user_msg = (
        f"Empresa: {entity_name}\n\n"
        "--- OUTPUT KYC SCREENER AGENT ---\n"
        + json.dumps(kyc_output, ensure_ascii=False, indent=2)
        + "\n\n--- OUTPUT MODEL BUILDER AGENT ---\n"
        + json.dumps(modelo_financiero, ensure_ascii=False, indent=2)
        + "\n\n--- OUTPUT VALUATION REVIEWER AGENT ---\n"
        + json.dumps(valuation_output, ensure_ascii=False, indent=2)
        + "\n\n--- OUTPUT MARKET RESEARCHER AGENT ---\n"
        + market_research_output
        + "\n\nRedacta el informe final de riesgo de credito en markdown."
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
        ],
        profile="gpt52",
        temperature=0.2,
    )

    output = response.choices[0].message.content or ""
    logger.info("[Credit Risk Report Agent] informe generado (%d chars)", len(output))
    logger.info("=== [Credit Risk Report Agent] Fin ===")
    return output