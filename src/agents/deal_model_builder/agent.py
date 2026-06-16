"""
src/agents/deal_model_builder/agent.py
=========================================
Deal Model Builder Agent (opcional) -- Agente 3 de 5 del pipeline Corporate &
Deal Intelligence.

Vive en su propio paquete (deal_model_builder) para no colisionar con
src/agents/model_builder, que pertenece al pipeline KYC.

Si no hay earnings_summary, devuelve {"disponible": False, ...} y el pipeline
continua sin este agente (es opcional).

Skills: 3-statement-model, comps-analysis
"""

import json

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()

DEAL_MODEL_BUILDER_TASK_PROMPT = """Eres el "Model Builder Agent" (rol opcional)
dentro de un pipeline de Corporate & Deal Intelligence para un banco con
actividad comercial.

Recibiras el analisis de resultados financieros redactado por el Earnings
Reviewer Agent para una empresa objetivo (texto libre).

TAREA: extrae o estima (cuando el texto lo permita) los siguientes elementos:

1. indicadores_clave: lista de hasta 5 indicadores mencionados o inferibles
   (nombre + valor como string, p.ej. "+18%", "11% (desde 14%)").
2. tendencias_estructurales: lista de 2-4 frases cortas describiendo
   tendencias de fondo del negocio.
3. interpretacion: 2-3 frases de interpretacion de alto nivel sobre la
   situacion financiera y posibles necesidades de financiacion.

FORMATO DE SALIDA (JSON estricto, sin texto adicional, sin markdown fences):
{
  "indicadores_clave": [
    {"nombre": "...", "valor": "..."}
  ],
  "tendencias_estructurales": ["...", "..."],
  "interpretacion": "..."
}

REGLAS:
- No inventes cifras que no esten respaldadas por el texto de entrada.
- No tomes decisiones de inversion ni recomiendes productos concretos.
"""


def run_deal_model_builder_agent(company_name: str, earnings_summary: str) -> dict:
    """
    company_name: nombre de la empresa objetivo
    earnings_summary: texto del Earnings Reviewer Agent

    Devuelve dict con indicadores, tendencias e interpretacion.
    Si earnings_summary esta vacio, devuelve {"disponible": False, ...}.
    """
    logger.info("=== [Model Builder Agent - Deal] Inicio (empresa=%s) ===", company_name)

    if not earnings_summary or not earnings_summary.strip():
        logger.info("[Model Builder Agent - Deal] sin earnings_summary: agente omitido (opcional)")
        logger.info("=== [Model Builder Agent - Deal] Fin (omitido) ===")
        return {"disponible": False, "indicadores_clave": [], "tendencias_estructurales": [], "interpretacion": ""}

    base_prompt = load_agent_prompt("model-builder")
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Corporate & Deal Intelligence)\n"
        + DEAL_MODEL_BUILDER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["3-statement-model"])

    user_msg = f"Empresa objetivo: {company_name}\n\nAnalisis del Earnings Reviewer Agent:\n{earnings_summary}"

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        profile="gpt52",
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
        result["disponible"] = True
    except json.JSONDecodeError:
        logger.warning("[Model Builder Agent - Deal] respuesta no-JSON")
        result = {
            "disponible": False,
            "indicadores_clave": [],
            "tendencias_estructurales": [],
            "interpretacion": "",
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    logger.info("[Model Builder Agent - Deal] %d indicadores, %d tendencias",
                len(result.get("indicadores_clave", [])), len(result.get("tendencias_estructurales", [])))
    logger.info("=== [Model Builder Agent - Deal] Fin ===")
    return result