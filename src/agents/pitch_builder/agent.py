"""
src/agents/pitch_builder/agent.py
====================================
Pitch Builder Agent -- Agente 5 de 5 del pipeline Deal Intelligence.

Genera la narrativa comercial en JSON + el pitchbook .pptx y .pdf.
"""

import json
from pathlib import Path

from azure_client import chat_completion
from logging_utils import get_logger
from agents.pitch_builder.pptx_builder import build_pitch_deck
from agents.pitch_builder.pdf_builder import build_pitch_pdf

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
    logger.info("=== [Pitch Builder Agent] Inicio (empresa=%s) ===", company_name)

    from agents.pitch_builder.prompt import get_system_prompt
    system_prompt = get_system_prompt(
        extra=(
            f"Empresa objetivo: {company_name}\n"
            f"Sector: {sector}"
        )
    )

    model_block = (
        "Vision financiera base construida con senales operativas del pipeline; "
        "complementar con due diligence comercial en la reunion."
    )
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

    # --- Generar .pptx ---
    pptx_dir = run_dir / "5_pitch_builder"
    pptx_dir.mkdir(parents=True, exist_ok=True)

    try:
        build_pitch_deck(
            output_path=pptx_dir / "pitchbook.pptx",
            company_name=company_name,
            sector=sector,
            pitch=result,
            meeting_brief=meeting_brief,
            model_output=model_output,
        )
        result["pptx_path"] = "5_pitch_builder/pitchbook.pptx"
        logger.info("[Pitch Builder Agent] .pptx generado")
    except Exception as exc:  # noqa: BLE001
        logger.warning("[Pitch Builder Agent] error .pptx: %s", exc)
        result["pptx_path"] = None
        result["pptx_error"] = str(exc)

    # --- Generar .pdf ---
    try:
        build_pitch_pdf(
            output_path=pptx_dir / "pitchbook.pdf",
            company_name=company_name,
            sector=sector,
            pitch=result,
            meeting_brief=meeting_brief,
            model_output=model_output,
        )
        result["pdf_path"] = "5_pitch_builder/pitchbook.pdf"
        logger.info("[Pitch Builder Agent] .pdf generado")
    except Exception as exc:  # noqa: BLE001
        logger.warning("[Pitch Builder Agent] error .pdf: %s", exc)
        result["pdf_path"] = None
        result["pdf_error"] = str(exc)

    logger.info("=== [Pitch Builder Agent] Fin ===")
    return result