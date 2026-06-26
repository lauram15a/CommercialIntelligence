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

# ── Normalización de outputs ──────────────────────────────────────────────────
"""
Funciones de normalización del output del KYC Screener Agent
para que el result.json tenga el formato que espera run_detail.html.

Añadir estas funciones al kyc_orchestrator.py y llamarlas antes de
guardar result.json.
"""


def normalize_kyc_output(kyc_output: dict) -> dict:
    """
    Normaliza el output del KYC Screener Agent al formato que espera el template.

    Cambios:
    - kyc_results: convierte dict anidado -> lista plana de reglas
    - extracted_entities: convierte dict -> lista de documentos
    """
    normalized = dict(kyc_output)

    # ── 1. Normalizar kyc_results ──────────────────────────────────────────
    kr = kyc_output.get("kyc_results", {})

    if isinstance(kr, dict):
        rule_outcomes = (
            kr.get("rule_outcomes")
            or (kr.get("rules_engine") or {}).get("rule_outcomes", [])
            or []
        )

        STATUS_MAP = {
            "pass": "PASS", "partial": "WARN", "fail": "FAIL",
            "PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL",
            "n/a": "WARN",
        }

        rules_list = []
        for r in rule_outcomes:
            if not isinstance(r, dict):
                continue
            rules_list.append({
                "rule_id":  r.get("rule_id", ""),
                "name":     r.get("rule_text") or r.get("name") or r.get("rule_id", ""),
                "status":   STATUS_MAP.get(str(r.get("outcome", r.get("status", ""))).lower(), "WARN"),
                "evidence": r.get("evidence", ""),
            })

        normalized["kyc_results"] = rules_list

    # ── 2. Normalizar extracted_entities ──────────────────────────────────
    ee = kyc_output.get("extracted_entities", {})

    if isinstance(ee, dict):
        docs_list = []
        inventory = ee.get("documents_inventory", []) or []
        applicant = ee.get("applicant", {}) or {}
        applicant_name = applicant.get("legal_name", "")

        if inventory:
            for doc in inventory:
                ref  = doc.get("ref", "")
                tipo = doc.get("type", "otro")
                tipo_display = (
                    "Escritura / Ficha registral" if "formation" in tipo
                    else "Estados financieros"    if "financial"  in tipo
                    else tipo.replace("_", " ").capitalize()
                )
                docs_list.append({
                    "tipo_documento": tipo_display,
                    "entidad":        {"nombre_legal": applicant_name},
                    "observaciones":  ref,
                })
        else:
            if applicant_name:
                docs_list.append({
                    "tipo_documento": "Ficha identificativa",
                    "entidad":        {"nombre_legal": applicant_name},
                    "observaciones":  f"NIF: {applicant.get('nif_cif', applicant.get('nif', ''))}",
                })
            for bo in (ee.get("beneficial_owners") or []):
                if isinstance(bo, dict) and bo.get("name"):
                    docs_list.append({
                        "tipo_documento": "Titular real (UBO)",
                        "entidad":        {"nombre_legal": bo["name"]},
                        "observaciones":  f"{bo.get('ownership_pct', '')}% - {bo.get('nationality', bo.get('nationality_or_jurisdiction', ''))}",
                    })

        normalized["extracted_entities"] = docs_list

    return normalized


def normalize_modelo_financiero(modelo_financiero: dict) -> dict:
    """
    Normaliza el output del Model Builder Agent al formato que espera el template.

    Cambios:
    - convierte normalized_kyc_profile.financials_normalized.years[] -> periodos[]
    """
    if modelo_financiero.get("periodos"):
        return modelo_financiero

    normalized = dict(modelo_financiero)
    periodos = []

    # Intentar desde normalized_kyc_profile.financials_normalized.years
    profile   = modelo_financiero.get("normalized_kyc_profile") or {}
    fin_norm  = profile.get("financials_normalized") or {}      if isinstance(profile, dict) else {}
    years     = fin_norm.get("years") or []                     if isinstance(fin_norm, dict) else []

    # Fallback: financial_model.periods / years
    if not years:
        fin_model = modelo_financiero.get("financial_model") or {}
        years = (fin_model.get("periods") or fin_model.get("years") or []) if isinstance(fin_model, dict) else []

    for y in years:
        if not isinstance(y, dict):
            continue
        periodo = str(y.get("fiscal_year") or y.get("year") or y.get("period") or "")
        inc = y.get("income_statement") or {}
        bal = y.get("balance_sheet") or {}
        periodos.append({
            "periodo":            periodo,
            "ebitda":             inc.get("ebitda"),
            "deuda_financiera":   bal.get("net_financial_debt"),
            "activo_corriente":   bal.get("current_assets"),
            "pasivo_corriente":   bal.get("current_liabilities"),
            "gastos_financieros": inc.get("financial_expenses"),
        })

    normalized["periodos"] = periodos

    if not normalized.get("resumen"):
        notes = modelo_financiero.get("data_quality_notes")
        if isinstance(notes, dict):
            std = notes.get("standardization_applied") or []
            normalized["resumen"] = "; ".join(std[:2]) if std else ""
        elif isinstance(notes, list):
            normalized["resumen"] = "; ".join(notes[:2])
        else:
            normalized["resumen"] = ""

    if not normalized.get("audit_flags"):
        notes = modelo_financiero.get("data_quality_notes")
        if isinstance(notes, dict):
            normalized["audit_flags"] = notes.get("missing_fields") or []
        elif isinstance(notes, list):
            normalized["audit_flags"] = notes
        else:
            normalized["audit_flags"] = []

    return normalized


