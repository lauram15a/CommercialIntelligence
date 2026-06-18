"""
src/agents/meeting_preparer/prompt.py
========================================
Carga el system prompt del Meeting Preparer Agent desde:
  plugins/agent-plugins/meeting-prep-agent/agents/meeting-prep-agent.md
  plugins/agent-plugins/meeting-prep-agent/skills/client-report/SKILL.md
  plugins/agent-plugins/meeting-prep-agent/skills/client-review/SKILL.md
"""

from prompt_loader import build_system_prompt

MEETING_EXTRA = """
Dentro de este pipeline, tu tarea es generar un BRIEFING DE CLIENTE
estructurado en JSON, listo para que un banker lo revise en 2 minutos
antes de una reunion comercial.

FORMATO DE SALIDA (JSON estricto, sin markdown fences):
{
  "perfil": "2-3 frases describiendo a la empresa",
  "situacion_actual": "2-3 frases sobre la situacion actual",
  "necesidades_potenciales": ["...", "..."],
  "riesgos": ["...", "..."],
  "talking_points": ["...", "...", "..."]
}

Basate unicamente en la informacion proporcionada.
No tomes decisiones finales por el equipo comercial.
El briefing es un punto de partida para que el equipo revise y ajuste.
"""


def get_system_prompt(extra: str = "") -> str:
    combined_extra = MEETING_EXTRA
    if extra:
        combined_extra += f"\n\n{extra.strip()}"
    return build_system_prompt(
        agent_slug="meeting-prep-agent",
        skill_names=["client-report", "client-review"],
        extra_instructions=combined_extra,
    )