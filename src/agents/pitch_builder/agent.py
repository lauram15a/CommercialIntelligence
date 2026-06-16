"""
src/agents/pitch_builder/agent.py
====================================
Pitch Builder Agent -- Agente 5 de 5 del pipeline Corporate & Deal
Intelligence.

Genera la narrativa comercial (markdown) y el pitchbook .pptx (via pptx_builder.py).

Skills: pitch-deck, comps-analysis
"""

import json
from pathlib import Path

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger
from src.agents.pitch_builder.pptx_builder import build_pitch_deck

logger = get_logger()

PITCH_BUILDER_TASK_PROMPT = """Eres el "Pitch Builder Agent" dentro de un
pipeline de Corporate & Deal Intelligence para un banco con actividad
comercial. Eres el ultimo agente del flujo.

Recibiras:
1. El nombre de la empresa objetivo, el sector y el motivo de la oportunidad.
2. El analisis de resultados financieros del Earnings Reviewer Agent.
3. El briefing del Meeting Preparer Agent.
4. (Opcional) La vision financiera basica del Model Builder Agent.

TAREA: redacta el contenido de una PROPUESTA COMERCIAL en formato JSON:

- titulo: titulo de la propuesta.
- subtitulo: 1 frase que resuma la oportunidad.
- oportunidad_detectada: 2-3 frases describiendo la oportunidad concreta.
- contexto_financiero: lista de 3-4 puntos con los datos financieros clave.
- encaje_productos: lista de 2-4 productos o servicios del banco que encajan
  (nombres genericos de producto de banca corporativa).
- comparables: lista de 2-3 empresas comparables del mismo sector.
- argumentos_valor: lista de 3-4 argumentos de venta.
- proximos_pasos: lista de 2-3 acciones concretas para el equipo comercial.
- narrativa_markdown: resumen ejecutivo de 3-5 parrafos en markdown.

FORMATO DE SALIDA (JSON estricto, sin texto adicional, sin markdown fences):
{
  "titulo": "...",
  "subtitulo": "...",
  "oportunidad_detectada": "...",
  "contexto_financiero": ["...", "..."],
  "encaje_productos": ["...", "..."],
  "comparables": ["...", "..."],
  "argumentos_valor": ["...", "..."],
  "proximos_pasos": ["...", "..."],
  "narrativa_markdown": "..."
}

REGLAS:
- No uses nombres de productos o marcas de competidores.
- Termina narrativa_markdown con: "El equipo comercial revisa, ajusta y
  personaliza esta propuesta antes de cualquier interaccion con el cliente."
"""


def _has_prompt(agent_key: str) -> bool:
    try:
        from src.skill_loader import AGENT_PROMPTS  # type: ignore
        return agent_key in AGENT_PROMPTS
    except Exception:
        return False


def _fallback_prompt() -> str:
    return (
        "Eres un analista de banca corporativa especializado en construir "
        "propuestas comerciales y pitchbooks claros, persuasivos y orientados a la accion."
    )


def run_pitch_builder_agent(
    company_name: str,
    sector: str,
    opportunity_context: dict,
    earnings_summary: str,
    meeting_brief: dict,
    model_output: dict | None,
    run_dir: Path,
) -> dict:
    """
    Genera la propuesta en JSON + pitchbook .pptx en run_dir/5_pitch_builder/.

    Devuelve el dict de la propuesta con campo "pptx_path" añadido.
    """
    logger.info("=== [Pitch Builder Agent] Inicio (empresa=%s) ===", company_name)

    base_prompt = load_agent_prompt("pitch-agent") if _has_prompt("pitch-agent") else _fallback_prompt()
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Corporate & Deal Intelligence)\n"
        + PITCH_BUILDER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["sector-overview"])

    model_block = "Sin vision financiera adicional del Model Builder Agent (paso opcional no disponible)."
    if model_output and model_output.get("disponible"):
        model_block = json.dumps(model_output, ensure_ascii=False, indent=2)

    user_msg = (
        f"Empresa objetivo: {company_name}\n"
        f"Sector: {sector}\n"
        f"Motivo de la oportunidad: {opportunity_context.get('motivo', 'no especificado')} "
        f"(prioridad: {opportunity_context.get('prioridad', 'no especificada')})\n\n"
        f"Analisis de resultados financieros (Earnings Reviewer Agent):\n{earnings_summary}\n\n"
        f"Briefing de cliente (Meeting Preparer Agent):\n{json.dumps(meeting_brief, ensure_ascii=False, indent=2)}\n\n"
        f"Vision financiera basica (Model Builder Agent):\n{model_block}"
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        profile="gpt52",
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        logger.warning("[Pitch Builder Agent] respuesta no-JSON")
        result = {
            "titulo": f"Propuesta comercial \u2014 {company_name}",
            "subtitulo": "",
            "oportunidad_detectada": "",
            "contexto_financiero": [],
            "encaje_productos": [],
            "comparables": [],
            "argumentos_valor": [],
            "proximos_pasos": [],
            "narrativa_markdown": content[:2000],
            "error": "respuesta_no_json",
        }

    # --- Generacion del pitchbook .pptx ---
    pptx_dir = run_dir / "5_pitch_builder"
    pptx_dir.mkdir(parents=True, exist_ok=True)
    pptx_path = pptx_dir / "pitchbook.pptx"

    try:
        build_pitch_deck(
            output_path=pptx_path,
            company_name=company_name,
            sector=sector,
            pitch=result,
            meeting_brief=meeting_brief,
            model_output=model_output,
        )
        result["pptx_path"] = "5_pitch_builder/pitchbook.pptx"
        logger.info("[Pitch Builder Agent] pitchbook generado en %s", pptx_path)
    except Exception as exc:  # noqa: BLE001
        logger.warning("[Pitch Builder Agent] error generando pitchbook .pptx: %s", exc)
        result["pptx_path"] = None
        result["pptx_error"] = str(exc)

    logger.info("=== [Pitch Builder Agent] Fin ===")
    return result