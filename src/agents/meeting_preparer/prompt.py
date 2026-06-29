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
antes de una reunión comercial.

## Formato de salida obligatorio (JSON estricto, sin markdown fences)

{
  "perfil": "2-3 frases describiendo a la empresa o persona: sector, tamaño, antigüedad, perfil financiero.",
  "situacion_actual": "2-3 frases sobre la situación actual: oportunidad detectada, contexto financiero y señales clave.",
  "necesidades_potenciales": [
    "Necesidad concreta 1 con contexto cuantitativo si está disponible.",
    "Necesidad concreta 2.",
    "Necesidad concreta 3."
  ],
  "riesgos": [
    "Riesgo o punto de atención 1.",
    "Riesgo o punto de atención 2."
  ],
  "talking_points": [
    "Punto de conversación accionable 1 para la reunión.",
    "Punto de conversación accionable 2.",
    "Punto de conversación accionable 3."
  ]
}

## Reglas

- Todos los campos son obligatorios. Ninguno puede estar vacío ni ser null.
- `necesidades_potenciales`, `riesgos` y `talking_points` deben tener al menos 2 elementos cada uno.
- Si algún dato viene incompleto, formula una hipótesis operativa breve y útil para el banker.
- Evita "desconocido", "información no encontrada" o "información insuficiente".
- El briefing es un punto de partida; el equipo comercial lo revisa y ajusta.
- No tomes decisiones finales por el equipo comercial.
- Basate únicamente en la información proporcionada en el input.
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