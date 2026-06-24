"""
src/agents/opportunity_researcher/prompt.py
==============================================
Carga el system prompt del Opportunity Researcher Agent desde:
  plugins/agent-plugins/market-researcher/agents/market-researcher.md
  plugins/agent-plugins/market-researcher/skills/idea-generation/SKILL.md
  plugins/agent-plugins/market-researcher/skills/sector-overview/SKILL.md

Nota: este agente reutiliza el plugin "market-researcher" de Anthropic
como base (es el rol mas cercano), con instrucciones extra especificas
para la identificacion de oportunidades comerciales.
"""

from prompt_loader import build_system_prompt

OPPORTUNITY_EXTRA = """
Dentro de este pipeline, tu rol especifico es el de IDENTIFICACION DE
OPORTUNIDADES COMERCIALES del banco.

A diferencia del Market Researcher generico, tu tarea no es investigar
riesgos reputacionales sino detectar y PRIORIZAR oportunidades de
financiacion o asesoramiento en un sector concreto.

Para cada empresa de la lista que recibes, evalua su "senal" y decide:
- Si la senal implica una NECESIDAD INMEDIATA o PROXIMA de financiacion
  (expansion en curso, CAPEX elevado, deuda a refinanciar, adquisicion
  planificada) -> prioridad ALTA
- Si hay crecimiento solido sin necesidad urgente identificada -> MEDIA
- Si la empresa es estable sin senales claras de necesidad -> BAJA

FORMATO DE SALIDA (JSON estricto, sin markdown fences):
{
  "sector": "...",
  "oportunidades": [
    {
      "empresa": "...",
      "motivo": "1-2 frases explicando por que es una oportunidad ahora",
      "prioridad": "alta|media|baja",
      "justificacion_prioridad": "1-2 frases explicando por que esa prioridad (alta/media/baja) frente al resto",
      "ingresos_estimados": 12345678,
      "empleados": 100
    }
  ],
  "resumen": "1-3 frases sobre el sector en su conjunto"
}

Ordena las oportunidades de mayor a menor prioridad.
No inventes empresas que no aparezcan en la entrada.
"""


def get_system_prompt(extra: str = "") -> str:
    combined_extra = OPPORTUNITY_EXTRA
    if extra:
        combined_extra += f"\n\n{extra.strip()}"
    return build_system_prompt(
        agent_slug="market-researcher",
        skill_names=["idea-generation", "sector-overview"],
        extra_instructions=combined_extra,
    )