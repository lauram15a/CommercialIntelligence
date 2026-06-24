"""
kyc_orchestrator.py
=====================
Master Orchestrator del sistema multiagente KYC + Credit Risk Intelligence.

Outputs en: outputs/YYYYMMDDHHMMSS_KYC_<empresa>/
"""

import json
import re
import sys
import unicodedata
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.logging_utils import setup_run_logging
from src.agents.kyc_screener.agent import run_kyc_screener_agent
from src.agents.model_builder.agent import run_model_builder_agent
from src.agents.valuation_reviewer.agent import run_valuation_reviewer_agent
from src.agents.market_researcher.agent import run_market_researcher_agent
from src.agents.credit_risk_report.agent import run_credit_risk_report_agent

DATA_DIR = Path(__file__).resolve().parent / "data"


def _normalize_name(value: str) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^a-zA-Z0-9]+", "", normalized).lower()


def load_historial(entity_name: str) -> dict:
    bbdd_path = DATA_DIR / "bbdd.json"
    if bbdd_path.exists():
        with open(bbdd_path, encoding="utf-8") as f:
            bbdd = json.load(f)
        historial = bbdd.get("historial", {}) or {}
    else:
        historial = {}

    path = DATA_DIR / "historial.json"
    if not historial and path.exists():
        with open(path, encoding="utf-8") as f:
            historial = json.load(f)

    if not historial:
        return {}
    # Búsqueda exacta primero
    if entity_name in historial:
        return historial[entity_name]

    # Búsqueda robusta (mayúsculas/tildes/puntuación)
    needle = _normalize_name(entity_name)
    for key, value in historial.items():
        if _normalize_name(key) == needle:
            return value
    return {}


