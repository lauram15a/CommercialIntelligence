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
        with open(bbdd_path, encoding="utf-8-sig") as f:
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
                f"  Ingresos: {balance.get('ingresos', 'N/D'):,} EUR" if isinstance(balance.get('ingresos'), (int, float)) else f"  Ingresos: estimacion pendiente de reporte",
                f"  EBITDA: {balance.get('ebitda', 'N/D'):,} EUR" if isinstance(balance.get('ebitda'), (int, float)) else f"  EBITDA: estimacion pendiente de reporte",
                f"  Deuda financiera: {balance.get('deuda_financiera', 'N/D'):,} EUR" if isinstance(balance.get('deuda_financiera'), (int, float)) else f"  Deuda financiera: estimacion pendiente de reporte",
                f"  Patrimonio neto: {balance.get('patrimonio_neto', 'N/D'):,} EUR" if isinstance(balance.get('patrimonio_neto'), (int, float)) else f"  Patrimonio neto: estimacion pendiente de reporte",
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
        with open(ext_path, encoding="utf-8-sig") as f:
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
            f"Sector: {perfil.get('sector', 'Sector no reportado por la fuente')}",
            f"Descripcion: {perfil.get('descripcion', 'Descripcion corporativa en proceso de consolidacion')}",
            f"Senal de mercado: {perfil.get('senal_mercado', 'Senal sectorial en seguimiento')}",
            f"Ingresos estimados: {perfil.get('ingresos_estimados', 0):,} EUR" if isinstance(perfil.get('ingresos_estimados'), (int, float)) else "Ingresos estimados: rango medio sectorial",
            f"Empleados estimados: {perfil.get('empleados', 0)}" if isinstance(perfil.get('empleados'), (int, float)) else "Empleados estimados: plantilla en expansion",
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


def _build_inferred_financial_document(target_company: str, sector: str, target_context: dict) -> dict:
    ingresos = target_context.get("ingresos_estimados")
    if not isinstance(ingresos, (int, float)) or ingresos <= 0:
        ingresos = 12_000_000
    empleados = target_context.get("empleados") if isinstance(target_context.get("empleados"), (int, float)) else 80

    sector_norm = (sector or "").strip().lower()
    margin_map = {
        "tecnologia": 0.24,
        "energia": 0.22,
        "industrial": 0.17,
        "construccion": 0.11,
        "retail y distribucion": 0.09,
        "salud y farmacia": 0.19,
        "inmobiliario": 0.16,
        "agroindustria": 0.12,
    }
    leverage_map = {
        "tecnologia": 0.35,
        "energia": 0.62,
        "industrial": 0.50,
        "construccion": 0.58,
        "retail y distribucion": 0.42,
        "salud y farmacia": 0.37,
        "inmobiliario": 0.65,
        "agroindustria": 0.45,
    }
    ebitda_margin = margin_map.get(sector_norm, 0.15)
    debt_ratio = leverage_map.get(sector_norm, 0.45)

    ebitda = round(ingresos * ebitda_margin)
    deuda = round(ingresos * debt_ratio)
    capex = round(ingresos * (0.08 if sector_norm in {"energia", "industrial", "construccion"} else 0.05))
    crecimiento = 0.11 if sector_norm in {"tecnologia", "salud y farmacia", "energia"} else 0.07

    inferred = [
        f"Empresa: {target_company}",
        f"Sector: {sector or 'Sector transversal'}",
        "Fuente: inferencia operativa basada en senales de oportunidad y benchmark sectorial.",
        "",
        "=== ESTIMACION FINANCIERA OPERATIVA (BASE DE TRABAJO) ===",
        f"Ingresos estimados ttm: {ingresos:,.0f} EUR",
        f"EBITDA estimado: {ebitda:,.0f} EUR (margen {ebitda_margin*100:.1f}%)",
        f"CAPEX estimado: {capex:,.0f} EUR",
        f"Deuda financiera estimada: {deuda:,.0f} EUR",
        f"Plantilla estimada: {int(empleados)} empleados",
        f"Crecimiento anual de referencia: {crecimiento*100:.1f}%",
        "",
        "=== CONTEXTO COMERCIAL ===",
        f"Motivo principal: {target_context.get('motivo', 'Oportunidad detectada en pipeline sectorial.')}",
        f"Prioridad asignada: {target_context.get('prioridad', 'media')}",
        (
            "Hipotesis de trabajo: estructurar una propuesta de financiacion con foco en "
            "circulante, deuda de crecimiento y soluciones de cobertura segun perfil del sector."
        ),
    ]
    return {"name": f"inferencia_financiera_{target_company}.txt", "text": "\n".join(inferred)}