def normalize_valuation_output(valuation_output: dict) -> dict:
    """
    Normaliza el output del Valuation Reviewer Agent al formato que espera el template.

    Cambios:
    - construye ratios.ratios_por_periodo[] desde comparativa_modelo_vs_historial_bancario
    - extrae interpretacion desde conclusiones o comparativa
    """
    existing_ratios = valuation_output.get("ratios") or {}
    if isinstance(existing_ratios, dict) and existing_ratios.get("ratios_por_periodo"):
        return valuation_output

    normalized = dict(valuation_output)

    # ── Extraer ratios por periodo ─────────────────────────────────────────
    comparativa   = valuation_output.get("comparativa_modelo_vs_historial_bancario") or {}
    tendencias    = comparativa.get("tendencias_financieras_normalizadas") or {}
    apalancamiento = tendencias.get("apalancamiento_y_cobertura") or {}
    liquidez      = tendencias.get("liquidez_y_circulante") or {}

    debt_ebitda  = apalancamiento.get("net_debt_to_ebitda") or {}
    interest_cov = apalancamiento.get("interest_coverage_ebitda") or {}
    current_ratio = liquidez.get("current_ratio") or {}

    years = sorted([k for k in debt_ebitda.keys() if isinstance(k, str) and k.isdigit()])

    ratios_por_periodo = []
    for year in years:
        ratios_por_periodo.append({
            "periodo":             year,
            "debt_ebitda":         debt_ebitda.get(year),
            "liquidez_corriente":  current_ratio.get(year),
            "cobertura_intereses": interest_cov.get(year),
        })

    variacion = {}
    if len(ratios_por_periodo) >= 2:
        first = ratios_por_periodo[0]
        last  = ratios_por_periodo[-1]
        if first.get("debt_ebitda") and last.get("debt_ebitda"):
            delta = ((last["debt_ebitda"] - first["debt_ebitda"]) / first["debt_ebitda"]) * 100
            variacion["variacion_deuda_ebitda_pct"] = round(delta, 1)

    normalized["ratios"] = {
        "ratios_por_periodo": ratios_por_periodo,
        "variacion": variacion,
    }

    # ── Extraer interpretación ─────────────────────────────────────────────
    if not normalized.get("interpretacion"):
        conclusions = (
            valuation_output.get("conclusiones")
            or valuation_output.get("conclusions")
            or {}
        )
        if isinstance(conclusions, dict):
            normalized["interpretacion"] = (
                conclusions.get("credit_view")
                or conclusions.get("vista_credito")
                or conclusions.get("sintesis")
                or ""
            )
        elif isinstance(conclusions, str):
            normalized["interpretacion"] = conclusions

        if not normalized.get("interpretacion"):
            consistencia = comparativa.get("consistencia_general") or {}
            normalized["interpretacion"] = consistencia.get("comentario", "")

    return normalized

# ──────────────────────────────────────────────────────────────────────────────

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
        with open(bbdd_path, encoding="utf-8-sig") as f:
            bbdd = json.load(f)
        historial = bbdd.get("historial", {}) or {}
    else:
        historial = {}

    path = DATA_DIR / "historial.json"
    if not historial and path.exists():
        with open(path, encoding="utf-8-sig") as f:
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
        if not isinstance(d, dict):
            continue
        entidad = d.get("entidad", {}) or {}
        if not isinstance(entidad, dict):
            continue
        for owner in entidad.get("titulares_reales") or []:
            if isinstance(owner, str) and owner.strip():
                names.add(owner)
            elif isinstance(owner, dict):
                owner_name = owner.get("nombre")
                if isinstance(owner_name, str) and owner_name.strip():
                    names.add(owner_name)
        for admin in entidad.get("administradores") or []:
            if isinstance(admin, str) and admin.strip():
                names.add(admin)
            elif isinstance(admin, dict):
                admin_name = admin.get("nombre")
                if isinstance(admin_name, str) and admin_name.strip():
                    names.add(admin_name)
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
    kyc_output_raw = run_kyc_screener_agent(documents, use_mock_screening)
    _raw_extracted_entities = kyc_output_raw.get("extracted_entities", {})
    kyc_output = normalize_kyc_output(kyc_output_raw)
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

    related_names = _collect_related_names(kyc_output.get("extracted_entities", []) or [])

    logger.info("FASE 2/5: Model Builder Agent")
    _notify("model_builder", "started")
    modelo_financiero = run_model_builder_agent(_raw_extracted_entities or kyc_output.get("extracted_entities", []))
    modelo_financiero = normalize_modelo_financiero(modelo_financiero)
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
    valuation_output = normalize_valuation_output(valuation_output)
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