def _collect_related_names(extracted_entities: list[dict]) -> list[str]:
    names = set()
    for d in extracted_entities:
        entidad = d.get("entidad", {}) or {}
        for owner in entidad.get("titulares_reales") or []:
            names.add(owner)
        for admin in entidad.get("administradores") or []:
            names.add(admin)
    return sorted(names)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def run_multiagent_pipeline(
    entity_name: str,
    documents: list[dict],
    use_mock_screening: bool = False,
    use_mock_market_research: bool = False,
    step_callback=None,
) -> dict:
    """Ejecuta el sistema multiagente KYC + Credit Risk Intelligence completo.

    step_callback: callable(step_key: str, event: str) donde event es
                   'started' o 'completed'. Usado por la UI para actualizar
                   el Pipeline de agentes en tiempo real.
    """
    def _notify(step_key: str, event: str):
        if step_callback:
            try:
                step_callback(step_key, event)
            except Exception:  # noqa: BLE001
                pass

    run_id, logger, run_dir = setup_run_logging(
        use_case="kyc",
        entity=entity_name,
    )
    evidencias_agentes = []

    logger.info("================================================================")
    logger.info("INICIO PIPELINE KYC | run_id=%s | entidad=%s", run_id, entity_name)
    logger.info("Carpeta de outputs: %s", run_dir)
    logger.info("================================================================")

    logger.info("FASE 1/5: KYC Screener Agent")
    _notify("kyc_screener", "started")
    kyc_output = run_kyc_screener_agent(documents, use_mock_screening)
    _write_json(run_dir / "1_kyc_screener" / "output.json", kyc_output)
    evidencias_agentes.append({
        "tipo": "agente_kyc_screener",
        "id": "AGT-KYC-001",
        "agente": "KYC Screener Agent",
        "resultado": "OK",
        "descripcion": "Extraccion documental, reglas KYC y screening ejecutados.",
        "fuente": "Fuentes internas + screening local/operativo",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "1_kyc_screener/output.json",
        "nota": (
            f"Documentos procesados: {len(kyc_output.get('extracted_entities', []))}; "
            f"reglas evaluadas: {len(kyc_output.get('kyc_results', []))}; "
            f"sujetos screeneados: {len(kyc_output.get('screening_results', []))}."
        ),
    })
    _notify("kyc_screener", "completed")

    related_names = _collect_related_names(kyc_output["extracted_entities"])

    logger.info("FASE 2/5: Model Builder Agent")
    _notify("model_builder", "started")
    modelo_financiero = run_model_builder_agent(kyc_output["extracted_entities"])
    _write_json(run_dir / "2_model_builder" / "output.json", modelo_financiero)
    evidencias_agentes.append({
        "tipo": "agente_model_builder",
        "id": "AGT-KYC-002",
        "agente": "Model Builder Agent",
        "resultado": "OK" if not modelo_financiero.get("error") else "NO_CONCLUYENTE",
        "descripcion": "Normalizacion financiera multi-periodo y deteccion de audit flags.",
        "fuente": "Datos financieros extraidos del expediente",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "2_model_builder/output.json",
        "nota": (
            f"Periodos normalizados: {len(modelo_financiero.get('periodos', []))}; "
            f"audit_flags: {len(modelo_financiero.get('audit_flags', []))}."
        ),
    })
    _notify("model_builder", "completed")

    logger.info("FASE 3/5: Market Researcher Agent")
    _notify("market_researcher", "started")
    market_research_output = run_market_researcher_agent(
        entity_name, related_names, use_mock_market_research
    )
    _write_text(run_dir / "4_market_researcher" / "output.txt", market_research_output)

    evidencias = kyc_output.get("evidencias") or []
    evidencias.append({
        "tipo": "fuente_externa_noticias",
        "id": "MKT-001",
        "resultado": "OK" if (market_research_output or "").strip() else "NO_CONCLUYENTE",
        "descripcion": "Registro de señales externas para riesgo reputacional/legal.",
        "fuente": "Busqueda externa (local_db/fuentes_externas.json o fuente configurada)",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": f"Market Researcher Agent -> entidad={entity_name}",
        "nota": "La decision final requiere validacion manual de Cumplimiento y Riesgos.",
        "contenido_referencia": (market_research_output or "")[:900],
    })
    evidencias_agentes.append({
        "tipo": "agente_market_researcher",
        "id": "AGT-KYC-003",
        "agente": "Market Researcher Agent",
        "resultado": "OK" if (market_research_output or "").strip() else "NO_CONCLUYENTE",
        "descripcion": "Recopilacion y sintesis de señales externas reputacionales y legales.",
        "fuente": "fuentes_externas.json / agregador configurado",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "4_market_researcher/output.txt",
        "nota": "Hallazgos externos sujetos a verificacion manual de Cumplimiento y Riesgos.",
        "contenido_referencia": (market_research_output or "")[:900],
    })
    kyc_output["evidencias"] = evidencias

    _notify("market_researcher", "completed")

    logger.info("FASE 4/5: Valuation Reviewer Agent")
    _notify("valuation_reviewer", "started")
    historial        = load_historial(entity_name)
    valuation_output = run_valuation_reviewer_agent(modelo_financiero, historial)
    _write_json(run_dir / "3_valuation_reviewer" / "output.json", valuation_output)
    evidencias_agentes.append({
        "tipo": "agente_valuation_reviewer",
        "id": "AGT-KYC-004",
        "agente": "Valuation Reviewer Agent",
        "resultado": "OK",
        "descripcion": "Calculo de ratios y analisis de riesgo cruzado con historial del cliente.",
        "fuente": "Modelo financiero normalizado + historial interno",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "3_valuation_reviewer/output.json",
        "nota": (
            f"Ratios calculados para {len(valuation_output.get('ratios', {}).get('ratios_por_periodo', []))} periodos; "
            f"historial disponible: {'si' if bool(historial) else 'no'}."
        ),
    })
    _notify("valuation_reviewer", "completed")

    logger.info("FASE 5/5: Credit Risk Report Agent")
    _notify("credit_risk_report", "started")
    informe = run_credit_risk_report_agent(
        entity_name=entity_name,
        kyc_output=kyc_output,
        modelo_financiero=modelo_financiero,
        valuation_output=valuation_output,
        market_research_output=market_research_output,
    )
    _write_text(run_dir / "informe.md", informe)
    evidencias_agentes.append({
        "tipo": "agente_credit_risk_report",
        "id": "AGT-KYC-005",
        "agente": "Credit Risk Report Agent",
        "resultado": "OK" if (informe or "").strip() else "NO_CONCLUYENTE",
        "descripcion": "Sintesis integral para comite de riesgos con recomendaciones operativas.",
        "fuente": "Outputs de KYC Screener, Model Builder, Market Researcher y Valuation Reviewer",
        "fecha_extraccion": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "trazabilidad": "informe.md",
        "nota": "La decision final de riesgo corresponde al analista y al comite.",
        "contenido_referencia": (informe or "")[:900],
    })
    _notify("credit_risk_report", "completed")

    result = {
        "run_id":                run_id,
        "entity_name":           entity_name,
        "use_case":              "kyc",
        "kyc_output":            kyc_output,
        "modelo_financiero":     modelo_financiero,
        "valuation_output":      valuation_output,
        "market_research_output": market_research_output,
        "historial":             historial,
        "evidencias_agentes":    evidencias_agentes,
    }
    _write_json(run_dir / "result.json", result)

    logger.info("FIN PIPELINE KYC | run_id=%s | outputs en %s", run_id, run_dir)
    return {**result, "informe": informe}