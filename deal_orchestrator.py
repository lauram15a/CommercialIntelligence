"""
deal_orchestrator.py
======================
Master Orchestrator del sistema multiagente Corporate & Deal Intelligence.

Outputs en: outputs/YYYYMMDDHHMMSS_DEAL_<sector|empresa|zona>/

Soporta tres modos de busqueda:
  - Por sector (fuente interna o externa)
  - Por empresa (detecta si es cliente; fuente segun resultado)
  - Por geografia (comunidad autonoma, fuente interna o externa)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from logging_utils import setup_run_logging
from agents.opportunity_researcher.agent import run_opportunity_researcher_agent
from agents.earnings_reviewer.agent import run_earnings_reviewer_agent
from agents.deal_model_builder.agent import run_deal_model_builder_agent
from agents.meeting_preparer.agent import run_meeting_preparer_agent
from agents.pitch_builder.agent import run_pitch_builder_agent

DATA_DIR = Path(__file__).resolve().parent / "data"


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _select_target_company(oportunidades: list[dict], company_name: str | None) -> dict:
    if not oportunidades:
        return {"empresa": company_name or "Empresa sin identificar",
                "motivo": "", "prioridad": "media"}
    if company_name:
        for op in oportunidades:
            if op.get("empresa", "").strip().lower() == company_name.strip().lower():
                return op
    return oportunidades[0]


def _load_datos_empresa(company_name: str, fuente: str) -> list[dict]:
    """
    Carga los datos financieros o de contexto de una empresa segun la fuente.

    fuente="interna"  -> lee bbdd.json (cliente del banco)
    fuente="externa"  -> lee fuentes_externas.json (no cliente)

    Devuelve lista de {"name": str, "text": str} lista para el Earnings Reviewer.
    """
    if fuente == "interna":
        bbdd_path = DATA_DIR / "bbdd.json"
        if not bbdd_path.exists():
            return []
        with open(bbdd_path, encoding="utf-8") as f:
            bbdd = json.load(f)
        empresas_kyc = bbdd.get("empresas_kyc", {})
        # Busqueda case-insensitive
        nombre_lower = company_name.strip().lower()
        empresa = None
        for key, val in empresas_kyc.items():
            if key.strip().lower() == nombre_lower:
                empresa = val
                break
        if not empresa:
            return []
        # Construir documento de texto con balances reales
        lines = [
            f"Empresa: {empresa.get('nombre_legal', company_name)}",
            f"Sector: {empresa.get('sector', 'No consta')}",
            f"Empleados: {empresa.get('empleados', 'No consta')}",
            "",
            "=== ESTADOS FINANCIEROS ===",
        ]
        for balance in empresa.get("balances", []):
            p = balance.get("periodo", "N/D")
            lines += [
                f"Periodo {p}:",
                f"  Ingresos: {balance.get('ingresos', 'N/D'):,} EUR" if isinstance(balance.get('ingresos'), (int, float)) else f"  Ingresos: N/D",
                f"  EBITDA: {balance.get('ebitda', 'N/D'):,} EUR" if isinstance(balance.get('ebitda'), (int, float)) else f"  EBITDA: N/D",
                f"  Deuda financiera: {balance.get('deuda_financiera', 'N/D'):,} EUR" if isinstance(balance.get('deuda_financiera'), (int, float)) else f"  Deuda financiera: N/D",
                f"  Patrimonio neto: {balance.get('patrimonio_neto', 'N/D'):,} EUR" if isinstance(balance.get('patrimonio_neto'), (int, float)) else f"  Patrimonio neto: N/D",
            ]
        # Cuentas detalladas si existen
        cuentas = empresa.get("cuentas_empresa", {})
        if cuentas.get("pyg"):
            lines.append("\n=== CUENTA DE RESULTADOS DETALLADA ===")
            for anyo, pyg in cuentas["pyg"].items():
                lines.append(f"Año {anyo}:")
                for k, v in pyg.items():
                    lines.append(f"  {k}: {v:,}" if isinstance(v, (int, float)) else f"  {k}: {v}")
        return [{"name": f"datos_internos_{company_name}.txt", "text": "\n".join(lines)}]

    else:  # fuente == "externa"
        ext_path = DATA_DIR / "fuentes_externas.json"
        if not ext_path.exists():
            return []
        with open(ext_path, encoding="utf-8") as f:
            ext = json.load(f)
        empresas_ext = ext.get("empresas", {})
        nombre_lower = company_name.strip().lower()
        empresa = None
        for key, val in empresas_ext.items():
            if key.strip().lower() == nombre_lower:
                empresa = val
                break
        if not empresa:
            return []
        # Construir documento con info externa
        perfil = empresa.get("perfil_publico", {})
        noticias = empresa.get("noticias", [])
        senales  = empresa.get("senales_externas", [])
        lines = [
            f"Empresa: {company_name}",
            f"Fuente: externa (fuentes publicas y prensa)",
            f"Sector: {perfil.get('sector', 'No consta')}",
            f"Descripcion: {perfil.get('descripcion', 'No consta')}",
            f"Senal de mercado: {perfil.get('senal_mercado', 'No consta')}",
            "",
            "=== NOTICIAS Y SENALES EXTERNAS ===",
        ]
        for n in noticias:
            lines += [
                f"Titulo: {n.get('titulo', '')}",
                f"Fuente: {n.get('fuente', '')} | Fecha: {n.get('fecha', '')}",
                f"Resumen: {n.get('resumen', '')}",
                "",
            ]
        for s in senales:
            lines.append(f"- {s}")
        riesgos = empresa.get("riesgos_sectoriales", [])
        if riesgos:
            lines.append("\n=== RIESGOS SECTORIALES ===")
            for r in riesgos:
                lines.append(f"- {r}")
        return [{"name": f"datos_externos_{company_name}.txt", "text": "\n".join(lines)}]


def run_deal_intelligence_pipeline(
    sector: str,
    company_name: str | None = None,
    financial_documents: list[dict] | None = None,
    fuente: str = "interna",
    geografia: str = "",
    empresas_geografia: list[dict] | None = None,
    use_mock: bool = False,
    step_callback=None,
) -> dict:
    """
    sector:              sector a analizar (puede estar vacio si hay empresa o geografia)
    company_name:        empresa objetivo (opcional)
    financial_documents: documentos adicionales del usuario (opcional)
    fuente:              "interna" (bbdd.json) o "externa" (fuentes_externas.json)
    geografia:           comunidad autonoma para busqueda geografica (opcional)
    empresas_geografia:  lista pre-filtrada por app.py si hay busqueda geografica
    """
    financial_documents  = financial_documents  or []
    empresas_geografia   = empresas_geografia   or []

    def _notify(step_key: str, event: str):
        if step_callback:
            try:
                step_callback(step_key, event)
            except Exception:
                pass

    # Etiqueta para la carpeta de outputs
    entity_label = (
        company_name or
        (f"Zona_{geografia}" if geografia else None) or
        sector or
        "sin_label"
    )
    run_id, logger, run_dir = setup_run_logging(
        use_case="deal",
        entity=entity_label,
    )

    logger.info("================================================================")
    logger.info("INICIO PIPELINE DEAL | run_id=%s | fuente=%s | sector=%s | empresa=%s | zona=%s",
                run_id, fuente, sector or "-", company_name or "-", geografia or "-")
    logger.info("================================================================")

    # ---- Paso 1: Opportunity Researcher ----
    logger.info("PASO 1/5: Opportunity Researcher Agent")
    _notify("opportunity_researcher", "started")

    # Si hay empresas pre-filtradas por geografia, usarlas directamente
    if empresas_geografia:
        opportunity_output = {
            "sector": sector or geografia,
            "oportunidades": [
                {
                    "empresa":   e.get("empresa", ""),
                    "motivo":    e.get("señal", e.get("descripcion", "")),
                    "prioridad": "media",
                    "ingresos_estimados": e.get("ingresos_estimados"),
                    "empleados": e.get("empleados"),
                }
                for e in empresas_geografia
            ],
            "resumen": f"Busqueda geografica en {geografia}. Fuente: {'interna' if fuente == 'interna' else 'externa'}.",
        }
        # Enriquecer con prioridades reales via LLM solo si hay mas de 1 empresa
        if len(empresas_geografia) > 1:
            opportunity_output = run_opportunity_researcher_agent(
                sector or geografia,
                use_mock=use_mock,
                empresas_override=empresas_geografia,
            )
    else:
        opportunity_output = run_opportunity_researcher_agent(
            sector or company_name or geografia,
            use_mock=use_mock,
            fuente=fuente,
        )

    _write_json(run_dir / "1_opportunity_researcher" / "output.json", opportunity_output)
    _notify("opportunity_researcher", "completed")

    oportunidades  = opportunity_output.get("oportunidades", [])
    target         = _select_target_company(oportunidades, company_name)
    target_company = target.get("empresa", company_name or "sin_empresa")
    logger.info("Empresa objetivo: %s (prioridad=%s)", target_company, target.get("prioridad"))

    # ---- Paso 2: Earnings Reviewer ----
    logger.info("PASO 2/5: Earnings Reviewer Agent (fuente=%s)", fuente)
    _notify("earnings_reviewer", "started")

    # Prioridad de datos: documentos del usuario > BBDD segun fuente > señal
    if not financial_documents:
        financial_documents = _load_datos_empresa(target_company, fuente)
        if financial_documents:
            logger.info("  -> datos cargados desde fuente %s para '%s'", fuente, target_company)
        else:
            financial_documents = [{
                "name": "senal_oportunidad.txt",
                "text": (
                    f"Empresa: {target_company}\n"
                    f"Sector: {sector or geografia or 'No especificado'}\n"
                    f"Fuente: {fuente}\n"
                    f"Senal detectada: {target.get('motivo', '')}\n"
                    f"Ingresos estimados: {target.get('ingresos_estimados', 'no disponible')}\n"
                    f"Empleados: {target.get('empleados', 'no disponible')}\n"
                ),
            }]
            logger.info("  -> empresa no encontrada en fuente %s, usando senal", fuente)

    earnings_summary = run_earnings_reviewer_agent(target_company, financial_documents)
    _write_text(run_dir / "2_earnings_reviewer" / "output.txt", earnings_summary)
    _notify("earnings_reviewer", "completed")

    # ---- Paso 3: Model Builder (opcional) ----
    logger.info("PASO 3/5: Model Builder Agent (opcional)")
    _notify("model_builder", "started")
    model_output = run_deal_model_builder_agent(target_company, earnings_summary)
    _write_json(run_dir / "3_model_builder" / "output.json", model_output)
    _notify("model_builder", "completed")

    # ---- Paso 4: Meeting Preparer ----
    logger.info("PASO 4/5: Meeting Preparer Agent")
    _notify("meeting_preparer", "started")

    # Enriquecer con historial si es cliente interno
    if fuente == "interna":
        historial = _load_historial_cliente(target_company)
        if historial:
            target["historial_banco"] = (
                f"Cliente desde {historial.get('cliente_desde', 'N/D')}. "
                f"Rating interno: {historial.get('rating_interno', 'N/D')}. "
                f"Operaciones activas: {len(historial.get('operaciones_activas', []))}. "
                f"Impagos: {historial.get('impagos', 0)}."
            )
            target["_historial_completo"] = historial
    else:
        historial = {}
        target["historial_banco"] = "Empresa no cliente del banco. Datos procedentes de fuentes externas."

    meeting_brief = run_meeting_preparer_agent(
        target_company, target, earnings_summary, model_output
    )
    _write_json(run_dir / "4_meeting_preparer" / "output.json", meeting_brief)
    _notify("meeting_preparer", "completed")

    # ---- Paso 5: Pitch Builder ----
    logger.info("PASO 5/5: Pitch Builder Agent")
    _notify("pitch_builder", "started")
    pitch_output = run_pitch_builder_agent(
        company_name=target_company,
        sector=sector or geografia or "No especificado",
        opportunity_context=target,
        earnings_summary=earnings_summary,
        meeting_brief=meeting_brief,
        model_output=model_output,
        run_dir=run_dir,
    )
    _write_json(run_dir / "5_pitch_builder" / "output.json", pitch_output)
    _notify("pitch_builder", "completed")

    propuesta_md = pitch_output.get("narrativa_markdown", "")
    _write_text(run_dir / "propuesta.md", propuesta_md)

    result = {
        "run_id":             run_id,
        "sector":             sector or geografia or "No especificado",
        "company_name":       target_company,
        "fuente":             fuente,
        "geografia":          geografia or None,
        "use_case":           "deal",
        "opportunity_output": opportunity_output,
        "earnings_summary":   earnings_summary,
        "model_output":       model_output,
        "meeting_brief":      meeting_brief,
        "pitch_output":       pitch_output,
        "historial":          historial if fuente == "interna" else {},
    }
    _write_json(run_dir / "result.json", result)

    logger.info("FIN PIPELINE DEAL | run_id=%s | outputs en %s", run_id, run_dir)
    return {**result, "propuesta_md": propuesta_md}


def _load_historial_cliente(company_name: str) -> dict:
    """Lee el historial bancario del cliente desde bbdd.json."""
    bbdd_path = DATA_DIR / "bbdd.json"
    if not bbdd_path.exists():
        return {}
    with open(bbdd_path, encoding="utf-8") as f:
        bbdd = json.load(f)
    historial = bbdd.get("historial", {})
    nombre_lower = company_name.strip().lower()
    for key, val in historial.items():
        if key.strip().lower() == nombre_lower:
            return val
    return {}