"""
src/agents/kyc_screener/agent.py
===================================
KYC Screener Agent -- Agente 1 de 5 del pipeline KYC + Credit Risk Intelligence.

Cubre los pasos 1-2 del caso de uso: ingesta documental, validacion KYC
y screening de sanciones/PEP.
"""

import json

from azure_client import chat_completion
from logging_utils import get_logger
from src.agents.kyc_screener.screening import run_screening
from src.agents.kyc_screener.prompt import get_system_prompt

logger = get_logger("kyc")


def run_kyc_screener_agent(documents: list[dict], use_mock: bool = True) -> dict:
    """
    documents: lista de {"name": str, "text": str} con el expediente de la empresa.

    Devuelve:
        {
          "extracted_entities": {...},   <- dict raw del agente (se normaliza en el orchestrator)
          "kyc_results": [...],
          "screening_results": [...],
          "screening_resumen": "...",
          "screening_conclusion": "LIMPIO|ALERTA|NO_CONCLUYENTE"
        }
    """
    logger.info("=== [KYC Screener Agent] Inicio (%d documentos) ===", len(documents))

    system_prompt = get_system_prompt(
        extra=f"Numero de documentos del expediente: {len(documents)}"
    )

    docs_block = "\n\n".join(
        f"--- DOCUMENTO: {d['name']} ---\n{d['text'][:6000]}"
        for d in documents
    )

    user_msg = (
        "Analiza el siguiente expediente de onboarding y devuelve un JSON "
        "con los campos: extracted_entities, kyc_results.\n\n"
        f"{docs_block}"
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
        ],
        profile="gpt52",
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        logger.warning("[KYC Screener Agent] respuesta no-JSON, usando fallback")
        result = {
            "extracted_entities": [],
            "kyc_results": [],
            "error": "respuesta_no_json",
            "raw": content[:2000],
        }

    # Recopilar todos los nombres para el screening desde el raw del agente
    nombres_a_cribar = _collect_names_for_screening(result.get("extracted_entities"))

    logger.info("[KYC Screener Agent] screening sobre %d nombres: %s",
                len(nombres_a_cribar), nombres_a_cribar)

    # Ejecutar screening de sanciones/PEP
    screening_output = run_screening(nombres_a_cribar, use_mock=use_mock)

    result["screening_results"]    = screening_output["resultados"]
    result["screening_resumen"]    = screening_output["resumen"]
    result["screening_conclusion"] = screening_output["conclusion"]

    logger.info(
        "[KYC Screener Agent] %d reglas KYC, screening: %s (%d hits)",
        len(result.get("kyc_results", [])),
        screening_output["conclusion"],
        sum(len(r.get("hits", [])) for r in screening_output["resultados"]),
    )
    logger.info("=== [KYC Screener Agent] Fin ===")
    return result


def _collect_names_for_screening(extracted_entities) -> list[str]:
    """
    Extrae todos los nombres (empresa principal, titulares reales, administradores)
    para pasarlos al screening de sanciones/PEP.

    Soporta todos los formatos que puede devolver el agente:
      - dict con applicant, beneficial_owners, controllers (formato raw del agente)
      - lista de dicts con entidad.nombre_legal (formato normalizado)
    """
    names = set()

    if isinstance(extracted_entities, dict):
        # ── Formato raw del agente ──────────────────────────────────────
        # applicant
        applicant = extracted_entities.get("applicant") or {}
        if isinstance(applicant, dict):
            name = applicant.get("legal_name") or applicant.get("nombre_legal")
            if name:
                names.add(name.strip())

        # beneficial_owners
        for bo in (extracted_entities.get("beneficial_owners") or []):
            if isinstance(bo, str) and bo.strip():
                names.add(bo.strip())
            elif isinstance(bo, dict):
                name = bo.get("name") or bo.get("nombre")
                if name:
                    names.add(name.strip())

        # controllers / administradores
        for ctrl in (extracted_entities.get("controllers") or
                     extracted_entities.get("administradores") or []):
            if isinstance(ctrl, str) and ctrl.strip():
                names.add(ctrl.strip())
            elif isinstance(ctrl, dict):
                name = ctrl.get("name") or ctrl.get("nombre")
                if name:
                    names.add(name.strip())

        # ownership_and_control (formato alternativo)
        oac = extracted_entities.get("ownership_and_control") or {}
        if isinstance(oac, dict):
            for bo in (oac.get("beneficial_owners") or []):
                if isinstance(bo, dict):
                    name = bo.get("name") or bo.get("nombre")
                    if name:
                        names.add(name.strip())
            for ctrl in (oac.get("controllers") or []):
                if isinstance(ctrl, dict):
                    name = ctrl.get("name") or ctrl.get("nombre")
                    if name:
                        names.add(name.strip())

    elif isinstance(extracted_entities, list):
        # ── Formato normalizado (lista de docs) ────────────────────────
        for entity in extracted_entities:
            if not isinstance(entity, dict):
                continue
            # Formato lista normalizada: entidad.nombre_legal
            entidad = entity.get("entidad") or {}
            if isinstance(entidad, dict):
                name = entidad.get("nombre_legal") or entidad.get("nombre")
                if name:
                    names.add(name.strip())
            # Formato lista con titulares_reales y administradores dentro de entidad
            for tr in (entidad.get("titulares_reales") or []):
                if isinstance(tr, str) and tr.strip():
                    names.add(tr.strip())
                elif isinstance(tr, dict):
                    name = tr.get("nombre") or tr.get("name")
                    if name:
                        names.add(name.strip())
            for admin in (entidad.get("administradores") or []):
                if isinstance(admin, str) and admin.strip():
                    names.add(admin.strip())
                elif isinstance(admin, dict):
                    name = admin.get("nombre") or admin.get("name")
                    if name:
                        names.add(name.strip())

    return sorted(names)