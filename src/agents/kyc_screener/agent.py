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
          "extracted_entities": [...],
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

    # Construir el mensaje con todos los documentos
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

    # Recopilar todos los nombres para el screening
    nombres_a_cribar = _collect_names_for_screening(result.get("extracted_entities", []))

    # Ejecutar screening de sanciones
    screening_output = run_screening(nombres_a_cribar, use_mock=use_mock)

    result["screening_results"]    = screening_output["resultados"]
    result["screening_resumen"]    = screening_output["resumen"]
    result["screening_conclusion"] = screening_output["conclusion"]

    logger.info(
        "[KYC Screener Agent] %d entidades, %d reglas KYC, screening: %s",
        len(result.get("extracted_entities", [])),
        len(result.get("kyc_results", [])),
        screening_output["conclusion"],
    )
    logger.info("=== [KYC Screener Agent] Fin ===")
    return result


def _collect_names_for_screening(extracted_entities: list[dict]) -> list[str]:
    """Extrae todos los nombres (empresa, titulares, admins) para el screening."""
    names = set()
    for entity in extracted_entities:
        entidad = entity.get("entidad", {}) or {}

        if entidad.get("nombre_legal"):
            names.add(entidad["nombre_legal"])

        for tr in entidad.get("titulares_reales", []) or []:
            if isinstance(tr, str):
                names.add(tr)
            elif isinstance(tr, dict) and tr.get("nombre"):
                names.add(tr["nombre"])

        for admin in entidad.get("administradores", []) or []:
            if isinstance(admin, str):
                names.add(admin)
            elif isinstance(admin, dict) and admin.get("nombre"):
                names.add(admin["nombre"])

    return sorted(names)