def _load_empresas_deal_internas() -> dict:
    bbdd_path = DATA_DIR / "bbdd.json"
    if not bbdd_path.exists():
        return {}
    with open(bbdd_path, encoding="utf-8-sig") as f:
        bbdd = json.load(f)
    empresas = bbdd.get("empresas_deal", {})
    return empresas if isinstance(empresas, dict) else {}


def _load_personas_fisicas() -> list[dict]:
    personas_path = DATA_DIR / "personas_fisicas.json"
    if not personas_path.exists():
        return []
    with open(personas_path, encoding="utf-8-sig") as f:
        data = json.load(f)
    personas = data.get("personas", [])
    return personas if isinstance(personas, list) else []


def _get_sector_empresa(company_name: str, fuente: str) -> str:
    nombre = (company_name or "").strip().lower()
    if not nombre:
        return ""

    if fuente == "interna":
        for sector, empresas in _load_empresas_deal_internas().items():
            for emp in empresas:
                if (emp.get("empresa", "").strip().lower() == nombre):
                    return sector
        # Fallback al maestro KYC si no estuviera en empresas_deal
        bbdd_path = DATA_DIR / "bbdd.json"
        if bbdd_path.exists():
            with open(bbdd_path, encoding="utf-8-sig") as f:
                bbdd = json.load(f)
            for key, val in (bbdd.get("empresas_kyc", {}) or {}).items():
                if key.strip().lower() == nombre:
                    return val.get("sector", "")
        return ""

    # fuente externa
    ext_path = DATA_DIR / "fuentes_externas.json"
    if not ext_path.exists():
        return ""
    with open(ext_path, encoding="utf-8-sig") as f:
        ext = json.load(f)
    for key, val in (ext.get("empresas", {}) or {}).items():
        if key.strip().lower() == nombre:
            return (val.get("perfil_publico", {}) or {}).get("sector", "")
    return ""


def _get_empresas_sector_para_oportunidades(sector: str, fuente: str) -> list[dict]:
    sector_norm = (sector or "").strip().lower()
    if not sector_norm:
        return []

    if fuente == "interna":
        for key, empresas in _load_empresas_deal_internas().items():
            if key.strip().lower() == sector_norm:
                return empresas if isinstance(empresas, list) else []
        return []

    ext_path = DATA_DIR / "fuentes_externas.json"
    if not ext_path.exists():
        return []
    with open(ext_path, encoding="utf-8-sig") as f:
        ext = json.load(f)
    results = []
    for nombre, emp in (ext.get("empresas", {}) or {}).items():
        perfil = emp.get("perfil_publico", {}) or {}
        if perfil.get("sector", "").strip().lower() == sector_norm:
            results.append({
                "empresa": nombre,
                "descripcion": perfil.get("descripcion", ""),
                "señal": perfil.get("senal_mercado", ""),
                "ingresos_estimados": perfil.get("ingresos_estimados"),
                "empleados": perfil.get("empleados"),
            })
    return results


