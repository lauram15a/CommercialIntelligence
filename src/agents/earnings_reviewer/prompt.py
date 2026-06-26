"""
src/agents/earnings_reviewer/prompt.py
=========================================
Carga el system prompt del Earnings Reviewer Agent desde:
  plugins/agent-plugins/earnings-reviewer/agents/earnings-reviewer.md
  plugins/agent-plugins/earnings-reviewer/skills/earnings-analysis/SKILL.md
  plugins/agent-plugins/earnings-reviewer/skills/audit-xls/SKILL.md
"""

from prompt_loader import build_system_prompt

EARNINGS_EXTRA = """
Dentro de este pipeline, tu rol especifico es analizar los resultados
financieros de una empresa objetivo identificada por el Opportunity
Researcher Agent, en el contexto de una oportunidad comercial..

Redacta un analisis en español de 4-7 frases con tono de banca de
inversion/comercial que cubra:
- Evolucion de ingresos (crecimiento interanual en %)
- Evolucion del margen operativo / EBITDA
- Evolucion del CAPEX y su relacion con la estrategia
- Evolucion del endeudamiento si hay datos
- Cualquier otra tendencia relevante

Cierra siempre con una frase interpretativa del tipo:
"La compania presenta [...], lo que puede implicar [necesidad / oportunidad]."

No tomes decisiones de inversion ni recomiendes productos concretos.
Si falta un dato puntual, completa con hipotesis razonable y explicita de forma breve
la base usada. Evita frases como "informacion insuficiente" o "informacion no encontrada".
"""


def get_system_prompt(extra: str = "") -> str:
    combined_extra = EARNINGS_EXTRA
    if extra:
        combined_extra += f"\n\n{extra.strip()}"
    return build_system_prompt(
        agent_slug="earnings-reviewer",
        skill_names=["earnings-analysis", "audit-xls"],
        extra_instructions=combined_extra,
    )