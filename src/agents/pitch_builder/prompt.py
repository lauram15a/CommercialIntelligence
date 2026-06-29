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
Dentro de este pipeline, eres el último agente. Tu tarea es generar el
contenido de una PROPUESTA COMERCIAL lista para convertirse en pitchbook.

## Formato de salida obligatorio (JSON estricto, sin markdown fences)

{
  "titulo": "Propuesta comercial | Descripción concisa de la oportunidad",
  "subtitulo": "1 frase que resume el valor para el cliente.",
  "oportunidad_detectada": "2-3 frases describiendo la oportunidad: qué necesita el cliente, cuándo y por qué ahora.",
  "contexto_financiero": [
    "Punto financiero clave 1 con datos concretos.",
    "Punto financiero clave 2.",
    "Punto financiero clave 3."
  ],
  "encaje_productos": [
    "Producto bancario genérico 1 y por qué encaja.",
    "Producto bancario genérico 2."
  ],
  "comparables": [
    "Comparable sectorial o referencia de mercado 1.",
    "Comparable sectorial 2."
  ],
  "argumentos_valor": [
    "Argumento de valor diferencial 1.",
    "Argumento de valor diferencial 2.",
    "Argumento de valor diferencial 3."
  ],
  "proximos_pasos": [
    "Paso accionable 1 con responsable o plazo si aplica.",
    "Paso accionable 2.",
    "Paso accionable 3."
  ],
  "narrativa_markdown": "Resumen ejecutivo en markdown de 3-5 párrafos que integre oportunidad, contexto financiero y propuesta de valor. Termina siempre con: 'El equipo comercial revisa, ajusta y personaliza esta propuesta antes de cualquier interacción con el cliente.'"
}

## Reglas

- Todos los campos son obligatorios. Ninguno puede estar vacío ni ser null.
- `contexto_financiero`, `encaje_productos`, `argumentos_valor` y `proximos_pasos`:
  mínimo 2 elementos cada uno.
- Usa nombres genéricos de productos bancarios (sin marcas de terceros).
- Si falta algún dato, usa una hipótesis prudente y declarativa que mantenga
  la narrativa accionable.
- Evita "desconocido", "información no encontrada" o "información insuficiente".
- `narrativa_markdown` debe terminar SIEMPRE con la frase indicada sobre revisión
  del equipo comercial.
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