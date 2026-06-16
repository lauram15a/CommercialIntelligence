"""
agents/kyc_screener/agent.py
==============================
KYC Screener Agent - Agente 1 de 5 del sistema multiagente.
Cubre los pasos 1-2 del artículo (validación KYC).

Internamente orquesta tres sub-pasos (equivalentes a los subagentes
doc-reader / rules-engine / screening del cookbook original):

    1. doc_reader   -> extrae campos estructurados de cada documento
    2. kyc_rules     -> evalúa reglas KYC deterministas
    3. screening      -> sanciones / PEP / adverse media sobre cada parte

Devuelve un "KYC findings package" que consumen:
    - Model Builder Agent (datos_financieros de cada documento)
    - Credit Risk Report Agent (resultados KYC + screening)
"""

from datetime import date, datetime, timezone

from src.agents.kyc_screener.doc_reader import run_doc_reader
from src.agents.kyc_screener.screening import run_screening_tool
from src.logging_utils import get_logger

logger = get_logger()


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def evaluate_kyc_rules(extracted_entities: list[dict]) -> list[dict]:
    """Evalúa el conjunto de reglas KYC sobre los documentos extraídos."""
    results = []
    today = date.today()

    has_id_doc = any(d.get("tipo_documento") == "dni" for d in extracted_entities)
    results.append({
        "rule_id": "KYC-001",
        "name": "Documento de identidad presente",
        "status": "PASS" if has_id_doc else "FAIL",
        "evidence": "dni encontrado" if has_id_doc else "no se encontró ningún documento tipo 'dni'",
    })

    for d in extracted_entities:
        if d.get("tipo_documento") == "dni":
            fecha = _parse_date(d.get("fecha_documento"))
            if fecha:
                meses = (today.year - fecha.year) * 12 + (today.month - fecha.month)
                status = "WARN" if meses > 18 else "PASS"
                results.append({
                    "rule_id": "KYC-002",
                    "name": "Antigüedad documento de identidad",
                    "status": status,
                    "evidence": f"documento con fecha {fecha.isoformat()} ({meses} meses)",
                })

    nombres = {
        d["entidad"]["nombre_legal"]
        for d in extracted_entities
        if d.get("entidad", {}).get("nombre_legal")
    }
    results.append({
        "rule_id": "KYC-003",
        "name": "Consistencia de nombre legal entre documentos",
        "status": "PASS" if len(nombres) <= 1 else "FAIL",
        "evidence": f"nombres encontrados: {sorted(nombres)}",
    })

    has_beneficial_owner = any(
        d.get("entidad", {}).get("titulares_reales") for d in extracted_entities
    )
    results.append({
        "rule_id": "KYC-004",
        "name": "Titular real identificado",
        "status": "PASS" if has_beneficial_owner else "FAIL",
        "evidence": "titulares reales presentes" if has_beneficial_owner else "no se identifica titular real",
    })

    has_financials = any(
        d.get("tipo_documento") in ("balance", "pyg") for d in extracted_entities
    )
    results.append({
        "rule_id": "KYC-005",
        "name": "Información financiera presente",
        "status": "PASS" if has_financials else "FAIL",
        "evidence": "balance/PyG encontrado" if has_financials else "faltan estados financieros",
    })

    return results


def _collect_screening_subjects(extracted_entities: list[dict]) -> list[str]:
    names = set()
    for d in extracted_entities:
        entidad = d.get("entidad", {}) or {}
        if entidad.get("nombre_legal"):
            names.add(entidad["nombre_legal"])
        for owner in entidad.get("titulares_reales") or []:
            names.add(owner)
        for admin in entidad.get("administradores") or []:
            names.add(admin)
    return sorted(n for n in names if n)