def _build_company_specific_opportunities(company_name: str, fuente: str, analyst_notes: str = "") -> dict:
    if fuente == "interna":
        bbdd_path = DATA_DIR / "bbdd.json"
        empresa = {}
        historial = {}
        if bbdd_path.exists():
            with open(bbdd_path, encoding="utf-8-sig") as f:
                bbdd = json.load(f)
            for key, value in (bbdd.get("empresas_kyc", {}) or {}).items():
                if key.strip().lower() == company_name.strip().lower():
                    empresa = value
                    break
            for key, value in (bbdd.get("historial", {}) or {}).items():
                if key.strip().lower() == company_name.strip().lower():
                    historial = value
                    break

        sector = empresa.get("sector", "Corporativo")
        observaciones = empresa.get("observaciones", "")
        deuda = (((empresa.get("cuentas_empresa") or {}).get("detalle_deuda") or {}).get("vencimientos") or {})
        ops = [
            {
                "empresa": company_name,
                "motivo": "Refinanciacion y optimizacion de estructura de deuda con foco en los vencimientos proximos y el calendario de amortizacion.",
                "prioridad": "alta",
                "justificacion_prioridad": "Existe una conversacion inmediata de financiacion con capacidad de generar propuesta concreta y multproducto.",
            },
            {
                "empresa": company_name,
                "motivo": f"Refuerzo de circulante, trade finance y lineas operativas para acompanar crecimiento y expansion. {observaciones}".strip(),
                "prioridad": "media",
                "justificacion_prioridad": "La necesidad es relevante para sostener crecimiento, aunque normalmente se estructura despues de ordenar la deuda principal.",
            },
            {
                "empresa": company_name,
                "motivo": "Paquete de tesoreria, coberturas y vinculacion adicional para mejorar principalidad y rentabilidad relacional.",
                "prioridad": "media",
                "justificacion_prioridad": "La oportunidad comercial es clara, pero complementaria a las palancas de deuda y circulante.",
            },
        ]
        if historial.get("operaciones_activas"):
            ops[2]["prioridad"] = "alta"
            ops[2]["justificacion_prioridad"] = "La relacion activa permite una conversacion de share of wallet y cross-sell con alta probabilidad comercial."
        resumen = (
            f"Analisis focalizado en {company_name}. Se priorizan palancas sobre la propia empresa, "
            f"con foco en refinanciacion, circulante y vinculacion financiera asociada al sector {sector.lower()}."
        )
        if deuda:
            resumen += f" Vencimientos monitorizados: {', '.join(f'{k}: {v:,.0f} EUR' for k, v in deuda.items())}."
        if analyst_notes:
            resumen += f" Contexto gestor: {analyst_notes}"
        return {"sector": sector, "oportunidades": ops, "resumen": resumen}

    ext_path = DATA_DIR / "fuentes_externas.json"
    empresa = {}
    if ext_path.exists():
        with open(ext_path, encoding="utf-8-sig") as f:
            ext = json.load(f)
        for key, value in (ext.get("empresas", {}) or {}).items():
            if key.strip().lower() == company_name.strip().lower():
                empresa = value
                break
    perfil = empresa.get("perfil_publico", {}) or {}
    noticias = empresa.get("noticias", []) or []
    senales = empresa.get("senales_externas", []) or []
    sector = perfil.get("sector", "Mercado")
    ops = [
        {
            "empresa": company_name,
            "motivo": perfil.get("senal_mercado", senales[0] if senales else "Impulso comercial y de crecimiento detectado en fuentes externas."),
            "prioridad": "alta",
            "justificacion_prioridad": "Hay una senal publica concreta y accionable que permite preparar una aproximacion comercial inmediata.",
        },
        {
            "empresa": company_name,
            "motivo": "Financiacion de crecimiento, liquidez de acompasamiento y soluciones de estructuracion adaptadas al siguiente hito corporativo.",
            "prioridad": "media",
            "justificacion_prioridad": "Es una oportunidad natural derivada del crecimiento, aunque depende de validar calendario y profundidad de necesidad financiera.",
        },
        {
            "empresa": company_name,
            "motivo": f"Relacion de advisory y cobertura especializada apoyada en noticias recientes: {(noticias[0].get('titulo', '') if noticias else 'seguimiento sectorial activo')}.",
            "prioridad": "media",
            "justificacion_prioridad": "Aporta valor relacional y diferenciacion, pero suele materializarse tras la primera conversacion de financiacion.",
        },
    ]
    resumen = (
        f"Analisis focalizado en {company_name}. La identificacion de oportunidades se centra en distintas palancas sobre la misma compania "
        f"a partir de senales externas del sector {sector.lower()}."
    )
    if analyst_notes:
        resumen += f" Contexto gestor: {analyst_notes}"
    return {"sector": sector, "oportunidades": ops, "resumen": resumen}


def _find_personas_candidates(search_context: dict) -> list[dict]:
    personas = _load_personas_fisicas()
    mode = (search_context.get("search_mode") or "").strip().lower()
    segment = (search_context.get("person_segment") or "").strip().lower()
    client_type = (search_context.get("person_client_type") or "").strip().lower()
    name = (search_context.get("person_name") or "").strip().lower()
    nief = (search_context.get("person_nief") or "").strip().lower()
    geo_kind = (search_context.get("geografia_kind") or "territorial").strip().lower()
    geo_value = (search_context.get("geografia") or "").strip().lower()

    candidates = []
    for persona in personas:
        if segment and persona.get("segmento", "").strip().lower() != segment:
            continue
        if client_type == "cliente" and not persona.get("es_cliente"):
            continue
        if client_type == "no_cliente" and persona.get("es_cliente"):
            continue
        if mode == "persona":
            if nief and persona.get("nief", "").strip().lower() != nief:
                continue
            if name and persona.get("nombre", "").strip().lower() != name:
                continue
        if mode == "geografia":
            comparable = persona.get("territorial", "") if geo_kind == "territorial" else persona.get("oficina", "")
            if geo_value and comparable.strip().lower() != geo_value:
                continue
        candidates.append(persona)
    return candidates


