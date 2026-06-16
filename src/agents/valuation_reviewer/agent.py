"""
agents/valuation_reviewer/agent.py
====================================
Valuation Reviewer Agent - Agente 3 de 5.
Cubre los pasos 4-5 del artículo (análisis de riesgo + cruce con histórico).

Recibe:
    - el modelo financiero normalizado del Model Builder Agent
    - el historial del cliente (operaciones anteriores, incidencias, impagos...)

Calcula ratios de riesgo de forma DETERMINISTA (Python) y luego pide a GPT-5
una interpretación cualitativa, en el estilo del ejemplo del artículo
("La empresa incrementó un 35% su deuda financiera mientras que el EBITDA
solo creció un 8%...").

Skills reutilizadas del repo (adaptadas de equity/PE a credit risk):
    - portfolio-monitoring -> metodología de seguimiento de variaciones/KPIs
                               en el tiempo, reutilizada aquí para comparar
                               ratios de riesgo entre periodos.
"""

from typing import Any

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()


def compute_financial_ratios(modelo_financiero: dict) -> dict[str, Any]:
    """
    Calcula ratios de riesgo a partir del modelo normalizado del Model Builder Agent.

    modelo_financiero: salida de run_model_builder_agent (espera "periodos": [...])
    """
    periodos = modelo_financiero.get("periodos", [])
    periodos = sorted(periodos, key=lambda p: str(p.get("periodo") or ""))

    ratios_por_periodo = []
    for fin in periodos:
        ebitda = fin.get("ebitda")
        deuda = fin.get("deuda_financiera")
        ac = fin.get("activo_corriente")
        pc = fin.get("pasivo_corriente")
        gastos_fin = fin.get("gastos_financieros")

        ratios = {"periodo": fin.get("periodo")}
        ratios["debt_ebitda"] = round(deuda / ebitda, 2) if deuda is not None and ebitda else None
        ratios["liquidez_corriente"] = round(ac / pc, 2) if ac is not None and pc else None
        ratios["cobertura_intereses"] = round(ebitda / gastos_fin, 2) if ebitda is not None and gastos_fin else None
        ratios["ebitda"] = ebitda
        ratios["deuda_financiera"] = deuda
        ratios["ingresos"] = fin.get("ingresos")
        ratios_por_periodo.append(ratios)

    variacion = {}
    if len(ratios_por_periodo) >= 2:
        prev, curr = ratios_por_periodo[-2], ratios_por_periodo[-1]
        for key in ("ebitda", "deuda_financiera", "ingresos"):
            if prev.get(key) and curr.get(key):
                variacion[f"variacion_{key}_pct"] = round(
                    (curr[key] - prev[key]) / prev[key] * 100, 1
                )

    return {"ratios_por_periodo": ratios_por_periodo, "variacion": variacion}


VALUATION_REVIEWER_TASK_PROMPT = """Eres el "Valuation Reviewer Agent" dentro de un
pipeline de KYC + Credit Risk Intelligence para un banco.

Recibirás:
1. Ratios financieros por periodo y su variación interanual (ya calculados).
2. El historial del cliente en el banco (operaciones anteriores, incidencias,
   impagos, productos contratados).

TAREA: redacta un análisis de riesgo de crédito (5-8 frases, en español, tono de
comité de riesgos) que:
- Describa la evolución del apalancamiento (Debt/EBITDA) y su interpretación
  (mejora/deterioro de la capacidad de repago).
- Comente la liquidez corriente y la cobertura de intereses.
- Relacione los hallazgos financieros con el historial (p.ej. si ya hubo impagos
  o incidencias, si esto es una operación recurrente, si hay productos previos
  que indiquen buen comportamiento transaccional).
- Sea cuantitativo: usa los porcentajes y ratios proporcionados.

REGLAS:
- No tomes ni sugieras una decisión de aprobación/denegación.
- Si faltan datos para algún ratio (valor None/null), indícalo como limitación
  del análisis en lugar de omitirlo silenciosamente.
"""


def interpret_financial_ratios(ratios: dict, historial: dict) -> str:
    base_prompt = load_agent_prompt("valuation-reviewer")
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Credit Risk Intelligence)\n"
        + VALUATION_REVIEWER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["portfolio-monitoring"])

    user_msg = f"Ratios financieros:\n{ratios}\n\nHistorial del cliente:\n{historial or 'Sin historial previo'}"

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        profile="gpt52",
        temperature=0.2,
    )
    return response.choices[0].message.content


def run_valuation_reviewer_agent(modelo_financiero: dict, historial: dict) -> dict:
    """
    Devuelve:
        {
          "ratios": {...},
          "interpretacion": "..."
        }
    """
    logger.info("=== [Valuation Reviewer Agent] Inicio ===")

    ratios = compute_financial_ratios(modelo_financiero)
    logger.info("[Valuation Reviewer Agent] ratios calculados para %d periodos", len(ratios["ratios_por_periodo"]))

    interpretacion = interpret_financial_ratios(ratios, historial)
    logger.info("[Valuation Reviewer Agent] interpretación generada (%d chars)", len(interpretacion))

    logger.info("=== [Valuation Reviewer Agent] Fin ===")
    return {"ratios": ratios, "interpretacion": interpretacion}