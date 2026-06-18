"""
src/agents/market_researcher/agent.py
========================================
Market Researcher Agent -- Agente 3 de 5 del pipeline KYC + Credit Risk Intelligence.

Busca senales externas: noticias, litigios y cambios societarios relevantes
sobre la empresa y sus partes vinculadas.
"""

import json
from pathlib import Path

from azure_client import chat_completion
from logging_utils import get_logger

from src.agents.market_researcher.prompt import get_system_prompt

logger = get_logger("kyc")

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


def run_market_researcher_agent(
    entity_name: str,
    related_names: list[str],
    use_mock: bool = True,
) -> str:
    """
    entity_name:    nombre de la empresa principal.
    related_names:  titulares reales y administradores identificados.
    use_mock:       si True, lee noticias desde bbdd.json en lugar de
                    fuentes externas reales.

    Devuelve texto markdown con el resumen de senales externas.
    """
    logger.info("=== [Market Researcher Agent] Inicio (empresa=%s) ===", entity_name)

    # Cargar noticias desde bbdd.json si existen
    noticias_text = _load_noticias(entity_name)

    system_prompt = get_system_prompt(
        extra=(
            f"Empresa analizada: {entity_name}\n"
            f"Partes vinculadas a revisar: {', '.join(related_names) if related_names else 'ninguna adicional'}"
        )
    )

    user_msg = (
        f"Empresa: {entity_name}\n"
        f"Partes vinculadas: {', '.join(related_names) if related_names else 'no identificadas'}\n\n"
        f"Noticias y senales disponibles en la base de datos interna:\n{noticias_text}\n\n"
        "Redacta un resumen en markdown de las senales externas relevantes para el analisis de riesgo."
    )

    response = chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg},
        ],
        profile="gpt52",
        temperature=0.2,
    )

    output = response.choices[0].message.content or ""
    logger.info("[Market Researcher Agent] resumen generado (%d chars)", len(output))
    logger.info("=== [Market Researcher Agent] Fin ===")
    return output


def _load_noticias(entity_name: str) -> str:
    """Carga noticias del bbdd.json para la empresa."""
    bbdd_path = DATA_DIR / "bbdd.json"
    if not bbdd_path.exists():
        return "No hay noticias disponibles en la base de datos interna."

    try:
        with open(bbdd_path, encoding="utf-8") as f:
            bbdd = json.load(f)
    except (json.JSONDecodeError, OSError):
        return "Error al leer la base de datos interna."

    noticias = bbdd.get("noticias", [])
    if not noticias:
        return "No hay noticias registradas en la base de datos interna."

    # Filtrar noticias de esta empresa
    entity_lower = entity_name.strip().lower()
    relevantes = [
        n for n in noticias
        if entity_lower in n.get("empresa", "").lower()
    ]

    if not relevantes:
        return f"No se han encontrado noticias especificas para '{entity_name}' en la base de datos interna."

    lines = [f"=== NOTICIAS INTERNAS: {entity_name} ==="]
    for n in relevantes:
        lines += [
            f"\nTitulo: {n['titulo']}",
            f"Fuente: {n['fuente']} | Fecha: {n['fecha']}",
            f"Resumen: {n['resumen']}",
        ]
    return "\n".join(lines)