def _build_person_opportunity_output(search_context: dict, analyst_notes: str = "") -> tuple[dict, dict | None]:
    candidates = _find_personas_candidates(search_context)
    mode = (search_context.get("search_mode") or "").strip().lower()
    segment = (search_context.get("person_segment") or "").strip().lower()
    geo_value = search_context.get("geografia") or ""
    geo_kind = search_context.get("geografia_kind") or "territorial"

    if not candidates:
        label = search_context.get("person_name") or search_context.get("person_nief") or segment or geo_value or "universo persona"
        return ({
            "sector": segment or geo_value or "personas fisicas",
            "oportunidades": [],
            "resumen": f"No se localizaron personas para el criterio {label}. Ajusta segmento, cliente o geografia para ampliar el universo.",
        }, None)

    if mode == "persona":
        persona = candidates[0]
        oportunidades = []
        for item in persona.get("oportunidades_base", []) or []:
            oportunidades.append({
                "empresa": persona.get("nombre", ""),
                "motivo": item.get("motivo", ""),
                "prioridad": item.get("prioridad", "media"),
                "justificacion_prioridad": item.get("justificacion_prioridad", ""),
                "ingresos_estimados": persona.get("ingresos_anuales_estimados"),
                "empleados": 1,
            })
        resumen = (
            f"Analisis focalizado en {persona.get('nombre', '')}, segmento {persona.get('segmento', '')}. "
            f"Se priorizan distintas oportunidades sobre la misma persona: liquidez, inversion, financiacion y vinculacion."
        )
        if analyst_notes:
            resumen += f" Contexto gestor: {analyst_notes}"
        return ({"sector": persona.get("segmento", "personas fisicas"), "oportunidades": oportunidades, "resumen": resumen}, persona)

    oportunidades = []
    for persona in candidates:
        principal = (persona.get("oportunidades_base") or [{}])[0]
        oportunidades.append({
            "empresa": persona.get("nombre", ""),
            "motivo": principal.get("motivo", persona.get("perfil", "")),
            "prioridad": principal.get("prioridad", "media"),
            "justificacion_prioridad": principal.get("justificacion_prioridad", "Priorizacion basada en senales comerciales y perfil del cliente."),
            "ingresos_estimados": persona.get("ingresos_anuales_estimados"),
            "empleados": 1,
        })

    priority_order = {"alta": 0, "media": 1, "baja": 2}
    oportunidades.sort(key=lambda item: (priority_order.get(item.get("prioridad", "media"), 1), -(item.get("ingresos_estimados") or 0)))
    resumen = (
        f"Universo de personas fisicas priorizado por {('segmento ' + segment) if mode == 'segmento' else (geo_kind + ' ' + geo_value)}. "
        "El ranking combina inmediatez comercial, capacidad economica y potencial de vinculacion."
    )
    if analyst_notes:
        resumen += f" Contexto gestor: {analyst_notes}"
    first_name = oportunidades[0].get("empresa", "") if oportunidades else ""
    first_persona = next((p for p in candidates if p.get("nombre") == first_name), None)
    return ({"sector": segment or geo_value or "personas fisicas", "oportunidades": oportunidades, "resumen": resumen}, first_persona)


def _build_person_financial_document(persona: dict) -> dict:
    productos = ", ".join(persona.get("productos_actuales", []) or []) or "sin productos activos declarados"
    senales = "\n".join(f"- {item}" for item in (persona.get("senales", []) or []))
    text = (
        f"Persona objetivo: {persona.get('nombre', '')}\n"
        f"NIF/NIE/F: {persona.get('nief', '')}\n"
        f"Segmento: {persona.get('segmento', '')}\n"
        f"Cliente actual del banco: {'si' if persona.get('es_cliente') else 'no'}\n"
        f"Territorial: {persona.get('territorial', '')}\n"
        f"Oficina: {persona.get('oficina', '')}\n"
        f"Perfil: {persona.get('perfil', '')}\n"
        f"Ingresos anuales estimados: {persona.get('ingresos_anuales_estimados', 0):,.0f} EUR\n"
        f"Ahorro liquido estimado: {persona.get('ahorro_liquido_estimado', 0):,.0f} EUR\n"
        f"Patrimonio invertible estimado: {persona.get('patrimonio_invertible_estimado', 0):,.0f} EUR\n"
        f"Productos actuales: {productos}\n\n"
        "=== SENALES COMERCIALES ===\n"
        f"{senales}\n"
    )
    return {"name": f"perfil_persona_{persona.get('nombre', 'persona')}.txt", "text": text}


