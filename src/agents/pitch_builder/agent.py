"""
src/agents/pitch_builder/agent.py
====================================
Pitch Builder Agent -- Agente 5 de 5 del pipeline Deal Intelligence.

Genera la narrativa comercial en JSON + el pitchbook .pptx mediante
pptx_builder.py.
"""

import json
from pathlib import Path

from azure_client import chat_completion
from logging_utils import get_logger
from src.agents.pitch_builder.pptx_builder import build_pitch_deck
from src.agents.pitch_builder.prompt import get_system_prompt

logger = get_logger("deal")


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

    system_prompt = get_system_prompt(
        extra=(
            f"Empresa objetivo: {company_name}\n"
            f"Sector: {sector}"
        )
    )

    model_block = "Sin vision financiera adicional del Model Builder Agent (paso opcional no disponible)."
    if model_output and model_output.get("disponible"):
        model_block = json.dumps(model_output, ensure_ascii=False, indent=2)

    user_msg = (
        f"Empresa objetivo: {company_name}\n"
        f"Sector: {sector}\n"
        f"Motivo de la oportunidad: {opportunity_context.get('motivo', 'no especificado')} "
        f"(prioridad: {opportunity_context.get('prioridad', 'no especificada')})\n\n"
        f"Analisis de resultados financieros (Earnings Reviewer Agent):\n{earnings_summary}\n\n"
        f"Briefing de cliente (Meeting Preparer Agent):\n"
        + json.dumps(meeting_brief, ensure_ascii=False, indent=2)
        + f"\n\nVision financiera basica (Model Builder Agent):\n{model_block}"
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
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
            "titulo": f"Propuesta comercial - {company_name}",
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

    # Generar el pitchbook .pptx
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
        logger.warning("[Pitch Builder Agent] error generando pitchbook: %s", exc)
        result["pptx_path"] = None
        result["pptx_error"] = str(exc)

    logger.info("=== [Pitch Builder Agent] Fin ===")
    return result