def _build_evidencias(
    documents: list[dict],
    extracted_entities: list[dict],
    kyc_results: list[dict],
    screening_results: list[dict],
) -> list[dict]:
    now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    evidencias = []

    for idx, extracted in enumerate(extracted_entities, start=1):
        doc_name = documents[idx - 1].get("name", f"documento_{idx}.txt") if idx - 1 < len(documents) else f"documento_{idx}.txt"
        raw_text = documents[idx - 1].get("text", "") if idx - 1 < len(documents) else ""
        evidencias.append({
            "tipo": "fuente_interna_documental",
            "id": f"DOC-{idx:03d}",
            "resultado": "OK",
            "descripcion": (
                f"Extraccion estructurada de {doc_name} "
                f"(tipo detectado: {extracted.get('tipo_documento', 'desconocido')})."
            ),
            "fuente": "Repositorio documental interno (expediente KYC)",
            "fecha_extraccion": now_iso,
            "trazabilidad": f"KYC Screener/doc-reader -> {doc_name}",
            "nota": extracted.get("observaciones") or "",
            "contenido_referencia": raw_text[:600],
        })

    for rule in kyc_results:
        status = (rule.get("status") or "").upper()
        result_map = {"PASS": "OK", "WARN": "NO_CONCLUYENTE", "FAIL": "ALERTA"}
        evidencias.append({
            "tipo": "regla_kyc",
            "id": rule.get("rule_id", "KYC-UNK"),
            "resultado": result_map.get(status, "NO_CONCLUYENTE"),
            "descripcion": f"{rule.get('name', 'Regla KYC')} - {rule.get('evidence', '')}",
            "fuente": "Motor de reglas KYC interno",
            "fecha_extraccion": now_iso,
            "trazabilidad": "KYC Screener/evaluate_kyc_rules",
        })

    for idx, screening in enumerate(screening_results, start=1):
        hits = screening.get("hits", []) or []
        has_note = bool(screening.get("note"))
        resultado = "ALERTA" if hits else ("NO_CONCLUYENTE" if has_note else "OK")
        evidencias.append({
            "tipo": "screening_sanciones",
            "id": f"SCR-{idx:03d}",
            "resultado": resultado,
            "descripcion": (
                f"Screening de {screening.get('name', 'sujeto no identificado')} con "
                f"{len(hits)} coincidencia(s)."
            ),
            "fuente": screening.get("source", "screening"),
            "fecha_extraccion": now_iso,
            "trazabilidad": f"KYC Screener/screening_lookup -> {screening.get('name', '')}",
            "nota": screening.get("note", ""),
            "contenido_referencia": "\n".join(
                f"- {h.get('nombre', '')} | {h.get('tipo', '')} | {h.get('lista', '')} | confianza={h.get('confianza', '')}"
                for h in hits[:8]
            ),
        })

    return evidencias


def run_kyc_screener_agent(
    documents: list[dict],
    use_mock_screening: bool = True,
) -> dict:
    """
    Ejecuta el KYC Screener Agent completo.

    documents: lista de {"name": str, "text": str}

    Devuelve:
        {
          "extracted_entities": [...],
          "kyc_results": [...],
          "screening_results": [...],
        }
    """
    logger.info("=== [KYC Screener Agent] Inicio (%d documentos) ===", len(documents))

    extracted_entities = []
    for doc in documents:
        result = run_doc_reader(doc["text"], document_name=doc["name"])
        extracted_entities.append(result)

    kyc_results = evaluate_kyc_rules(extracted_entities)
    for r in kyc_results:
        logger.info("[KYC Screener Agent] regla %s [%s] %s", r["rule_id"], r["status"], r["name"])

    subjects = _collect_screening_subjects(extracted_entities)
    screening_results = []
    for name in subjects:
        res = run_screening_tool({"name": name}, use_mock=use_mock_screening)
        screening_results.append(res)

    evidencias = _build_evidencias(documents, extracted_entities, kyc_results, screening_results)

    logger.info("=== [KYC Screener Agent] Fin ===")
    return {
        "extracted_entities": extracted_entities,
        "kyc_results": kyc_results,
        "screening_results": screening_results,
        "evidencias": evidencias,
    }