def _build_person_history(persona: dict) -> dict:
    if not persona or not persona.get("es_cliente"):
        return {}
    return {
        "cliente_desde": "2021-01-01",
        "rating_interno": "Vinculacion alta",
        "impagos": 0,
        "segmento": persona.get("segmento", "").capitalize(),
        "gestor": persona.get("oficina", ""),
        "operaciones_activas": [
            {
                "tipo": "Relacion comercial activa",
                "importe_EUR": persona.get("patrimonio_invertible_estimado") or persona.get("ahorro_liquido_estimado"),
                "fecha_inicio": "2023-01-01",
                "vencimiento": "Revision anual",
                "al_corriente": True,
            }
        ],
        "notas_gestor": persona.get("perfil", ""),
    }


def run_deal_intelligence_pipeline(
    sector: str,
    company_name: str | None = None,
    financial_documents: list[dict] | None = None,
    fuente: str = "interna",
    geografia: str = "",
    empresas_geografia: list[dict] | None = None,
    analyst_notes: str = "",
    entity_family: str = "juridica",
    search_context: dict | None = None,
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
    search_context       = search_context or {}

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
    logger.info("INICIO PIPELINE DEAL | run_id=%s | familia=%s | fuente=%s | sector=%s | empresa=%s | zona=%s | notas=%s",
                run_id, entity_family, fuente, sector or "-", company_name or "-", geografia or "-",
                "si" if analyst_notes else "no")
    logger.info("================================================================")

    # ---- Paso 1: Opportunity Researcher ----
    logger.info("PASO 1/5: Opportunity Researcher Agent")
    _notify("opportunity_researcher", "started")

    persona_profile = None
    # Si hay empresas pre-filtradas por geografia, usarlas directamente
    if entity_family == "fisica":
        opportunity_output, persona_profile = _build_person_opportunity_output(search_context, analyst_notes)
    elif empresas_geografia:
        opportunity_output = {
            "sector": sector or geografia,
            "oportunidades": [
                {
                    "empresa":   e.get("empresa", ""),
                    "motivo":    e.get("señal", e.get("descripcion", "")),
                    "justificacion_prioridad": (
                        "Clasificada como media por pertenecer al universo geográfico "
                        "seleccionado; requiere validación comercial adicional."
                    ),
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
                analyst_notes=analyst_notes,
            )
    else:
        company_mode = bool(company_name and not sector and not geografia)
        if company_mode:
            opportunity_output = _build_company_specific_opportunities(company_name, fuente, analyst_notes)
        else:
            opportunity_output = run_opportunity_researcher_agent(
                sector or company_name or geografia,
                use_mock=use_mock,
                fuente=fuente,
                analyst_notes=analyst_notes,
            )

    # Compatibilidad: garantizar explicación de clasificación aunque el LLM
    # devuelva formato antiguo.
    for op in opportunity_output.get("oportunidades", []) or []:
        if not op.get("justificacion_prioridad"):
            op["justificacion_prioridad"] = (
                op.get("motivo")
                or "Prioridad asignada por señales de mercado y contexto sectorial."
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
        if entity_family == "fisica" and persona_profile:
            financial_documents = [_build_person_financial_document(persona_profile)]
            fuente = "interna" if persona_profile.get("es_cliente") else "externa"
        else:
            financial_documents = _load_datos_empresa(target_company, fuente)
        if financial_documents:
            logger.info("  -> datos cargados desde fuente %s para '%s'", fuente, target_company)
        else:
            financial_documents = [
                _build_inferred_financial_document(
                    target_company=target_company,
                    sector=sector or geografia or "",
                    target_context=target,
                )
            ]
            logger.info("  -> empresa no encontrada en fuente %s, usando inferencia sectorial enriquecida", fuente)

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
    if entity_family == "fisica":
        historial = _build_person_history(persona_profile or {})
        if historial:
            target["historial_banco"] = (
                f"Cliente particular del banco. Segmento {historial.get('segmento', 'N/D')}. "
                f"Oficina {historial.get('gestor', 'N/D')}."
            )
            target["_historial_completo"] = historial
        else:
            historial = {}
            target["historial_banco"] = "Prospecto no cliente. Analisis apoyado en perfil patrimonial y senales comerciales."
    elif fuente == "interna":
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
        "entity_family":      entity_family,
        "fuente":             fuente,
        "geografia":          geografia or None,
        "analyst_notes":      analyst_notes or None,
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
    with open(bbdd_path, encoding="utf-8-sig") as f:
        bbdd = json.load(f)
    historial = bbdd.get("historial", {})
    nombre_lower = company_name.strip().lower()
    for key, val in historial.items():
        if key.strip().lower() == nombre_lower:
            return val
    return {}