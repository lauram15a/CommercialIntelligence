"""
src/agents/meeting_preparer/agent.py
=======================================
Meeting Preparer Agent -- Agente 4 de 5 del pipeline Corporate & Deal
Intelligence.

Genera un briefing estructurado (perfil, situacion actual, necesidades,
riesgos, talking points) para el equipo comercial antes de una reunion.

Skills: client-report, client-review
"""

import json

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()

MEETING_PREPARER_TASK_PROMPT = """Eres el "Meeting Preparer Agent" dentro de un
pipeline de Corporate & Deal Intelligence para un banco con actividad
comercial.

Recibiras:
1. El nombre de la empresa objetivo y el motivo por el que fue identificada
   como oportunidad (del Opportunity Researcher Agent).
2. El analisis de resultados financieros del Earnings Reviewer Agent (texto).
3. Una vision financiera basica del Model Builder Agent.

TAREA: genera un BRIEFING DE CLIENTE estructurado en JSON:

- perfil: 2-3 frases describiendo a la empresa.
- situacion_actual: 2-3 frases sobre la situacion actual.
- necesidades_potenciales: lista de 2-4 necesidades de financiacion o asesoramiento.
- riesgos: lista de 2-4 riesgos o puntos de atencion.
- talking_points: lista de 3-5 puntos de conversacion concretos y accionables.

FORMATO DE SALIDA (JSON estricto, sin texto adicional, sin markdown fences):
{
  "perfil": "...",
  "situacion_actual": "...",
  "necesidades_potenciales": ["...", "..."],
  "riesgos": ["...", "..."],
  "talking_points": ["...", "...", "..."]
}

REGLAS:
- Basate unicamente en la informacion proporcionada.
- Tono profesional y orientado a la accion, para leer en 2 minutos.
- No tomes decisiones finales por el equipo comercial.
"""


def _has_prompt(agent_key: str) -> bool:
    try:
        from src.skill_loader import AGENT_PROMPTS  # type: ignore
        return agent_key in AGENT_PROMPTS
    except Exception:
        return False


def _fallback_prompt() -> str:
    return (
        "Eres un asistente de banca corporativa especializado en preparar "
        "briefings de cliente claros, accionables y orientados a la reunion comercial."
    )


def run_meeting_preparer_agent(
    company_name: str,
    opportunity_context: dict,
    earnings_summary: str,
    model_output: dict | None = None,
) -> dict:
    """
    company_name: nombre de la empresa objetivo
    opportunity_context: dict con {"motivo": ..., "prioridad": ...}
    earnings_summary: texto del Earnings Reviewer Agent
    model_output: salida del Model Builder Agent (opcional)
    """
    logger.info("=== [Meeting Preparer Agent] Inicio (empresa=%s) ===", company_name)

    base_prompt = load_agent_prompt("meeting-prep-agent") if _has_prompt("meeting-prep-agent") else _fallback_prompt()
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Corporate & Deal Intelligence)\n"
        + MEETING_PREPARER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["portfolio-monitoring"])

    model_block = "Sin vision financiera adicional del Model Builder Agent (paso opcional no disponible)."
    if model_output and model_output.get("disponible"):
        model_block = json.dumps(model_output, ensure_ascii=False, indent=2)

    user_msg = (
        f"Empresa objetivo: {company_name}\n\n"
        f"Motivo de la oportunidad (Opportunity Researcher Agent): "
        f"{opportunity_context.get('motivo', 'no especificado')} "
        f"(prioridad: {opportunity_context.get('prioridad', 'no especificada')})\n\n"
        f"Analisis de resultados financieros (Earnings Reviewer Agent):\n{earnings_summary}\n\n"
        f"Vision financiera basica (Model Builder Agent):\n{model_block}"
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
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

    logger.info("[Meeting Preparer Agent] briefing generado: %d necesidades, %d riesgos, %d talking points",
                len(result.get("necesidades_potenciales", [])),
                len(result.get("riesgos", [])),
                len(result.get("talking_points", [])))
    logger.info("=== [Meeting Preparer Agent] Fin ===")
    return result