"""
src/agents/opportunity_researcher/agent.py
=============================================
Opportunity Researcher Agent -- Agente 1 de 5 del pipeline Deal Intelligence.

Identifica y prioriza empresas con potencial de financiacion o asesoramiento
dentro de un sector concreto.
"""

import json
from pathlib import Path

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.opportunity_researcher.prompt import get_system_prompt

logger = get_logger("deal")

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


def run_opportunity_researcher_agent(
    sector: str,
    use_mock: bool = False,
    fuente: str = "interna",
    empresas_override: list[dict] | None = None,
) -> dict:
    """
    sector:             sector o zona a analizar
    fuente:             "interna" (bbdd.json) o "externa" (fuentes_externas.json)
    empresas_override:  lista de empresas ya filtradas (p.ej. por geografia)
    """
    logger.info("=== [Opportunity Researcher Agent] Inicio (sector=%s, fuente=%s) ===",
                sector, fuente)

    # Usar empresas pre-filtradas si las hay, si no cargar de la fuente correcta
    if empresas_override:
        empresas = empresas_override
    else:
        empresas = _load_empresas_sector(sector, fuente)

    from agents.opportunity_researcher.prompt import get_system_prompt
    system_prompt = get_system_prompt(
        extra=(
            f"Sector / zona a analizar: {sector}\n"
            f"Fuente de datos: {'base de datos interna del banco (clientes)' if fuente == 'interna' else 'fuentes externas publicas (no clientes)'}"
        )
    )

    user_msg = (
        f"Sector / zona: {sector}\n"
        f"Fuente: {fuente}\n\n"
        f"Empresas detectadas:\n"
        + json.dumps(empresas, ensure_ascii=False, indent=2)
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
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

    logger.info("[Opportunity Researcher Agent] %d oportunidades",
                len(result.get("oportunidades", [])))
    logger.info("=== [Opportunity Researcher Agent] Fin ===")
    return result


def _load_empresas_sector(sector: str, fuente: str = "interna") -> list[dict]:
    """Carga empresas de un sector desde la fuente correcta."""
    if fuente == "interna":
        bbdd_path = DATA_DIR / "bbdd.json"
        if not bbdd_path.exists():
            return []
        with open(bbdd_path, encoding="utf-8") as f:
            bbdd = json.load(f)
        empresas_deal = bbdd.get("empresas_deal", {})
        sector_lower  = sector.strip().lower()
        for key, val in empresas_deal.items():
            if key.strip().lower() == sector_lower:
                return val
        return []
    else:  # externa
        ext_path = DATA_DIR / "fuentes_externas.json"
        if not ext_path.exists():
            return []
        with open(ext_path, encoding="utf-8") as f:
            ext = json.load(f)
        sector_lower = sector.strip().lower()
        results = []
        for nombre, emp in ext.get("empresas", {}).items():
            perfil = emp.get("perfil_publico", {})
            if perfil.get("sector", "").strip().lower() == sector_lower:
                results.append({
                    "empresa":     nombre,
                    "descripcion": perfil.get("descripcion", ""),
                    "señal":       perfil.get("senal_mercado", ""),
                    "ingresos_estimados": None,
                    "empleados":   None,
                })
        return results

