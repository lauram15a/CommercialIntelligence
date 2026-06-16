"""
src/agents/earnings_reviewer/agent.py
========================================
Earnings Reviewer Agent -- Agente 2 de 5 del pipeline Corporate & Deal
Intelligence.

Cubre el paso 2 (analisis de resultados financieros): revisa cuentas anuales,
resultados trimestrales o presentaciones corporativas de la empresa objetivo
e identifica tendencias clave.

Skills: earnings-analysis, audit-xls
"""

import json

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()

EARNINGS_REVIEWER_TASK_PROMPT = """Eres el "Earnings Reviewer Agent" dentro de un
pipeline de Corporate & Deal Intelligence para un banco con actividad comercial.

Tu tarea: a partir de los datos financieros aportados sobre una empresa
objetivo (ya extraidos como texto), identifica las TENDENCIAS clave de su
evolucion financiera reciente.

ENTRADA: nombre de la empresa + uno o varios bloques de texto con datos
financieros (pueden venir de distintos documentos y periodos).

TAREA: redacta un analisis en español (4-7 frases, tono de banca de
inversion/comercial) que cubra, cuando los datos lo permitan:
- Evolucion de ingresos (crecimiento/decrecimiento interanual, en %).
- Evolucion del margen operativo (mejora o compresion).
- Evolucion del CAPEX y su relacion con la estrategia de la empresa.
- Evolucion del endeudamiento, si hay datos.
- Cualquier otra tendencia relevante.

Cierra con una frase del tipo: "La compañia presenta [...],
lo que puede implicar [necesidad de financiacion / oportunidad, etc.]".

REGLAS:
- Se cuantitativo: usa los numeros y porcentajes presentes en los datos.
- Si faltan datos para alguna dimension, indicalo como limitacion.
- No tomes decisiones de inversion ni recomiendes productos concretos.
"""


def _has_prompt(agent_key: str) -> bool:
    try:
        from src.skill_loader import AGENT_PROMPTS  # type: ignore
        return agent_key in AGENT_PROMPTS
    except Exception:
        return False


def _fallback_prompt() -> str:
    return (
        "Eres un analista financiero senior de un banco con actividad de "
        "banca corporativa, especializado en revisar resultados financieros "
        "de empresas para identificar tendencias y necesidades potenciales."
    )


def run_earnings_reviewer_agent(company_name: str, financial_texts: list[dict]) -> str:
    """
    company_name: nombre de la empresa objetivo
    financial_texts: lista de {"name": str, "text": str}

    Devuelve un resumen en texto del analisis de resultados financieros.
    """
    logger.info("=== [Earnings Reviewer Agent] Inicio (empresa=%s, %d documentos) ===",
                company_name, len(financial_texts))

    base_prompt = load_agent_prompt("earnings-reviewer") if _has_prompt("earnings-reviewer") else _fallback_prompt()
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Corporate & Deal Intelligence)\n"
        + EARNINGS_REVIEWER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["audit-xls"])

    if financial_texts:
        docs_block = "\n\n".join(
            f"--- DOCUMENTO: {d['name']} ---\n{d['text'][:8000]}" for d in financial_texts
        )
    else:
        docs_block = "(No se ha aportado ningun documento financiero. Indica esta limitacion explicitamente.)"

    user_msg = f"Empresa objetivo: {company_name}\n\n{docs_block}"

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        profile="gpt52",
        temperature=0.2,
    )

    output = response.choices[0].message.content or ""
    logger.info("[Earnings Reviewer Agent] analisis generado (%d chars)", len(output))
    logger.info("=== [Earnings Reviewer Agent] Fin ===")
    return output