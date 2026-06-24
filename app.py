"""
app.py
Frontend Flask para la plataforma de agentes de IA del banco.

Rutas KYC:  /kyc/  /kyc/runs  /kyc/runs/<id>  /kyc/runs/<id>/progress
Rutas Deal: /deal/ /deal/runs /deal/runs/<id> /deal/runs/<id>/progress
            /deal/runs/<id>/pitchbook.pptx
"""

import json
import logging
import threading
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify, abort, send_file, session, redirect, url_for

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from config import BankConfig
from usecases import USE_CASES, get_use_case, get_available_use_cases

BASE_DIR    = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
DATA_DIR    = BASE_DIR / "data"
OUTPUTS_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = "mock-sso-dev-key-not-for-production"
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# SSO mock
# ---------------------------------------------------------------------------
SSO_DATA_PATH = DATA_DIR / "sso" / "sso.json"


def _load_sso_data() -> dict:
    if SSO_DATA_PATH.exists():
        with open(SSO_DATA_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _get_current_user() -> dict | None:
    sso = _load_sso_data()
    username = session.get("sso_user") or sso.get("active_user")
    users = sso.get("users", {})
    return users.get(username)

_RUNS_STATE:      dict[str, dict] = {}
_DEAL_RUNS_STATE: dict[str, dict] = {}
_RUNS_LOCK = threading.Lock()

AGENT_STEPS = [
    {
        "key":   "kyc_screener",
        "label": "KYC Screener Agent",
        "short": "Validación KYC",
        "desc":  "Consulta los sistemas del banco, valida el expediente KYC y realiza el screening de sanciones y PEP.",
    },
    {
        "key":   "model_builder",
        "label": "Model Builder Agent",
        "short": "Normalización financiera",
        "desc":  "Normaliza los estados financieros disponibles en el banco a un modelo multi-período.",
    },
    {
        "key":   "market_researcher",
        "label": "Market Researcher Agent",
        "short": "Señales externas",
        "desc":  "Busca noticias, litigios y cambios societarios relevantes sobre la empresa.",
    },
    {
        "key":   "valuation_reviewer",
        "label": "Valuation Reviewer Agent",
        "short": "Análisis de riesgo",
        "desc":  "Calcula ratios de riesgo (Debt/EBITDA, liquidez, cobertura) y los compara con el histórico.",
    },
    {
        "key":   "credit_risk_report",
        "label": "Credit Risk Report Agent",
        "short": "Informe para comité",
        "desc":  "Sintetiza todos los hallazgos en el informe final para el comité de riesgos.",
    },
]

DEAL_AGENT_STEPS = [
    {
        "key":   "opportunity_researcher",
        "label": "Opportunity Researcher Agent",
        "short": "Identificación de oportunidades",
        "desc":  "Analiza el sector y detecta empresas con señales relevantes de financiación o asesoramiento.",
    },
    {
        "key":   "earnings_reviewer",
        "label": "Earnings Reviewer Agent",
        "short": "Análisis financiero",
        "desc":  "Revisa los resultados financieros de la empresa objetivo e identifica tendencias clave.",
    },
    {
        "key":   "model_builder",
        "label": "Model Builder Agent",
        "short": "Visión financiera",
        "desc":  "Calcula indicadores clave y genera una interpretación de la situación financiera.",
    },
    {
        "key":   "meeting_preparer",
        "label": "Meeting Preparer Agent",
        "short": "Briefing de cliente",
        "desc":  "Genera el perfil, situación actual, necesidades potenciales, riesgos y talking points.",
    },
    {
        "key":   "pitch_builder",
        "label": "Pitch Builder Agent",
        "short": "Propuesta y pitchbook",
        "desc":  "Construye la narrativa comercial y el pitchbook en PowerPoint listo para la reunión.",
    },
]


def _current_use_case_slug() -> str | None:
    endpoint = request.endpoint or ""
    if endpoint.startswith("kyc_"):
        return "kyc-credit-risk"
    if endpoint.startswith("deal_"):
        return "corporate-deal-intelligence"
    if endpoint == "usecase_detail":
        return (request.view_args or {}).get("slug")
    return None


def _build_banner_state() -> dict:
    endpoint = request.endpoint or ""
    current_slug = _current_use_case_slug()
    current_use_case = get_use_case(current_slug) if current_slug else None

    main_nav = []
    for uc in get_available_use_cases():
        main_nav.append({
            "label": uc.get("short_name") or uc.get("name") or uc.get("slug", ""),
            "href": url_for("usecase_detail", slug=uc["slug"]),
            "active": uc.get("slug") == current_slug,
        })

    tabs = []
    title_by_endpoint = {
        "usecases_menu": "Casos de uso",
        "kyc_runs_list": "Histórico",
        "kyc_run_detail": "Detalle de ejecución",
        "kyc_run_progress": "Análisis en curso",
        "deal_runs_list": "Histórico",
        "deal_run_detail": "Detalle de ejecución",
        "deal_run_progress": "Análisis en curso",
    }

    if endpoint.startswith("kyc_"):
        tabs = [
            {
                "label": AGENT_STEPS[0]["short"],
                "href": url_for("kyc_index"),
                "active": endpoint == "kyc_index",
            },
            {
                "label": "Histórico",
                "href": url_for("kyc_runs_list"),
                "active": endpoint in {"kyc_runs_list", "kyc_run_detail"},
            },
        ]
    elif endpoint.startswith("deal_"):
        tabs = [
            {
                "label": DEAL_AGENT_STEPS[0]["short"],
                "href": url_for("deal_index"),
                "active": endpoint == "deal_index",
            },
            {
                "label": "Histórico",
                "href": url_for("deal_runs_list"),
                "active": endpoint in {"deal_runs_list", "deal_run_detail"},
            },
        ]
    elif endpoint == "usecases_menu":
        tabs = [
            {
                "label": uc.get("code") or uc.get("short_name") or uc.get("name"),
                "href": url_for("usecase_detail", slug=uc["slug"]),
                "active": False,
            }
            for uc in get_available_use_cases()
        ]

    title_hidden_endpoints = {"kyc_index", "deal_index"}

    current_title = title_by_endpoint.get(endpoint)
    if endpoint == "usecase_detail" and current_use_case:
        current_title = current_use_case.get("name") or current_use_case.get("short_name")
    if endpoint in title_hidden_endpoints:
        current_title = ""
    elif not current_title and current_use_case:
        current_title = current_use_case.get("short_name") or current_use_case.get("name")
    if endpoint not in title_hidden_endpoints and not current_title:
        current_title = BankConfig.PRODUCT_NAME

    breadcrumb = [BankConfig.BANK_NAME]
    if current_use_case:
        breadcrumb.append(current_use_case.get("short_name") or current_use_case.get("name"))
    if current_title and current_title != breadcrumb[-1]:
        breadcrumb.append(current_title)

    return {
        "main_nav": main_nav,
        "tabs": tabs,
        "current_section": {"title": current_title},
        "breadcrumb": breadcrumb,
    }


@app.context_processor
def inject_globals():
    context = BankConfig.to_template_context()
    context["available_use_cases"] = get_available_use_cases()
    context["sso_user"] = _get_current_user()
    context["banner"] = _build_banner_state()
    return context


# ---------------------------------------------------------------------------
# Helpers genericos de estado de ejecucion
# ---------------------------------------------------------------------------

def _init_run_state(state_dict, run_id, steps, label):
    with _RUNS_LOCK:
        state_dict[run_id] = {
            "label":          label,
            "status":         "running",
            "current_step":   steps[0]["key"],
            "completed_steps": [],
            "error":          None,
            "real_run_id":    None,
            "run_dir":        None,
            "started_at":     datetime.now().isoformat(timespec="seconds"),
        }


def _update_run_state(state_dict, run_id, **kwargs):
    with _RUNS_LOCK:
        if run_id in state_dict:
            state_dict[run_id].update(kwargs)


def _mark_step_completed(state_dict, run_id, step_key):
    with _RUNS_LOCK:
        state = state_dict.get(run_id)
        if not state:
            return
        if step_key not in state["completed_steps"]:
            state["completed_steps"].append(step_key)


# ---------------------------------------------------------------------------
# Helpers de lectura de outputs/
# ---------------------------------------------------------------------------

def _format_run_timestamp(run_id: str) -> str:
    try:
        dt = datetime.strptime(run_id, "%Y%m%d%H%M%S")
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return run_id


def _list_runs(use_case: str) -> list[dict]:
    """
    Lista ejecuciones de un caso de uso concreto buscando en
    outputs/YYYYMMDDHHMMSS_KYC_empresa/result.json  o
    outputs/YYYYMMDDHHMMSS_DEAL_sector/result.json
    Devuelve lista ordenada más reciente primero.
    """
    prefix_marker = f"_{use_case.upper()}_"
    runs = []

    if not OUTPUTS_DIR.exists():
        return []

    for run_dir in sorted(OUTPUTS_DIR.iterdir(), reverse=True):
        if not run_dir.is_dir():
            continue
        name = run_dir.name
        if prefix_marker not in name:
            continue
        result_path = run_dir / "result.json"
        if not result_path.exists():
            continue
        try:
            with open(result_path, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        # Extraer run_id (la parte de timestamp antes de _KYC_/_DEAL_)
        run_id = name.split(prefix_marker, 1)[0]

        if use_case == "kyc":
            label = data.get("entity_name") or name
        else:
            label = data.get("company_name") or data.get("sector") or name

        runs.append({
            "run_id":      run_id,
            "entity_name": name,
            "label":       label,
            "timestamp":   _format_run_timestamp(run_id),
            "run_dir":     str(run_dir),
        })

    runs.sort(key=lambda r: r["run_id"], reverse=True)
    return runs


def _find_run_dir(use_case: str, run_id: str) -> Path | None:
    """Encuentra la carpeta de un run bajo outputs/YYYYMMDDHHMMSS_USECASE_*/"""
    prefix_marker = f"_{use_case.upper()}_"
    if not OUTPUTS_DIR.exists():
        return None
    for candidate in OUTPUTS_DIR.iterdir():
        if not candidate.is_dir():
            continue
        name = candidate.name
        if name.startswith(run_id) and prefix_marker in name:
            return candidate
    return None


def _load_run(use_case: str, run_id: str, extra_text_files: dict | None = None) -> dict:
    run_dir = _find_run_dir(use_case, run_id)
    if run_dir is None:
        abort(404)

    result = {}
    result_path = run_dir / "result.json"
    if result_path.exists():
        with open(result_path, encoding="utf-8") as f:
            result = json.load(f)

    run = {
        "run_id":    run_id,
        "timestamp": _format_run_timestamp(run_id),
        "result":    result,
        "run_dir":   run_dir,
    }

    for key, filename in (extra_text_files or {}).items():
        path = run_dir / filename
        run[key] = path.read_text(encoding="utf-8") if path.exists() else ""

    return run


# ---------------------------------------------------------------------------
# Rutas - Menu principal y fichas de casos de uso
# ---------------------------------------------------------------------------

@app.route("/")
def usecases_menu():
    return render_template("usecases.html", use_cases=USE_CASES)


@app.route("/casos-de-uso/<slug>")
def usecase_detail(slug):
    use_case = get_use_case(slug)
    if not use_case:
        abort(404)
    return render_template("usecase_detail.html", uc=use_case)


# ---------------------------------------------------------------------------
# Helpers de base de datos de empresas
# ---------------------------------------------------------------------------

def _load_empresas_kyc() -> dict:
    """Carga empresas KYC desde data/bbdd.json (fallback a data/empresas_kyc.json)."""
    bbdd_path = DATA_DIR / "bbdd.json"
    if bbdd_path.exists():
        with open(bbdd_path, encoding="utf-8") as f:
            data = json.load(f)
        empresas = data.get("empresas_kyc")
        if isinstance(empresas, dict):
            return empresas

    path = DATA_DIR / "empresas_kyc.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_empresas_deal() -> dict:
    """Carga empresas Deal desde data/bbdd.json (fallback a data/empresas_deal.json)."""
    bbdd_path = DATA_DIR / "bbdd.json"
    if bbdd_path.exists():
        with open(bbdd_path, encoding="utf-8") as f:
            data = json.load(f)
        empresas = data.get("empresas_deal")
        if isinstance(empresas, dict):
            return empresas

    path = DATA_DIR / "empresas_deal.json"
    if not path.exists():
        path = DATA_DIR / "empresas_mock.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _get_empresa_kyc(nombre: str) -> dict:
    """Devuelve los datos de una empresa KYC por nombre (insensible a mayúsculas/tildes)."""
    db = _load_empresas_kyc()
    nombre_lower = nombre.strip().lower()
    for key, data in db.items():
        if key.strip().lower() == nombre_lower:
            return data
    return {}


def _get_empresa_deal(nombre: str) -> dict:
    """Devuelve una empresa de la BBDD Deal por nombre exacto (case-insensitive)."""
    db = _load_empresas_deal()
    nombre_lower = nombre.strip().lower()
    for sector, empresas in db.items():
        for emp in empresas:
            if emp.get("empresa", "").strip().lower() == nombre_lower:
                return {"sector": sector, **emp}
    return {}


def _deal_to_kyc_entity(entity_name: str, deal_empresa: dict) -> dict:
    """Mapea una empresa de Deal al esquema mínimo KYC para no romper el flujo."""
    if not deal_empresa:
        return {}
    return {
        "nombre_legal": deal_empresa.get("empresa", entity_name),
        "nif": "No consta en BBDD KYC",
        "forma_juridica": "No consta",
        "domicilio_social": "No consta",
        "fecha_constitucion": "No consta",
        "capital_social": None,
        "cnae": "No consta",
        "sector": deal_empresa.get("sector", "No consta"),
        "empleados": deal_empresa.get("empleados"),
        "titulares_reales": [],
        "administradores": [],
        "alertas_kyc": [],
        "balances": [],
        "observaciones": (
            "Empresa seleccionada desde la BBDD de oportunidades Deal. "
            f"Descripción: {deal_empresa.get('descripcion', 'No consta')}. "
            f"Señal observada: {deal_empresa.get('señal', 'No consta')}"
        ),
    }


def _build_kyc_documents(entity_name: str, empresa: dict, extra_notes: str = "") -> list[dict]:
    """
    Construye documentos de texto realistas a partir de los datos de la empresa
    en la base de datos del banco, para pasarlos al doc_reader del KYC Screener Agent.
    """
    def _fmt_num(value, fallback: str = "No consta") -> str:
        if isinstance(value, (int, float)):
            return f"{value:,.0f}"
        return fallback

    docs = []

    # Documento 1: Escritura de constitución / ficha identificativa
    titulares_txt = "\n".join(
        f"  - {t['nombre']} ({t['participacion']}% - {t['nacionalidad']})"
        for t in empresa.get("titulares_reales", [])
    ) or "  - No consta"
    admins_txt = "\n".join(
        f"  - {a['nombre']} ({a['cargo']})"
        for a in empresa.get("administradores", [])
    ) or "  - No consta"
    alertas_txt = "\n".join(
        f"  - {a}" for a in empresa.get("alertas_kyc", [])
    ) or "  - Sin alertas registradas"

    doc_escritura = f"""FICHA IDENTIFICATIVA Y ESCRITURA DE CONSTITUCIÓN
Nombre legal: {empresa.get('nombre_legal', entity_name)}
NIF/CIF: {empresa.get('nif', 'No consta')}
Forma jurídica: {empresa.get('forma_juridica', 'No consta')}
Domicilio social: {empresa.get('domicilio_social', 'No consta')}
Fecha de constitución: {empresa.get('fecha_constitucion', 'No consta')}
Capital social: {_fmt_num(empresa.get('capital_social'))} EUR
CNAE: {empresa.get('cnae', 'No consta')}
Sector: {empresa.get('sector', 'No consta')}
Empleados: {empresa.get('empleados', 'No consta')}

TITULARES REALES (UBO):
{titulares_txt}

ADMINISTRADORES:
{admins_txt}

ALERTAS KYC REGISTRADAS EN BBDD DEL BANCO:
{alertas_txt}

OBSERVACIONES INTERNAS:
{empresa.get('observaciones', 'Sin observaciones adicionales.')}
{f'NOTAS DEL ANALISTA: {extra_notes}' if extra_notes else ''}
"""
    docs.append({"name": "escritura_constitucion.txt", "text": doc_escritura})

    # Documentos 2..N: un balance por cada período disponible
    for balance in empresa.get("balances", []):
        periodo = balance.get("periodo", "N/D")
        doc_balance = f"""ESTADOS FINANCIEROS - EJERCICIO {periodo}
Empresa: {empresa.get('nombre_legal', entity_name)}
NIF/CIF: {empresa.get('nif', 'No consta')}
Período: {periodo}

CUENTA DE RESULTADOS:
    Ingresos de explotación: {_fmt_num(balance.get('ingresos'), 'N/D')} EUR
    EBITDA: {_fmt_num(balance.get('ebitda'), 'N/D')} EUR
    Gastos financieros: {_fmt_num(balance.get('gastos_financieros'), 'N/D')} EUR

BALANCE:
    Activo corriente: {_fmt_num(balance.get('activo_corriente'), 'N/D')} EUR
    Pasivo corriente: {_fmt_num(balance.get('pasivo_corriente'), 'N/D')} EUR
    Deuda financiera neta: {_fmt_num(balance.get('deuda_financiera'), 'N/D')} EUR
    Patrimonio neto: {_fmt_num(balance.get('patrimonio_neto'), 'N/D')} EUR

Fuente: Sistemas contables del banco (datos remitidos por la empresa y validados internamente).
"""
        docs.append({"name": f"balance_{periodo}.txt", "text": doc_balance})

    # Si no había datos en la BBDD, construir un documento mínimo
    if not docs:
        docs.append({"name": "expediente_basico.txt", "text": (
            f"Razón social: {entity_name}\n"
            f"Estado: empresa no encontrada en la base de datos del banco.\n"
            f"Se requiere aportación de documentación por parte del cliente.\n"
            f"{f'Notas del analista: {extra_notes}' if extra_notes else ''}"
        )})

    return docs


def _load_fuentes_externas() -> dict:
    """Carga data/fuentes_externas.json."""
    path = DATA_DIR / "fuentes_externas.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("empresas", {})


def _get_comunidades_disponibles() -> list[str]:
    """
    Devuelve la lista de comunidades autonomas disponibles combinando
    bbdd.json (clientes) y fuentes_externas.json (no clientes).
    """
    comunidades = set()

    # Desde bbdd.json (clientes KYC tienen domicilio_social)
    db_kyc = _load_empresas_kyc()
    for emp in db_kyc.values():
        domicilio = emp.get("domicilio_social", "")
        # Intentar extraer comunidad desde el campo observaciones o sector
        # (en bbdd.json no siempre hay comunidad explicita, usamos provincia del domicilio)
        comunidad = emp.get("comunidad_autonoma", "")
        if comunidad:
            comunidades.add(comunidad)

    # Desde fuentes_externas.json (no clientes)
    ext = _load_fuentes_externas()
    for emp in ext.values():
        ca = emp.get("comunidad_autonoma", "")
        if ca:
            comunidades.add(ca)

    return sorted(comunidades)


def _get_empresas_por_geografia(comunidad: str, fuente: str) -> list[dict]:
    """
    Devuelve empresas de una comunidad autonoma.
    fuente: "interna" (bbdd.json) o "externa" (fuentes_externas.json)
    """
    results = []
    if fuente == "interna":
        db = _load_empresas_kyc()
        for nombre, emp in db.items():
            if emp.get("comunidad_autonoma", "").lower() == comunidad.lower():
                results.append({
                    "empresa": nombre,
                    "sector":  emp.get("sector", ""),
                    "descripcion": emp.get("observaciones", ""),
                    "señal": f"Cliente interno. Sector: {emp.get('sector', '')}.",
                    "ingresos_estimados": None,
                    "empleados": emp.get("empleados"),
                })
    else:
        ext = _load_fuentes_externas()
        for nombre, emp in ext.items():
            if emp.get("comunidad_autonoma", "").lower() == comunidad.lower():
                perfil = emp.get("perfil_publico", {})
                senales = emp.get("senales_externas", [])
                results.append({
                    "empresa": nombre,
                    "sector":  perfil.get("sector", ""),
                    "descripcion": perfil.get("descripcion", ""),
                    "señal": perfil.get("senal_mercado", senales[0] if senales else ""),
                    "ingresos_estimados": None,
                    "empleados": None,
                })
    return results


# ---------------------------------------------------------------------------
# API - Autocompletado de empresas
# ---------------------------------------------------------------------------

@app.route("/api/empresas/kyc")
def api_empresas_kyc():
    """Devuelve lista de nombres de empresas KYC para autocompletado."""
    q = request.args.get("q", "").strip().lower()
    db = _load_empresas_kyc()
    names = sorted(db.keys())
    if q:
        names = [n for n in names if q in n.lower()]
    return jsonify(names)


@app.route("/api/empresas/deal")
def api_empresas_deal():
    """Devuelve lista de nombres de empresas Deal para autocompletado."""
    q = request.args.get("q", "").strip().lower()
    sector_filter = request.args.get("sector", "").strip()
    db = _load_empresas_deal()
    names = []
    for sector, empresas in db.items():
        if sector_filter and sector.lower() != sector_filter.lower():
            continue
        for emp in empresas:
            nombre = emp.get("empresa", "")
            if nombre and (not q or q in nombre.lower()):
                names.append(nombre)
    return jsonify(sorted(set(names)))


# ---------------------------------------------------------------------------
# Caso de uso 1 - KYC & Credit Risk Intelligence (prefijo /kyc)
# ---------------------------------------------------------------------------

def _run_kyc_pipeline_background(run_id, entity_name, documents):
    try:
        from kyc_orchestrator import run_multiagent_pipeline

        def step_cb(step_key: str, event: str):
            if event == "started":
                _update_run_state(_RUNS_STATE, run_id, current_step=step_key)
            elif event == "completed":
                _mark_step_completed(_RUNS_STATE, run_id, step_key)

        result = run_multiagent_pipeline(
            entity_name=entity_name,
            documents=documents,
            use_mock_screening=False,
            use_mock_market_research=False,
            step_callback=step_cb,
        )
        _update_run_state(_RUNS_STATE, run_id,
                          status="done",
                          current_step=None,
                          real_run_id=result["run_id"])
    except Exception as exc:  # noqa: BLE001
        logger.exception("Error en pipeline KYC en background | run_id=%s | entity=%s", run_id, entity_name)
        _update_run_state(
            _RUNS_STATE,
            run_id,
            status="error",
            error=f"{type(exc).__name__}: {exc}",
            current_step=None,
        )


@app.route("/kyc/")
def kyc_index():
    runs = _list_runs("kyc")[:6]
    empresa_names = set(_load_empresas_kyc().keys())
    for empresas in _load_empresas_deal().values():
        for emp in empresas:
            nombre = emp.get("empresa", "")
            if nombre:
                empresa_names.add(nombre)
    empresa_names = sorted(empresa_names)
    return render_template("index.html", runs=runs, agent_steps=AGENT_STEPS,
                           empresa_names=empresa_names)


@app.route("/kyc/runs")
def kyc_runs_list():
    runs = _list_runs("kyc")
    return render_template("runs_list.html", runs=runs)


@app.route("/kyc/runs/<run_id>")
def kyc_run_detail(run_id):
    run = _load_run("kyc", run_id, extra_text_files={"informe_md": "informe.md"})
    return render_template("run_detail.html", run=run, agent_steps=AGENT_STEPS)


@app.route("/kyc/runs/<run_id>/progress")
def kyc_run_progress(run_id):
    with _RUNS_LOCK:
        state = _RUNS_STATE.get(run_id)
    if not state:
        abort(404)
    return render_template(
        "run_progress.html",
        run_id=run_id,
        entity_name=state["label"],
        agent_steps=AGENT_STEPS,
        api_status_url=f"/kyc/api/runs/{run_id}/status",
        result_url_prefix="/kyc/runs",
    )


@app.route("/kyc/api/runs/<run_id>/status")
def kyc_api_run_status(run_id):
    with _RUNS_LOCK:
        state = _RUNS_STATE.get(run_id)
    if not state:
        return jsonify({"error": "run_id no encontrado"}), 404
    return jsonify(state)


@app.route("/kyc/runs/<run_id>/informe.docx")
def kyc_download_informe(run_id):
    run_dir = _find_run_dir("kyc", run_id)
    if run_dir is None:
        abort(404)
    informe_md  = (run_dir / "informe.md").read_text(encoding="utf-8") if (run_dir / "informe.md").exists() else ""
    entity_name = ""
    result_path = run_dir / "result.json"
    if result_path.exists():
        with open(result_path, encoding="utf-8") as f:
            entity_name = json.load(f).get("entity_name", "")
    try:
        from docx_builder import build_informe_docx
        docx_path = run_dir / "informe.docx"
        build_informe_docx(docx_path, entity_name, informe_md)
    except Exception as exc:
        abort(500, f"Error generando el informe: {exc}")
    safe_name     = "".join(c if c.isalnum() or c in " -_" else "" for c in entity_name).strip().replace(" ", "_")
    download_name = f"informe_{safe_name or run_id}.docx"
    return send_file(docx_path, as_attachment=True, download_name=download_name)


@app.route("/kyc/solicitudes/nueva", methods=["POST"])
def kyc_nueva_solicitud():
    entity_name = request.form.get("entity_name", "").strip()
    if not entity_name:
        abort(400, "El nombre de la entidad es obligatorio")

    notes = request.form.get("entity_notes", "").strip()

    # Consultar la base de datos del banco
    empresa = _get_empresa_kyc(entity_name)
    if not empresa:
        empresa = _deal_to_kyc_entity(entity_name, _get_empresa_deal(entity_name))
    documents = _build_kyc_documents(entity_name, empresa, extra_notes=notes)

    provisional_run_id = uuid.uuid4().hex[:12]
    _init_run_state(_RUNS_STATE, provisional_run_id, AGENT_STEPS, entity_name)

    threading.Thread(
        target=_run_kyc_pipeline_background,
        args=(provisional_run_id, entity_name, documents),
        daemon=True,
    ).start()

    return render_template(
        "run_progress.html",
        run_id=provisional_run_id,
        entity_name=entity_name,
        agent_steps=AGENT_STEPS,
        api_status_url=f"/kyc/api/runs/{provisional_run_id}/status",
        result_url_prefix="/kyc/runs",
    )


# ---------------------------------------------------------------------------
# Caso de uso 2 - Corporate & Deal Intelligence (prefijo /deal)
# ---------------------------------------------------------------------------

def _run_deal_pipeline_background(run_id, sector, company_name,
                                   financial_documents, fuente="interna",
                                   geografia="", empresas_geografia=None):
    try:
        from deal_orchestrator import run_deal_intelligence_pipeline

        def step_cb(step_key: str, event: str):
            if event == "started":
                _update_run_state(_DEAL_RUNS_STATE, run_id, current_step=step_key)
            elif event == "completed":
                _mark_step_completed(_DEAL_RUNS_STATE, run_id, step_key)

        result = run_deal_intelligence_pipeline(
            sector=sector,
            company_name=company_name or None,
            financial_documents=financial_documents,
            fuente=fuente,
            geografia=geografia,
            empresas_geografia=empresas_geografia or [],
            use_mock=False,
            step_callback=step_cb,
        )
        _update_run_state(_DEAL_RUNS_STATE, run_id,
                          status="done",
                          current_step=None,
                          real_run_id=result["run_id"])
    except Exception as exc:  # noqa: BLE001
        logger.exception(
            "Error en pipeline DEAL en background | run_id=%s | sector=%s | company=%s",
            run_id,
            sector,
            company_name,
        )
        _update_run_state(
            _DEAL_RUNS_STATE,
            run_id,
            status="error",
            error=f"{type(exc).__name__}: {exc}",
            current_step=None,
        )


@app.route("/deal/")
def deal_index():
    runs = _list_runs("deal")[:6]

    # Nombres para autocomplete por fuente
    empresa_names_internas = sorted(_load_empresas_kyc().keys())
    empresa_names_externas = sorted(_load_fuentes_externas().keys())
    empresa_names_todas    = sorted(set(empresa_names_internas + empresa_names_externas))

    comunidades = _get_comunidades_disponibles()

    return render_template(
        "deal_index.html",
        runs=runs,
        agent_steps=DEAL_AGENT_STEPS,
        empresa_names=empresa_names_todas,
        empresa_names_internas=empresa_names_internas,
        empresa_names_externas=empresa_names_externas,
        comunidades=comunidades,
    )


@app.route("/deal/runs")
def deal_runs_list():
    runs = _list_runs("deal")
    return render_template("deal_runs_list.html", runs=runs)


@app.route("/deal/runs/<run_id>")
def deal_run_detail(run_id):
    run = _load_run("deal", run_id, extra_text_files={
        "propuesta_md":     "propuesta.md",
        "earnings_summary": "2_earnings_reviewer/output.txt",
    })
    pptx_rel = run["result"].get("pitch_output", {}).get("pptx_path")
    run["pptx_available"] = bool(pptx_rel) and (run["run_dir"] / pptx_rel).exists()
    return render_template("deal_run_detail.html", run=run, agent_steps=DEAL_AGENT_STEPS)


@app.route("/deal/runs/<run_id>/progress")
def deal_run_progress(run_id):
    with _RUNS_LOCK:
        state = _DEAL_RUNS_STATE.get(run_id)
    if not state:
        abort(404)
    return render_template(
        "run_progress.html",
        run_id=run_id,
        entity_name=state["label"],
        agent_steps=DEAL_AGENT_STEPS,
        api_status_url=f"/deal/api/runs/{run_id}/status",
        result_url_prefix="/deal/runs",
    )


@app.route("/deal/api/runs/<run_id>/status")
def deal_api_run_status(run_id):
    with _RUNS_LOCK:
        state = _DEAL_RUNS_STATE.get(run_id)
    if not state:
        return jsonify({"error": "run_id no encontrado"}), 404
    return jsonify(state)


@app.route("/deal/runs/<run_id>/pitchbook.pptx")
def deal_download_pitchbook(run_id):
    run_dir = _find_run_dir("deal", run_id)
    if run_dir is None:
        abort(404)
    result_path = run_dir / "result.json"
    if not result_path.exists():
        abort(404)
    with open(result_path, encoding="utf-8") as f:
        result = json.load(f)
    pptx_rel = result.get("pitch_output", {}).get("pptx_path")
    if not pptx_rel:
        abort(404)
    pptx_path = run_dir / pptx_rel
    if not pptx_path.exists():
        abort(404)
    company       = result.get("company_name", "empresa")
    safe_company  = "".join(c if c.isalnum() or c in " -_" else "" for c in company).strip().replace(" ", "_")
    download_name = f"pitchbook_{safe_company or 'oportunidad'}.pptx"
    return send_file(pptx_path, as_attachment=True, download_name=download_name)


@app.route("/deal/runs/<run_id>/pitchbook.pdf")
def deal_download_pitchbook_pdf(run_id):
    """Descarga del pitchbook en formato PDF."""
    run_dir = _find_run_dir("deal", run_id)
    if run_dir is None:
        abort(404)
    result_path = run_dir / "result.json"
    if not result_path.exists():
        abort(404)
    with open(result_path, encoding="utf-8") as f:
        result = json.load(f)
    pdf_rel = result.get("pitch_output", {}).get("pdf_path")
    if not pdf_rel:
        abort(404)
    pdf_path = run_dir / pdf_rel
    if not pdf_path.exists():
        abort(404)
    company      = result.get("company_name", "empresa")
    safe_company = "".join(c if c.isalnum() or c in " -_" else "" for c in company).strip().replace(" ", "_")
    download_name = f"pitchbook_{safe_company or 'oportunidad'}.pdf"
    return send_file(pdf_path, as_attachment=True, download_name=download_name)


@app.route("/deal/solicitudes/nueva", methods=["POST"])
def deal_nueva_solicitud():
    search_mode  = request.form.get("search_mode", "").strip().lower()

    # Campos raw del formulario
    sector_raw            = request.form.get("sector", "").strip()
    company_name_raw      = request.form.get("company_name", "").strip()
    company_name_sector   = request.form.get("company_name_sector", "").strip()
    company_name_empresa  = request.form.get("company_name_empresa", "").strip()
    geografia_raw         = request.form.get("geografia", "").strip()
    fuente_raw            = request.form.get("fuente", "interna")

    # Resolver parametros efectivos por modo de busqueda para que las pestanas
    # sean independientes entre si.
    sector = ""
    company_name = ""
    geografia = ""
    fuente = fuente_raw

    if search_mode == "empresa":
        company_name = company_name_raw or company_name_empresa
    elif search_mode == "geografia":
        geografia = geografia_raw
    elif search_mode == "sector":
        sector = sector_raw
        company_name = company_name_raw or company_name_sector
    else:
        # Fallback retrocompatible si llega una version antigua del formulario.
        sector = sector_raw
        company_name = company_name_raw or company_name_empresa or company_name_sector
        geografia = geografia_raw

    confirmar_externa = request.form.get("confirmar_externa", "")

    # Validacion por modo activo
    if search_mode == "empresa" and not company_name:
        abort(400, "Debes indicar una empresa en la pestana 'Por empresa'.")
    if search_mode == "sector" and not sector:
        abort(400, "Debes indicar un sector en la pestana 'Por sector'.")
    if search_mode == "geografia" and not geografia:
        abort(400, "Debes indicar una zona geografica en la pestana 'Por zona geografica'.")
    if not search_mode and not sector and not company_name and not geografia:
        abort(400, "Debes indicar al menos un sector, una empresa o una zona geografica.")

    # Si viene empresa sin sector ni geografia, detectar si es cliente
    empresa_es_cliente = False
    if company_name and not sector and not geografia:
        db_kyc = _load_empresas_kyc()
        empresa_es_cliente = company_name.strip().lower() in {
            k.strip().lower() for k in db_kyc.keys()
        }
        # Si no es cliente y no ha confirmado, devolver pagina de confirmacion
        if not empresa_es_cliente and not confirmar_externa:
            return render_template(
                "deal_confirmar_externa.html",
                company_name=company_name,
                department_name_deal=BankConfig.DEPARTMENT_NAME_DEAL,
            )
        # Si es cliente, forzar fuente interna
        if empresa_es_cliente:
            fuente = "interna"
        else:
            fuente = "externa"

    # Si hay geografia, construir lista de empresas del area
    empresas_geografia = []
    if geografia:
        empresas_geografia = _get_empresas_por_geografia(geografia, fuente)

    financial_documents = []
    for name, text in zip(request.form.getlist("doc_name"),
                          request.form.getlist("doc_text")):
        if text.strip():
            financial_documents.append({"name": name.strip() or "documento.txt", "text": text})

    provisional_run_id = uuid.uuid4().hex[:12]
    label = company_name or (f"Zona {geografia}" if geografia else f"Sector {sector}")
    _init_run_state(_DEAL_RUNS_STATE, provisional_run_id, DEAL_AGENT_STEPS, label)

    threading.Thread(
        target=_run_deal_pipeline_background,
        args=(provisional_run_id, sector, company_name, financial_documents,
              fuente, geografia, empresas_geografia),
        daemon=True,
    ).start()

    return render_template(
        "run_progress.html",
        run_id=provisional_run_id,
        entity_name=label,
        agent_steps=DEAL_AGENT_STEPS,
        api_status_url=f"/deal/api/runs/{provisional_run_id}/status",
        result_url_prefix="/deal/runs",
    )

if __name__ == "__main__":
    # Servir fotos SSO desde data/sso/images/
    @app.route("/sso/photo/<filename>")
    def sso_photo(filename):
        photo_dir = DATA_DIR / "sso" / "images"
        return send_file(photo_dir / filename)

    @app.route("/sso/switch/<username>")
    def sso_switch(username):
        sso = _load_sso_data()
        if username in sso.get("users", {}):
            session["sso_user"] = username
        return redirect(request.referrer or url_for("usecases_menu"))

    @app.route("/sso/api/user")
    def sso_api_user():
        user = _get_current_user()
        if not user:
            return jsonify({"error": "No user"}), 404
        return jsonify(user)

    @app.route("/sso/api/users")
    def sso_api_users():
        sso = _load_sso_data()
        return jsonify(list(sso.get("users", {}).values()))

    app.run(debug=True)