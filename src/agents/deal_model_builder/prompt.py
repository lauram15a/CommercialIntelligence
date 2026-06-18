"""
src/agents/deal_model_builder/prompt.py
==========================================
Carga el system prompt del Deal Model Builder Agent desde:
  plugins/agent-plugins/model-builder/agents/model-builder.md
  plugins/agent-plugins/model-builder/skills/3-statement-model/SKILL.md
  plugins/agent-plugins/model-builder/skills/comps-analysis/SKILL.md

Nota: reutiliza el plugin "model-builder" de Anthropic como base, con
instrucciones extra especificas para el pipeline Deal Intelligence
(extraccion de indicadores desde texto, no desde datos estructurados).
"""

from prompt_loader import build_system_prompt

DEAL_MODEL_EXTRA = """
Dentro de este pipeline, tu rol es OPCIONAL. Recibes el analisis de
resultados financieros del Earnings Reviewer Agent (texto libre) y
debes extraer de el una vision financiera estructurada.

TAREA: extrae o estima (solo si el texto lo respalda) los siguientes
elementos:

- indicadores_clave: lista de hasta 5 indicadores con nombre y valor
  como string (por ejemplo "+18%", "11% desde 14%", "3,7x")
- tendencias_estructurales: lista de 2-4 frases cortas de tendencias
  de fondo del negocio
- interpretacion: 2-3 frases de alto nivel sobre la situacion
  financiera y posibles necesidades de financiacion

FORMATO DE SALIDA (JSON estricto, sin markdown fences):
{
  "indicadores_clave": [{"nombre": "...", "valor": "..."}],
  "tendencias_estructurales": ["...", "..."],
  "interpretacion": "..."
}

No inventes cifras que no esten en el texto de entrada.
Si no hay suficiente informacion, devuelve listas vacias.
"""


def get_system_prompt(extra: str = "") -> str:
    combined_extra = DEAL_MODEL_EXTRA
    if extra:
        combined_extra += f"\n\n{extra.strip()}"
    return build_system_prompt(
        agent_slug="model-builder",
        skill_names=["3-statement-model", "comps-analysis"],
        extra_instructions=combined_extra,
    )