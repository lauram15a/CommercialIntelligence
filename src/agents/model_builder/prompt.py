"""
src/agents/deal_model_builder/prompt.py
==========================================
Carga el system prompt del Deal Model Builder Agent desde:
  plugins/agent-plugins/model-builder/agents/model-builder.md
  plugins/agent-plugins/model-builder/skills/3-statement-model/SKILL.md
  plugins/agent-plugins/model-builder/skills/comps-analysis/SKILL.md
"""

from prompt_loader import build_system_prompt

DEAL_MODEL_EXTRA = """
Dentro de este pipeline, tu rol es OPCIONAL. Recibes el análisis de
resultados financieros del Earnings Reviewer Agent (texto libre) y
debes extraer de él una visión financiera estructurada.

TAREA: extrae o estima (solo si el texto lo respalda) los siguientes
elementos.

## Formato de salida obligatorio (JSON estricto, sin markdown fences)

{
  "indicadores_clave": [
    {"nombre": "Nombre del indicador", "valor": "valor como string, p.ej. '+18%' o '3,7x'"}
  ],
  "tendencias_estructurales": [
    "Tendencia estructural 1 en 1 frase.",
    "Tendencia estructural 2 en 1 frase."
  ],
  "interpretacion": "2-3 frases de alto nivel sobre la situación financiera y posibles necesidades de financiación."
}

## Reglas

- `indicadores_clave`: hasta 5 indicadores. Si el texto no aporta datos cuantitativos,
  devuelve lista vacía `[]`. No inventes cifras.
- `tendencias_estructurales`: 2-4 frases. Si no hay información suficiente,
  describe las limitaciones de los datos de forma útil para el banker.
- `interpretacion` NUNCA debe estar vacía. Si los datos son escasos, indica
  la limitación y qué información adicional se necesitaría.
- No inventes cifras que no estén en el texto de entrada.
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