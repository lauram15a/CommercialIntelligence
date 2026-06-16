"""
agents/market_researcher/agent.py
===================================
Market Researcher Agent - Agente 4 de 5.
Cubre el paso 6 del artículo (búsqueda de señales externas: noticias, cambios
societarios, concursos, litigios, cambios de administradores).

En el repo original, el "Market Researcher" hace research sectorial para equity
research / pitch decks (sector-overview, competitive-analysis). Aquí se adapta
esa metodología de research a nivel de UNA EMPRESA concreta, con foco en señales
de riesgo reputacional/legal/societario en lugar de oportunidades de inversión.

Búsqueda externa:
- web_search_tool: define la tool de búsqueda como function-calling para GPT-5.
  Implementación real recomendada: Bing Search API / Bing Grounding (Azure AI
  Foundry) vía Managed Identity, o tu agregador de noticias interno.
- mock_news_lookup: para desarrollo, devuelve resultados desde
  data/noticias_mock.json sin llamadas externas.

No decide nada por sí mismo: solo incorpora información para el Credit Risk
Report Agent.
"""

import json
from pathlib import Path

from src.azure_client import chat_completion
from src.skill_loader import build_system_prompt, load_agent_prompt
from src.logging_utils import get_logger

logger = get_logger()

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


WEB_SEARCH_TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Busca noticias, litigios, cambios societarios o eventos relevantes "
            "sobre una empresa o sus administradores. Devuelve una lista de "
            "resultados con título, fuente, fecha y resumen."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Términos de búsqueda, p.ej. 'Empresa Ejemplo SL concurso acreedores'",
                }
            },
            "required": ["query"],
        },
    },
}


def local_news_lookup(query: str) -> dict:
    """
    Búsqueda en la fuente externa unificada data/fuentes_externas.json.
    Además de noticias, incorpora señales públicas (riesgos/cambios societarios)
    para simular resultados localizables por Deep Research.
    """
    registros = []

    # Fuente principal externa unificada (noticias + señales externas)
    path = DATA_DIR / "fuentes_externas.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            fuentes = json.load(f)

        for empresa, payload in (fuentes.get("empresas") or {}).items():
            for n in payload.get("noticias", []) or []:
                registros.append({
                    "empresa": empresa,
                    "titulo": n.get("titulo", ""),
                    "fuente": n.get("fuente", "fuente_externa"),
                    "fecha": n.get("fecha", ""),
                    "resumen": n.get("resumen", ""),
                    "tipo": "noticia",
                })

            riesgos_publicos = (payload.get("riesgos_publicos", []) or []) + (payload.get("riesgos_sectoriales", []) or [])
            for idx, riesgo in enumerate(riesgos_publicos, start=1):
                registros.append({
                    "empresa": empresa,
                    "titulo": f"Riesgo publico detectado #{idx}",
                    "fuente": "fuentes_externas.json",
                    "fecha": payload.get("ultima_actualizacion", ""),
                    "resumen": riesgo,
                    "tipo": "riesgo_publico",
                })

            for idx, cambio in enumerate(payload.get("cambios_societarios", []) or [], start=1):
                registros.append({
                    "empresa": empresa,
                    "titulo": f"Cambio societario relevante #{idx}",
                    "fuente": "fuentes_externas.json",
                    "fecha": payload.get("ultima_actualizacion", ""),
                    "resumen": cambio,
                    "tipo": "cambio_societario",
                })

            senales_mercado = (payload.get("senales_mercado", []) or []) + (payload.get("senales_externas", []) or [])
            for idx, senal in enumerate(senales_mercado, start=1):
                registros.append({
                    "empresa": empresa,
                    "titulo": f"Señal de mercado #{idx}",
                    "fuente": "fuentes_externas.json",
                    "fecha": payload.get("ultima_actualizacion", ""),
                    "resumen": senal,
                    "tipo": "senal_mercado",
                })

            for idx, hallazgo in enumerate(payload.get("litigios_y_regulatorio", []) or [], start=1):
                registros.append({
                    "empresa": empresa,
                    "titulo": f"Litigio o señal regulatoria #{idx}",
                    "fuente": "fuentes_externas.json",
                    "fecha": payload.get("ultima_actualizacion", ""),
                    "resumen": hallazgo,
                    "tipo": "litigio_regulatorio",
                })

    # Fallback a bbdd unificada
    if not registros:
        bbdd_path = DATA_DIR / "bbdd.json"
        if bbdd_path.exists():
            with open(bbdd_path, encoding="utf-8") as f:
                bbdd = json.load(f)
            registros = bbdd.get("noticias_empresas", []) or []

    if not registros:
        path = DATA_DIR / "noticias.json"
        if path.exists():
            with open(path, encoding="utf-8") as f:
                registros = json.load(f)

    if not registros:
        path = DATA_DIR / "noticias_empresas.json"
        if not path.exists():
            path = DATA_DIR / "noticias_mock.json"
        if not path.exists():
            return {"query": query, "resultados": [], "source": "local_db", "note": "fichero de noticias no encontrado"}
        with open(path, encoding="utf-8") as f:
            registros = json.load(f)

    query_lower = query.lower()
    resultados = [
        r for r in registros
        if any(token in (r.get("empresa", "") + " " + r.get("titulo", "") + " " + r.get("resumen", "")).lower()
               for token in query_lower.split())
    ]
    return {"query": query, "resultados": resultados, "source": "local_db"}


