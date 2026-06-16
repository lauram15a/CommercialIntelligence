"""
deal_orchestrator.py
======================
Master Orchestrator del sistema multiagente Corporate & Deal Intelligence.

Outputs en: outputs/YYYYMMDDHHMMSS_DEAL_<sector>/
"""

import json
from pathlib import Path
from datetime import datetime, timezone

from src.logging_utils import setup_run_logging
from src.agents.opportunity_researcher.agent import run_opportunity_researcher_agent
from src.agents.earnings_reviewer.agent import run_earnings_reviewer_agent
from src.agents.deal_model_builder.agent import run_deal_model_builder_agent
from src.agents.meeting_preparer.agent import run_meeting_preparer_agent
from src.agents.pitch_builder.agent import run_pitch_builder_agent


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _select_target_company(oportunidades: list[dict], company_name: str | None) -> dict:
    """Selecciona la empresa objetivo: la pedida por el usuario o la de mayor prioridad."""
    if not oportunidades:
        return {"empresa": company_name or "Empresa sin identificar", "motivo": "", "prioridad": "media"}
    if company_name:
        for op in oportunidades:
            if op.get("empresa", "").strip().lower() == company_name.strip().lower():
                return op
    return oportunidades[0]


def run_deal_intelligence_pipeline(
    sector: str,
    company_name: str | None = None,
    financial_documents: list[dict] | None = None,
    use_mock: bool = False,
    step_callback=None,
) -> dict:
    """
    sector: sector a analizar (p.ej. "Industrial")
    company_name: empresa objetivo (opcional; si no, se usa la de mayor prioridad)
    financial_documents: lista de {"name": str, "text": str} (opcional)
    use_mock: usa fallback local explícito (compatibilidad)
    step_callback: callable(step_key: str, event: str) para actualizar la UI
    """
    financial_documents = financial_documents or []

    def _notify(step_key: str, event: str):
        if step_callback:
            try:
                step_callback(step_key, event)
            except Exception:  # noqa: BLE001
                pass

    # Crear run_dir desde el inicio usando el sector (conocido antes del paso 1)
    run_id, logger, run_dir = setup_run_logging(
        use_case="deal",
        entity=sector,
    )
    evidencias_agentes = []

    logger.info("================================================================")
    logger.info("INICIO PIPELINE DEAL INTELLIGENCE | run_id=%s | sector=%s", run_id, sector)
    logger.info("Carpeta de outputs: %s", run_dir)
    logger.info("================================================================")

    # ---- Paso 1: Opportunity Researcher ----
    logger.info("PASO 1/5: Opportunity Researcher Agent (sector=%s)", sector)
    _notify("opportunity_researcher", "started")
    opportunity_output = run_opportunity_researcher_agent(sector, use_mock=use_mock)
    _write_json(run_dir / "1_opportunity_researcher" / "output.json", opportunity_output)
    evidencias_agentes.append({
        "tipo": "agente_opportunity_researcher",
        "id": "AGT-DEAL-001",
        "agente": "Opportunity Researcher Agent",
        "resultado": "OK" if not opportunity_output.get("error") else "NO_CONCLUYENTE",
        "descripcion": "Identificacion y priorizacion de oportunidades por sector.",
        "fuente": "BBDD interna + criterios de priorizacion del agente",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "1_opportunity_researcher/output.json",
        "nota": f"Oportunidades evaluadas: {len(opportunity_output.get('oportunidades', []))}.",
    })
    _notify("opportunity_researcher", "completed")

    oportunidades  = opportunity_output.get("oportunidades", [])
    target         = _select_target_company(oportunidades, company_name)
    target_company = target.get("empresa", company_name or "sin_empresa")

    logger.info("Empresa objetivo: %s (prioridad=%s)", target_company, target.get("prioridad"))

    # ---- Paso 2: Earnings Reviewer ----
    logger.info("PASO 2/5: Earnings Reviewer Agent")
    _notify("earnings_reviewer", "started")
    if not financial_documents:
        financial_documents = [{
            "name": "senal_oportunidad.txt",
            "text": (
                f"Empresa: {target_company}\n"
                f"Sector: {sector}\n"
                f"Senal detectada: {target.get('motivo', '')}\n"
                f"Ingresos estimados: {target.get('ingresos_estimados', 'no disponible')}\n"
                f"Empleados: {target.get('empleados', 'no disponible')}\n"
            ),
        }]
    earnings_summary = run_earnings_reviewer_agent(target_company, financial_documents)
    _write_text(run_dir / "2_earnings_reviewer" / "output.txt", earnings_summary)
    evidencias_agentes.append({
        "tipo": "agente_earnings_reviewer",
        "id": "AGT-DEAL-002",
        "agente": "Earnings Reviewer Agent",
        "resultado": "OK" if (earnings_summary or "").strip() else "NO_CONCLUYENTE",
        "descripcion": "Analisis de resultados financieros y tendencias clave.",
        "fuente": "Documentacion financiera aportada + contexto de oportunidad",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "2_earnings_reviewer/output.txt",
        "nota": f"Documentos de entrada: {len(financial_documents)}.",
        "contenido_referencia": (earnings_summary or "")[:900],
    })
    _notify("earnings_reviewer", "completed")

    # ---- Paso 3: Model Builder (opcional) ----
    logger.info("PASO 3/5: Model Builder Agent (opcional)")
    _notify("model_builder", "started")
    model_output = run_deal_model_builder_agent(target_company, earnings_summary)
    _write_json(run_dir / "3_model_builder" / "output.json", model_output)
    evidencias_agentes.append({
        "tipo": "agente_model_builder_deal",
        "id": "AGT-DEAL-003",
        "agente": "Model Builder Agent (Deal)",
        "resultado": "OK" if model_output.get("disponible", False) else "NO_CONCLUYENTE",
        "descripcion": "Extraccion de indicadores y tendencias estructurales para soporte comercial.",
        "fuente": "Resumen de Earnings Reviewer",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "3_model_builder/output.json",
        "nota": "Paso opcional en el pipeline Deal.",
    })
    _notify("model_builder", "completed")

    # ---- Paso 4: Meeting Preparer ----
    logger.info("PASO 4/5: Meeting Preparer Agent")
    _notify("meeting_preparer", "started")
    meeting_brief = run_meeting_preparer_agent(target_company, target, earnings_summary, model_output)
    _write_json(run_dir / "4_meeting_preparer" / "output.json", meeting_brief)
    evidencias_agentes.append({
        "tipo": "agente_meeting_preparer",
        "id": "AGT-DEAL-004",
        "agente": "Meeting Preparer Agent",
        "resultado": "OK" if not meeting_brief.get("error") else "NO_CONCLUYENTE",
        "descripcion": "Generacion de briefing comercial: perfil, riesgos, necesidades y talking points.",
        "fuente": "Opportunity context + analisis financiero + modelo opcional",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "4_meeting_preparer/output.json",
    })
    _notify("meeting_preparer", "completed")

    # ---- Paso 5: Pitch Builder ----
    logger.info("PASO 5/5: Pitch Builder Agent")
    _notify("pitch_builder", "started")
    pitch_output = run_pitch_builder_agent(
        company_name=target_company,
        sector=sector,
        opportunity_context=target,
        earnings_summary=earnings_summary,
        meeting_brief=meeting_brief,
        model_output=model_output,
        run_dir=run_dir,
    )
    _write_json(run_dir / "5_pitch_builder" / "output.json", pitch_output)
    evidencias_agentes.append({
        "tipo": "agente_pitch_builder",
        "id": "AGT-DEAL-005",
        "agente": "Pitch Builder Agent",
        "resultado": "OK" if not pitch_output.get("error") else "NO_CONCLUYENTE",
        "descripcion": "Construccion de propuesta final y pitchbook para revision comercial.",
        "fuente": "Briefing de cliente + contexto de oportunidad + analisis financiero",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "5_pitch_builder/output.json",
        "nota": f"Pitchbook generado: {'si' if bool(pitch_output.get('pptx_path')) else 'no'}.",
        "contenido_referencia": (pitch_output.get("narrativa_markdown") or "")[:900],
    })
    _notify("pitch_builder", "completed")

    propuesta_md = pitch_output.get("narrativa_markdown", "")
    _write_text(run_dir / "propuesta.md", propuesta_md)

    result = {
        "run_id":             run_id,
        "sector":             sector,
        "company_name":       target_company,
        "use_case":           "deal",
        "opportunity_output": opportunity_output,
        "earnings_summary":   earnings_summary,
        "model_output":       model_output,
        "meeting_brief":      meeting_brief,
        "pitch_output":       pitch_output,
        "evidencias_agentes": evidencias_agentes,
    }
    _write_json(run_dir / "result.json", result)

    logger.info("FIN PIPELINE DEAL INTELLIGENCE | run_id=%s | outputs en %s", run_id, run_dir)
    return {**result, "propuesta_md": propuesta_md}