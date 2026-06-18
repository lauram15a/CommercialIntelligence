"""
src/agents/meeting_preparer/agent.py
=======================================
Meeting Preparer Agent -- Agente 4 de 5 del pipeline Deal Intelligence.

Genera el briefing de cliente estructurado para el equipo comercial:
perfil, situacion actual, necesidades potenciales, riesgos y talking points.
"""

import json

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.meeting_preparer.prompt import get_system_prompt

logger = get_logger("deal")


def run_meeting_preparer_agent(
    company_name: str,
    opportunity_context: dict,
    earnings_summary: str,
    model_output: dict | None = None,
) -> dict:
    """
    company_name:         nombre de la empresa objetivo.
    opportunity_context:  dict con {"motivo", "prioridad", ...} del Opportunity Researcher.
    earnings_summary:     texto del Earnings Reviewer Agent.
    model_output:         salida del Deal Model Builder Agent (opcional).

    Devuelve:
        {
          "perfil": "...",
          "situacion_actual": "...",
          "necesidades_potenciales": [...],
          "riesgos": [...],
          "talking_points": [...]
        }
    """
    logger.info("=== [Meeting Preparer Agent] Inicio (empresa=%s) ===", company_name)

    system_prompt = get_system_prompt(
        extra=f"Empresa objetivo: {company_name}"
    )

    model_block = "Sin vision financiera adicional del Model Builder Agent (paso opcional no disponible)."
    if model_output and model_output.get("disponible"):
        model_block = json.dumps(model_output, ensure_ascii=False, indent=2)

    # Incluir historial bancario si viene en opportunity_context
    historial_block = ""
    if opportunity_context.get("historial_banco"):
        historial_block = (
            f"\nHistorial bancario del cliente:\n{opportunity_context['historial_banco']}"
        )

    user_msg = (
        f"Empresa objetivo: {company_name}\n\n"
        f"Motivo de la oportunidad (Opportunity Researcher Agent): "
        f"{opportunity_context.get('motivo', 'no especificado')} "
        f"(prioridad: {opportunity_context.get('prioridad', 'no especificada')})"
        f"{historial_block}\n\n"
        f"Analisis de resultados financieros (Earnings Reviewer Agent):\n{earnings_summary}\n\n"
        f"Vision financiera basica (Model Builder Agent):\n{model_block}"
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
        logger.warning("[Meeting Preparer Agent] respuesta no-JSON")
        result = {
            "perfil": "",
            "situacion_actual": "",
            "necesidades_potenciales": [],
            "riesgos": [],
            "talking_points": [],
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    logger.info(
        "[Meeting Preparer Agent] %d necesidades, %d riesgos, %d talking points",
        len(result.get("necesidades_potenciales", [])),
        len(result.get("riesgos", [])),
        len(result.get("talking_points", [])),
    )
    logger.info("=== [Meeting Preparer Agent] Fin ===")
    return result