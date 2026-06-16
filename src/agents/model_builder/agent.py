"""
agents/model_builder/agent.py
===============================
Model Builder Agent - Agente 2 de 5.
Cubre el paso 3 del artículo (extracción y normalización financiera).

Recibe los "extracted_entities" del KYC Screener Agent (que ya incluyen un campo
"datos_financieros" por documento, posiblemente en distintos formatos/periodos) y
construye un modelo financiero normalizado de varios periodos, listo para que el
Valuation Reviewer Agent calcule ratios.

Skills reutilizadas del repo (adaptadas a credit risk en vez de equity research):
    - clean-data-xls     -> normalización de datos tabulares heterogéneos
    - 3-statement-model  -> estructura estándar de balance / PyG / cash flow
    - audit-xls          -> checks de consistencia
"""

import json

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()

MODEL_BUILDER_TASK_PROMPT = """Eres el "Model Builder Agent" dentro de un pipeline de
KYC + Credit Risk Intelligence para un banco.

Tu tarea: a partir de los bloques "datos_financieros" extraídos de varios documentos
(balances, PyG, posiblemente de distintos años y con campos heterogéneos), construye
un MODELO FINANCIERO NORMALIZADO de varios periodos.

ENTRADA: una lista de objetos "datos_financieros" (uno por documento), cada uno con
campos como ebitda, deuda_financiera, activo_corriente, pasivo_corriente,
patrimonio_neto, ingresos, gastos_financieros, periodo. Algunos campos pueden ser null.

TAREAS:
1. Agrupa los datos por "periodo" (año). Si dos documentos aportan el mismo periodo,
   combina los campos no nulos (no dupliques periodos).
2. Ordena los periodos cronológicamente.
3. Aplica checks de consistencia básicos (estilo audit-xls):
   - Si activo_corriente y pasivo_corriente y patrimonio_neto están presentes,
     verifica si los valores son plausibles (sin negativos donde no debería haberlos).
   - Señala cualquier salto inexplicado >100% entre periodos consecutivos en
     cualquier magnitud, como posible error de extracción a revisar.
4. Indica explícitamente qué campos faltan para cada periodo (data_gaps).

FORMATO DE SALIDA (JSON estricto, sin texto adicional, sin markdown fences):
{
  "periodos": [
    {
      "periodo": "2024",
      "ebitda": 1100000,
      "deuda_financiera": 3000000,
      "activo_corriente": 2200000,
      "pasivo_corriente": 1700000,
      "patrimonio_neto": 1800000,
      "ingresos": 9000000,
      "gastos_financieros": 140000,
      "data_gaps": ["patrimonio_neto no informado en el documento original"]
    }
  ],
  "audit_flags": [
    "Salto del 200% en deuda_financiera entre 2023 y 2024: revisar extracción"
  ],
  "resumen": "1-2 frases describiendo qué periodos y magnitudes están disponibles"
}

No calcules ratios (Debt/EBITDA, liquidez, etc.) -- eso lo hace el Valuation Reviewer Agent.
Tu responsabilidad es exclusivamente normalizar y auditar la calidad del dato.
"""


def run_model_builder_agent(extracted_entities: list[dict]) -> dict:
    """
    extracted_entities: salida de KYC Screener Agent (lista de dicts con
                         "datos_financieros" entre otros campos)

    Devuelve el modelo financiero normalizado (dict).
    """
    logger.info("=== [Model Builder Agent] Inicio ===")

    base_prompt = load_agent_prompt("model-builder")
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Credit Risk Intelligence)\n"
        + MODEL_BUILDER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["clean-data-xls", "3-statement-model", "audit-xls"])

    datos_financieros = [
        d.get("datos_financieros")
        for d in extracted_entities
        if d.get("datos_financieros") and any(v is not None for k, v in d["datos_financieros"].items() if k != "periodo")
    ]

    logger.info("[Model Builder Agent] %d bloques de datos financieros recibidos", len(datos_financieros))

    user_msg = f"datos_financieros extraídos:\n{json.dumps(datos_financieros, ensure_ascii=False, indent=2)}"

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
    except json.JSONDecodeError:
        logger.warning("[Model Builder Agent] respuesta no-JSON")
        result = {"error": "respuesta_no_json", "raw": content[:2000]}

    logger.info(
        "[Model Builder Agent] %d periodos normalizados, %d audit_flags",
        len(result.get("periodos", [])), len(result.get("audit_flags", [])),
    )
    logger.info("=== [Model Builder Agent] Fin ===")
    return result