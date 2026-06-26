"""
src/agents/pitch_builder/prompt.py
=====================================
Carga el system prompt del Pitch Builder Agent desde:
  plugins/agent-plugins/pitch-agent/agents/pitch-agent.md
  plugins/agent-plugins/pitch-agent/skills/pitch-deck/SKILL.md
  plugins/agent-plugins/pitch-agent/skills/comps-analysis/SKILL.md
  plugins/agent-plugins/pitch-agent/skills/sector-overview/SKILL.md
"""

from prompt_loader import build_system_prompt

PITCH_EXTRA = """
Dentro de este pipeline, eres el ultimo agente. Tu tarea es generar el
contenido de una PROPUESTA COMERCIAL lista para convertirse en pitchbook.

FORMATO DE SALIDA (JSON estricto, sin markdown fences):
{
  "titulo": "...",
  "subtitulo": "1 frase que resume la oportunidad",
  "oportunidad_detectada": "2-3 frases describiendo la oportunidad",
  "contexto_financiero": ["punto 1", "punto 2", "punto 3"],
  "encaje_productos": ["producto 1", "producto 2"],
  "comparables": ["comparable 1", "comparable 2"],
  "argumentos_valor": ["argumento 1", "argumento 2", "argumento 3"],
  "proximos_pasos": ["paso 1", "paso 2", "paso 3"],
  "narrativa_markdown": "resumen ejecutivo en markdown de 3-5 parrafos"
}

Usa nombres genericos de producto de banca.
No uses marcas registradas de terceros.
Si falta algun dato, usa una hipotesis prudente y declarativa, manteniendo
la narrativa accionable. Evita expresiones "desconocido", "informacion no encontrada"
o "informacion insuficiente".
Termina narrativa_markdown con: "El equipo comercial revisa, ajusta y
personaliza esta propuesta antes de cualquier interaccion con el cliente."
"""


def get_system_prompt(extra: str = "") -> str:
    combined_extra = PITCH_EXTRA
    if extra:
        combined_extra += f"\n\n{extra.strip()}"
    return build_system_prompt(
        agent_slug="pitch-agent",
        skill_names=["pitch-deck", "comps-analysis", "sector-overview"],
        extra_instructions=combined_extra,
    )