def real_web_search(query: str) -> dict:
    """
    Conector de búsqueda para entorno "real" de esta demo.
    Mientras no haya agregador externo, usa la BBDD local.
    """
    return local_news_lookup(query)


def run_web_search_tool(arguments: dict, use_mock: bool = False) -> dict:
    query = arguments.get("query", "")
    logger.info("[Market Researcher Agent] web_search: %s (use_mock=%s)", query, use_mock)
    if use_mock:
        result = local_news_lookup(query)
    else:
        result = real_web_search(query)
    logger.info("[Market Researcher Agent] web_search: %s -> %d resultados", query, len(result.get("resultados", [])))
    return result


MARKET_RESEARCHER_TASK_PROMPT = """Eres el "Market Researcher Agent" dentro de un
pipeline de KYC + Credit Risk Intelligence para un banco.

Tu tarea: investigar señales EXTERNAS sobre una empresa concreta (y, si se conocen,
sus administradores/titulares reales) que sean relevantes para el análisis de
riesgo de crédito:
- Noticias negativas o relevantes.
- Cambios societarios (fusiones, escisiones, cambios de administradores).
- Concursos de acreedores / preconcursos.
- Litigios públicos.
- Otros eventos relevantes (sanciones regulatorias, huelgas, pérdida de clientes clave).

Dispones de la tool "web_search" para buscar. Realiza entre 1 y 4 búsquedas como
máximo, combinando el nombre de la empresa con términos como "concurso acreedores",
"litigio", "noticias", nombres de administradores, etc.

Cuando termines, responde en español con un resumen breve (3-6 frases) de los
hallazgos relevantes. Si no se encuentra nada significativo, dilo explícitamente
("No se han encontrado señales externas relevantes en las fuentes consultadas").

REGLAS:
- No decidas ni opines sobre si la operación debe aprobarse: solo reporta hallazgos.
- Si una búsqueda no devuelve resultados, no lo presentes como ausencia de riesgo,
  sino como "no se encontró información en las fuentes consultadas".
"""


def run_market_researcher_agent(
    entity_name: str,
    related_names: list[str] | None = None,
    use_mock: bool = False,
    max_tool_calls: int = 4,
) -> str:
    """
    entity_name: nombre de la entidad principal
    related_names: administradores/titulares reales (opcional, ayuda a la búsqueda)

    Devuelve un resumen en texto de las señales externas encontradas.
    """
    logger.info("=== [Market Researcher Agent] Inicio (entidad=%s) ===", entity_name)

    base_prompt = load_agent_prompt("market-researcher")
    system_prompt = (
        base_prompt.strip()
        + "\n\n---\n# Tarea actual (Credit Risk Intelligence)\n"
        + MARKET_RESEARCHER_TASK_PROMPT
    )
    system_prompt = build_system_prompt(system_prompt, ["sector-overview"])

    related = ", ".join(related_names or [])
    user_msg = (
        f"Empresa: {entity_name}\n"
        f"Personas relacionadas (administradores/titulares): {related or 'no especificadas'}\n\n"
        f"Investiga señales externas relevantes para el análisis de riesgo de crédito."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]

    for _ in range(max_tool_calls + 1):
        response = chat_completion(
            messages=messages,
            profile="gpt52",
            tools=[WEB_SEARCH_TOOL_SPEC],
            temperature=0.1,
        )
        choice = response.choices[0]
        message = choice.message

        if not message.tool_calls:
            logger.info("=== [Market Researcher Agent] Fin ===")
            return message.content or ""

        messages.append(message.model_dump(exclude_unset=True))

        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            tool_result = run_web_search_tool(args, use_mock=use_mock)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, ensure_ascii=False),
            })

    response = chat_completion(messages=messages, profile="gpt52", temperature=0.1)
    logger.info("=== [Market Researcher Agent] Fin (límite de tool calls alcanzado) ===")
    return response.choices[0].message.content or ""