"""
agents/credit_risk_report/agent.py
====================================
Credit Risk Report Agent - Agente 5 de 5.
Cubre los pasos 7-8 del artículo (generación del informe + recomendaciones).

Recibe los outputs de los otros 4 agentes:
    - KYC Screener Agent       -> extracted_entities, kyc_results, screening_results
    - Model Builder Agent       -> modelo_financiero
    - Valuation Reviewer Agent  -> ratios, interpretacion
    - Market Researcher Agent    -> señales externas (texto)

Y produce el informe final para el comité de riesgos, con la misma estructura
que el ejemplo del artículo (resumen ejecutivo, KYC, análisis financiero,
señales externas, recomendaciones).
"""

from src.azure_client import chat_completion
from src.skill_loader import load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()

CREDIT_RISK_REPORT_TASK_PROMPT = """Eres el "Credit Risk Report Agent" dentro de un
pipeline de KYC + Credit Risk Intelligence para un banco. Eres el último agente del
flujo: tu trabajo es SINTETIZAR los outputs de los otros 4 agentes en un informe
único para el comité de riesgos.

Recibes:
- Resultados del KYC Screener Agent (datos extraídos, reglas KYC, screening PEP/sanciones)
- Resultados del Model Builder Agent (modelo financiero normalizado, varios periodos)
- Resultados del Valuation Reviewer Agent (ratios de riesgo + interpretación + cruce histórico)
- Resultados del Market Researcher Agent (señales externas)

Genera un INFORME en español, en markdown, con esta estructura EXACTA:

# Informe de riesgo - [Nombre de la entidad]

## Resumen ejecutivo
(4-8 líneas: situación general, principales hallazgos KYC, financieros y externos)

## Validación KYC
- Lista cada regla con su estado (PASS/WARN/FAIL) y evidencia
- Si hay FAIL o WARN, explica la implicación

## Análisis financiero
- Resume el modelo financiero normalizado (periodos disponibles, audit_flags si los hay)
- Ratios clave (Debt/EBITDA, liquidez corriente, cobertura de intereses) y su evolución
- Incluye la interpretación del Valuation Reviewer Agent, ajustándola si es necesario

## Screening (sanciones / PEP / adverse media)
- Resultado por cada parte screeneada
- Si hay hits, indica el nivel de confianza y si requiere revisión manual

## Señales externas
- Resume el output del Market Researcher Agent
- Si no se encontró nada relevante, indícalo explícitamente

## Recomendaciones
- Lista de acciones sugeridas (documentación adicional, garantías, ajuste de
  importe/plazo, escalado al comité, etc.)
- SIEMPRE termina con: "Estas recomendaciones son propuestas; la decisión final
  corresponde al analista y al comité de riesgos."

REGLAS:
- No tomes ni sugieras una decisión de aprobación/denegación final.
- Sé concreto y cuantitativo cuando los datos lo permitan.
- Si algún agente no aportó información (p.ej. faltan datos financieros), dilo
  explícitamente en la sección correspondiente.
- Cada hallazgo relevante debe poder trazarse al agente/documento de origen
  (p.ej. "según KYC Screener Agent, documento X...").
"""


def run_credit_risk_report_agent(
    entity_name: str,
    kyc_output: dict,
    modelo_financiero: dict,
    valuation_output: dict,
    market_research_output: str,
) -> str:
    """Genera el informe final en markdown."""
    logger.info("=== [Credit Risk Report Agent] Inicio (entidad=%s) ===", entity_name)

    base_prompt = load_agent_prompt("kyc-screener")
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (rol: Credit Risk Report Agent)\n"
        + CREDIT_RISK_REPORT_TASK_PROMPT
    )

    user_msg = f"""ENTIDAD: {entity_name}

--- OUTPUT KYC SCREENER AGENT ---
Datos extraídos:
{kyc_output.get('extracted_entities')}

Resultados reglas KYC:
{kyc_output.get('kyc_results')}

Resultados screening:
{kyc_output.get('screening_results')}

--- OUTPUT MODEL BUILDER AGENT ---
{modelo_financiero}

--- OUTPUT VALUATION REVIEWER AGENT ---
Ratios:
{valuation_output.get('ratios')}

Interpretación:
{valuation_output.get('interpretacion')}

--- OUTPUT MARKET RESEARCHER AGENT ---
{market_research_output}
"""

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        profile="gpt52",
        temperature=0.2,
    )

    informe = response.choices[0].message.content
    logger.info("[Credit Risk Report Agent] informe generado (%d chars)", len(informe))
    logger.info("=== [Credit Risk Report Agent] Fin ===")
    return informe