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
Funciones de normalización del output de los agentes KYC.
Soporta todos los formatos conocidos que el LLM puede generar.
"""



def _strip_md(text: str) -> str:
    """Elimina formato markdown no deseado: tachado (~~), bold (**), italic (*)."""
    if not isinstance(text, str):
        return text
    text = re.sub(r"~~(.+?)~~", r"\1", text)   # ~~tachado~~
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # **negrita** en interpretacion
    return text

def _get_val(obj):
    """Extrae número de {"value": X} o devuelve directamente si ya es número."""
    if obj is None:
        return None
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return obj.get("value") or obj.get("valor")
    return None


def _extract_year_series(d):
    """Devuelve {año: valor} para claves numéricas de 4 dígitos en un dict."""
    if not isinstance(d, dict):
        return {}
    return {k: v for k, v in d.items()
            if isinstance(k, str) and k.isdigit() and len(k) == 4
            and isinstance(v, (int, float))}


def normalize_kyc_output(kyc_output: dict) -> dict:
    """
    Normaliza el output del KYC Screener Agent.
    - kyc_results: dict anidado o lista vacía -> lista plana de reglas
    - extracted_entities: dict -> lista de documentos
    """
    normalized = dict(kyc_output)

    # ── 1. Normalizar kyc_results ──────────────────────────────────────────
    kr = kyc_output.get("kyc_results", [])
    STATUS_MAP = {
        "pass": "PASS", "partial": "WARN", "fail": "FAIL",
        "PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL", "n/a": "WARN",
    }

    if isinstance(kr, dict):
        rule_outcomes = (
            kr.get("rule_outcomes")
            or (kr.get("rules_engine") or {}).get("rule_outcomes", [])
            or []
        )
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
    elif isinstance(kr, list) and all(isinstance(r, dict) and "rule_id" in r for r in kr):
        # Ya es lista plana con rule_id — normalizar campos
        rules_list = []
        for r in kr:
            rules_list.append({
                "rule_id":  r.get("rule_id", ""),
                "name":     r.get("rule_text") or r.get("name") or r.get("rule_id", ""),
                "status":   STATUS_MAP.get(str(r.get("outcome", r.get("status", ""))).lower(), "WARN"),
                "evidence": r.get("evidence", ""),
            })
        normalized["kyc_results"] = rules_list
    # Si es lista vacía, queda como está

    # ── 2. Normalizar extracted_entities ──────────────────────────────────
    ee = kyc_output.get("extracted_entities")

    if isinstance(ee, dict):
        docs_list = []
        inventory     = ee.get("documents_inventory") or []
        applicant     = ee.get("applicant") or {}
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

    elif isinstance(ee, list) and ee and isinstance(ee[0], dict):
        # Ya es lista — asegurar que tiene los campos que espera el template
        fixed = []
        for doc in ee:
            tipo = doc.get("tipo_documento", doc.get("type", "documento"))
            entidad = doc.get("entidad") or {}
            nombre = entidad.get("nombre_legal", "") if isinstance(entidad, dict) else ""
            fixed.append({
                "tipo_documento": tipo,
                "entidad":        {"nombre_legal": nombre},
                "observaciones":  doc.get("observaciones", doc.get("ref", "")),
            })
        normalized["extracted_entities"] = fixed

    return normalized


def normalize_modelo_financiero(modelo_financiero: dict) -> dict:
    """
    Normaliza el output del Model Builder Agent.
    Soporta todos los formatos conocidos de salida del agente.
    """
    if modelo_financiero.get("periodos"):
        return modelo_financiero

    normalized = dict(modelo_financiero)
    periodos = []
    years = []

    # ── Formato A: financials_normalized.statements[] ─────────────────────
    # balance_sheet_selected (no balance_sheet), period_year (no fiscal_year)
    fn = modelo_financiero.get("financials_normalized") or {}
    if isinstance(fn, dict):
        years = fn.get("statements") or fn.get("periods") or fn.get("years") or []

    # ── Formato B: normalized_financials.periods[] ────────────────────────
    if not years:
        nf = modelo_financiero.get("normalized_financials") or {}
        if isinstance(nf, dict):
            years = nf.get("periods") or nf.get("statements") or nf.get("years") or []

    # ── Formato C: normalized_kyc_profile.financials_normalized.years[] ───
    if not years:
        profile  = modelo_financiero.get("normalized_kyc_profile") or {}
        fin_norm = profile.get("financials_normalized") or {} if isinstance(profile, dict) else {}
        years    = fin_norm.get("years") or [] if isinstance(fin_norm, dict) else []

    # ── Formato D: financial_model.periods ────────────────────────────────
    if not years:
        fin_model = modelo_financiero.get("financial_model") or {}
        years = fin_model.get("periods") or fin_model.get("years") or []

    for y in years:
        if not isinstance(y, dict):
            continue
        # period_year (Formato A) o fiscal_year (Formatos B/C) o year/period
        periodo = str(
            y.get("period_year") or y.get("fiscal_year")
            or y.get("year") or y.get("period") or ""
        )
        inc = y.get("income_statement") or {}
        # balance_sheet_selected (Formato A) o balance_sheet (Formatos B/C)
        bal = y.get("balance_sheet_selected") or y.get("balance_sheet") or {}

        periodos.append({
            "periodo":            periodo,
            "ebitda":             _get_val(inc.get("ebitda")),
            "deuda_financiera":   _get_val(bal.get("net_financial_debt")),
            "activo_corriente":   _get_val(bal.get("current_assets")),
            "pasivo_corriente":   _get_val(bal.get("current_liabilities")),
            "gastos_financieros": _get_val(inc.get("financial_expenses")),
        })

    normalized["periodos"] = periodos

    # resumen y audit_flags
    if not normalized.get("resumen"):
        notes = (modelo_financiero.get("data_quality_notes")
                 or modelo_financiero.get("data_quality")
                 or [])
        if isinstance(notes, dict):
            std = notes.get("standardization_applied") or notes.get("notes") or []
            normalized["resumen"] = ("; ".join(std[:2]) if isinstance(std, list)
                                     else str(std)[:200])
        elif isinstance(notes, list):
            # data_quality_flags es lista de dicts con "issue"
            issues = [n.get("issue", str(n)) for n in notes if isinstance(n, dict)]
            normalized["resumen"] = "; ".join(issues[:2]) if issues else ""
        else:
            normalized["resumen"] = ""

    if not normalized.get("audit_flags"):
        flags = modelo_financiero.get("data_quality_flags") or []
        if isinstance(flags, list):
            normalized["audit_flags"] = [
                f.get("issue", str(f)) for f in flags if isinstance(f, dict)
            ]
        else:
            normalized["audit_flags"] = []

    return normalized


def normalize_valuation_output(valuation_output: dict) -> dict:
    """
    Normaliza el output del Valuation Reviewer Agent.
    Soporta todos los formatos conocidos de salida del agente.
    """
    normalized = dict(valuation_output)

    # ── 1. Normalizar ratios_por_periodo ──────────────────────────────────
    existing = (valuation_output.get("ratios") or {}).get("ratios_por_periodo") or []

    if not existing:
        ratios_por_periodo = []
        debt_ebitda = current_ratio = interest_cov = {}

        # ── Formato nuevo: financial_model_vs_bank_history.credit_profile_snapshot
        fmvbh = valuation_output.get("financial_model_vs_bank_history") or {}
        cps   = fmvbh.get("credit_profile_snapshot") or {}
        lc    = cps.get("leverage_and_coverage") or {}
        liq   = cps.get("liquidity") or {}

        debt_ebitda   = _extract_year_series(lc.get("net_debt_to_ebitda") or {})
        current_ratio = _extract_year_series(liq.get("current_ratio") or {})
        interest_cov  = _extract_year_series(lc.get("interest_coverage_ebitda") or {})

        # ── Formato anterior: resumen_financiero_normalizado
        if not debt_ebitda:
            rf  = valuation_output.get("resumen_financiero_normalizado") or {}
            ap  = rf.get("apalancamiento") or {}
            bl  = rf.get("balance_y_liquidez") or {}
            cr_stmt = rf.get("cuenta_resultados") or {}
            debt_ebitda   = _extract_year_series(ap.get("net_debt_to_ebitda") or {})
            current_ratio = _extract_year_series(bl.get("current_ratio") or {})
            interest_cov  = _extract_year_series(
                cr_stmt.get("cobertura_intereses_ebitda")
                or cr_stmt.get("interest_coverage_ebitda")
                or ap.get("interest_coverage_ebitda") or {}
            )

        # ── Formato anterior: comparativa_modelo_vs_historial_bancario
        if not debt_ebitda:
            comp = valuation_output.get("comparativa_modelo_vs_historial_bancario") or {}
            tend = comp.get("tendencias_financieras_normalizadas") or {}
            apal = tend.get("apalancamiento_y_cobertura") or {}
            liqu = tend.get("liquidez_y_circulante") or {}
            debt_ebitda   = _extract_year_series(apal.get("net_debt_to_ebitda") or {})
            current_ratio = _extract_year_series((liqu.get("current_ratio") or {}))
            interest_cov  = _extract_year_series(apal.get("interest_coverage_ebitda") or {})

        years = sorted(set(
            list(debt_ebitda.keys())
            + list(current_ratio.keys())
            + list(interest_cov.keys())
        ))

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
                delta = ((last["debt_ebitda"] - first["debt_ebitda"])
                         / first["debt_ebitda"]) * 100
                variacion["variacion_deuda_ebitda_pct"] = round(delta, 1)

        normalized["ratios"] = {
            "ratios_por_periodo": ratios_por_periodo,
            "variacion": variacion,
        }

    # ── 2. Normalizar interpretacion ──────────────────────────────────────
    if not normalized.get("interpretacion"):
        # Formato nuevo: financial_model_vs_bank_history.overall_assessment.summary
        fmvbh = valuation_output.get("financial_model_vs_bank_history") or {}
        overall = fmvbh.get("overall_assessment") or {}
        if overall.get("summary"):
            normalized["interpretacion"] = _strip_md(overall["summary"])

        # Formato nuevo: indicadores_de_riesgo_y_flags
        if not normalized.get("interpretacion"):
            ind        = valuation_output.get("indicadores_de_riesgo_y_flags") or {}
            fortalezas = ind.get("fortalezas") or []
            alertas    = ind.get("alertas") or []
            if fortalezas or alertas:
                partes = []
                if fortalezas:
                    partes.append("Fortalezas: " + "; ".join(fortalezas[:3]))
                if alertas:
                    partes.append("Puntos de atención: " + "; ".join(alertas[:2]))
                normalized["interpretacion"] = _strip_md(" | ".join(partes))

        # Formatos anteriores
        if not normalized.get("interpretacion"):
            conclusions = (valuation_output.get("conclusiones")
                           or valuation_output.get("conclusions") or {})
            if isinstance(conclusions, dict):
                normalized["interpretacion"] = (
                    conclusions.get("credit_view")
                    or conclusions.get("vista_credito")
                    or conclusions.get("sintesis") or ""
                )
            elif isinstance(conclusions, str):
                normalized["interpretacion"] = conclusions

        if not normalized.get("interpretacion"):
            comp = valuation_output.get("comparativa_modelo_vs_historial_bancario") or {}
            cons = comp.get("consistencia_general") or {}
            normalized["interpretacion"] = cons.get("comentario", "")

    # Limpiar markdown no deseado de la interpretación
    if normalized.get("interpretacion"):
        normalized["interpretacion"] = _strip_md(normalized["interpretacion"])

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




def _extract_periodos_from_raw(raw_extracted: dict | list) -> list[dict]:
    """
    Extrae periodos financieros directamente del raw_extracted_entities
    sin pasar por el LLM, como fallback cuando el Model Builder devuelve
    periodos vacíos.

    Cubre todos los formatos conocidos de output del KYC Screener Agent.
    """
    periodos = []

    def _v(obj):
        """Extrae número de {"value": X} o devuelve el número directamente."""
        if isinstance(obj, (int, float)):
            return obj
        if isinstance(obj, dict):
            return obj.get("value") or obj.get("valor")
        return None

    def _parse_years(years_list):
        for y in years_list:
            if not isinstance(y, dict):
                continue
            periodo = str(
                y.get("fiscal_year") or y.get("period_year")
                or y.get("year") or y.get("period") or ""
            )
            if not periodo:
                continue
            inc = y.get("income_statement") or {}
            bal = (y.get("balance_sheet_selected") or y.get("balance_sheet")
                   or y.get("balance") or {})
            periodos.append({
                "periodo":            periodo,
                "ebitda":             _v(inc.get("ebitda")),
                "deuda_financiera":   _v(bal.get("net_financial_debt")),
                "activo_corriente":   _v(bal.get("current_assets")),
                "pasivo_corriente":   _v(bal.get("current_liabilities")),
                "gastos_financieros": _v(inc.get("financial_expenses")),
            })

    if isinstance(raw_extracted, dict):
        # Formato A: financials[] directamente
        financials = raw_extracted.get("financials") or []
        if financials and isinstance(financials, list):
            for f in financials:
                if not isinstance(f, dict):
                    continue
                yr = f.get("year") or f.get("fiscal_year") or f.get("periodo") or ""
                periodos.append({
                    "periodo":            str(yr),
                    "ebitda":             _v(f.get("ebitda_eur") or f.get("ebitda")),
                    "deuda_financiera":   _v(f.get("net_financial_debt_eur") or f.get("deuda_financiera")),
                    "activo_corriente":   _v(f.get("current_assets_eur") or f.get("activo_corriente")),
                    "pasivo_corriente":   _v(f.get("current_liabilities_eur") or f.get("pasivo_corriente")),
                    "gastos_financieros": _v(f.get("financial_expenses_eur") or f.get("gastos_financieros")),
                })

        # Formato B: financials_normalized.statements o .years
        if not periodos:
            fn = raw_extracted.get("financials_normalized") or {}
            if isinstance(fn, dict):
                _parse_years(fn.get("statements") or fn.get("years") or [])

        # Formato C: normalized_kyc_profile.financials_normalized.years
        if not periodos:
            profile = raw_extracted.get("normalized_kyc_profile") or {}
            fn2 = profile.get("financials_normalized") or {} if isinstance(profile, dict) else {}
            _parse_years(fn2.get("years") or [] if isinstance(fn2, dict) else [])

        # Formato D: normalized_financials.periods
        if not periodos:
            nf = raw_extracted.get("normalized_financials") or {}
            if isinstance(nf, dict):
                _parse_years(nf.get("periods") or nf.get("statements") or [])

    return periodos


def _load_periodos_from_bbdd(entity_name: str) -> list[dict]:
    """
    Fallback de último recurso: lee los balances directamente del bbdd.json
    cuando el Model Builder Agent no logra extraer periodos financieros.
    Los datos de bbdd.json son la fuente canónica y siempre están estructurados.
    """
    bbdd_path = DATA_DIR / "bbdd.json"
    if not bbdd_path.exists():
        return []
    try:
        with open(bbdd_path, encoding="utf-8-sig") as f:
            bbdd = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    # Búsqueda exacta primero, luego normalizada
    empresas_kyc = bbdd.get("empresas_kyc", {}) or {}
    empresa_data = empresas_kyc.get(entity_name)
    if not empresa_data:
        needle = _normalize_name(entity_name)
        for key, val in empresas_kyc.items():
            if _normalize_name(key) == needle:
                empresa_data = val
                break

    if not empresa_data:
        return []

    balances = empresa_data.get("balances") or []
    periodos = []
    for b in balances:
        if not isinstance(b, dict):
            continue
        periodos.append({
            "periodo":            str(b.get("periodo", "")),
            "ebitda":             b.get("ebitda"),
            "deuda_financiera":   b.get("deuda_financiera"),
            "activo_corriente":   b.get("activo_corriente"),
            "pasivo_corriente":   b.get("pasivo_corriente"),
            "gastos_financieros": b.get("gastos_financieros"),
        })
    return periodos

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
    _raw_extracted_entities = kyc_output_raw.get("extracted_entities") or {}
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
    modelo_financiero = run_model_builder_agent(_raw_extracted_entities or kyc_output.get("extracted_entities") or [])
    modelo_financiero = normalize_modelo_financiero(modelo_financiero)
    # Fallback 1: si el LLM no extrajo periodos, extraerlos del raw
    if not modelo_financiero.get("periodos") and _raw_extracted_entities:
        periodos_directos = _extract_periodos_from_raw(_raw_extracted_entities)
        if periodos_directos:
            modelo_financiero["periodos"] = periodos_directos
            logger.info("[Model Builder] periodos extraídos del raw: %d periodos", len(periodos_directos))
    # Fallback 2 (último recurso): leer balances directamente del bbdd.json
    if not modelo_financiero.get("periodos"):
        periodos_bbdd = _load_periodos_from_bbdd(entity_name)
        if periodos_bbdd:
            modelo_financiero["periodos"] = periodos_bbdd
            modelo_financiero["resumen"] = (
                modelo_financiero.get("resumen") or
                "Datos financieros cargados directamente desde base de datos interna."
            )
            logger.info("[Model Builder] periodos cargados de bbdd.json: %d periodos", len(periodos_bbdd))
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