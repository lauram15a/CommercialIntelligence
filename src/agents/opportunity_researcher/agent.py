"""
src/agents/opportunity_researcher/agent.py
=============================================
Opportunity Researcher Agent -- Agente 1 de 5 del pipeline Corporate & Deal
Intelligence.

Cubre el paso 1 del caso de uso (identificacion de oportunidades): analiza un
sector y devuelve una lista priorizada de empresas con potencial de
financiacion o asesoramiento, junto con la señal que las hace relevantes.

Fuente de datos:
- mock_company_lookup: para desarrollo, lee data/empresas_mock.json.
- real_company_lookup: placeholder para el conector real (CRM interno,
  bases de datos financieras como S&P Global / LSEG, etc.).
"""

import json
from pathlib import Path

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


def local_company_lookup(sector: str) -> dict:
    bbdd_path = DATA_DIR / "bbdd.json"
    registros = {}
    if bbdd_path.exists():
        with open(bbdd_path, encoding="utf-8") as f:
            bbdd = json.load(f)
        registros = bbdd.get("empresas_deal", {}) or {}

    if not registros:
        path = DATA_DIR / "empresas_deal.json"
        if not path.exists():
            path = DATA_DIR / "empresas_mock.json"
        if not path.exists():
            return {"sector": sector, "empresas": [], "source": "local_db",
                    "note": "fichero de empresas no encontrado"}
        with open(path, encoding="utf-8") as f:
            registros = json.load(f)

    empresas = registros.get(sector)
    if empresas is None:
        empresas = next(iter(registros.values()), [])
    return {"sector": sector, "empresas": empresas, "source": "local_db"}


def real_company_lookup(sector: str) -> dict:
    return local_company_lookup(sector)


def run_company_lookup(sector: str, use_mock: bool = False) -> dict:
    logger.info("[Opportunity Researcher Agent] busqueda de empresas en sector '%s' (use_mock=%s)", sector, use_mock)
    result = local_company_lookup(sector) if use_mock else real_company_lookup(sector)
    logger.info("[Opportunity Researcher Agent] sector '%s' -> %d empresas encontradas",
                sector, len(result.get("empresas", [])))
    return result


OPPORTUNITY_RESEARCHER_TASK_PROMPT = """Eres el "Opportunity Researcher Agent" dentro de un
pipeline de Corporate & Deal Intelligence para un banco con actividad comercial.

Tu tarea: a partir de una lista de empresas de un sector concreto (con una breve
descripcion y una "señal" relevante de cada una -- expansion, crecimiento,
incremento de deuda, rondas de financiacion, etc.), identifica y PRIORIZA las
oportunidades de financiacion o asesoramiento mas interesantes para el banco.

ENTRADA: sector analizado + lista de empresas, cada una con "descripcion",
"señal", "ingresos_estimados" y "empleados".

TAREAS:
1. Para cada empresa, evalua si la señal sugiere una necesidad de financiacion,
   asesoramiento, optimizacion de estructura de capital, cobertura de riesgos, etc.
2. Asigna una prioridad: "alta", "media" o "baja".
3. Para cada empresa, redacta un "motivo" de 1-2 frases que explique por que
   es una oportunidad relevante ahora.
4. Ordena las empresas de mayor a menor prioridad.
5. Redacta un "resumen" de 1-3 frases sobre el sector en su conjunto.

FORMATO DE SALIDA (JSON estricto, sin texto adicional, sin markdown fences):
{
  "sector": "...",
  "oportunidades": [
    {
      "empresa": "...",
      "motivo": "...",
      "prioridad": "alta|media|baja",
      "ingresos_estimados": 12345678,
      "empleados": 100
    }
  ],
  "resumen": "..."
}

REGLAS:
- No inventes empresas que no aparezcan en la entrada.
- No tomes decisiones de inversion ni recomiendes productos concretos en esta
  fase: eso lo hace el Meeting Preparer Agent y el Pitch Builder Agent.
"""


def run_opportunity_researcher_agent(sector: str, use_mock: bool = False) -> dict:
    """
    sector: nombre del sector a analizar (p.ej. "Industrial")

    Devuelve:
        {
          "sector": "...",
          "oportunidades": [{"empresa", "motivo", "prioridad", ...}, ...],
          "resumen": "..."
        }
    """
    logger.info("=== [Opportunity Researcher Agent] Inicio (sector=%s) ===", sector)

    lookup = run_company_lookup(sector, use_mock=use_mock)

    base_prompt = load_agent_prompt("market-researcher")
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Corporate & Deal Intelligence)\n"
        + OPPORTUNITY_RESEARCHER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["sector-overview"])

    user_msg = (
        f"Sector: {lookup['sector']}\n\n"
        f"Empresas detectadas:\n{json.dumps(lookup['empresas'], ensure_ascii=False, indent=2)}"
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
        logger.warning("[Opportunity Researcher Agent] respuesta no-JSON")
        result = {
            "sector": sector,
            "oportunidades": [],
            "resumen": "",
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    logger.info("[Opportunity Researcher Agent] %d oportunidades identificadas para sector '%s'",
                len(result.get("oportunidades", [])), sector)
    logger.info("=== [Opportunity Researcher Agent] Fin ===")
    return result