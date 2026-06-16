"""
usecases.py
=============
Catalogo de casos de uso disponibles en la plataforma.
"""

USE_CASES = [
    {
        "slug": "kyc-credit-risk",
        "status": "available",
        "code": "KYC-01",
        "name": "KYC & Credit Risk Intelligence",
        "short_name": "KYC + Riesgo de Crédito",
        "tagline": "El expediente se prepara solo, antes de que el analista abra el primer documento.",
        "summary": (
            "Un sistema de cinco agentes especializados lee toda la "
            "documentación de una solicitud de financiación -identidad, "
            "escrituras, balances, extractos- y entrega al analista un "
            "expediente ya organizado: validación KYC, análisis financiero, "
            "comparación con el histórico del cliente, señales externas y un "
            "informe listo para el comité de riesgos."
        ),
        "problem": (
            "Antes de valorar un riesgo, un analista puede pasar varias horas "
            "solo recopilando y leyendo documentación: identidad, escrituras "
            "de constitución, declaraciones fiscales, balances, nóminas, "
            "extractos bancarios, informes de riesgos, historial en el CRM, "
            "noticias públicas y listas de sanciones o PEP."
        ),
        "how_it_works": [
            {"title": "Ingesta documental",
             "description": "El sistema recopila y organiza todos los documentos de la solicitud, sea cual sea su formato de origen."},
            {"title": "Validación KYC",
             "description": "Comprueba identidad, vigencia de documentos, consistencia de nombres, titular real, sanciones y PEP, con una explicación clara de cada hallazgo."},
            {"title": "Extracción financiera",
             "description": "Lee balances, cuentas de resultados y flujos de caja, y normaliza la información aunque venga en formatos distintos."},
            {"title": "Análisis de riesgo",
             "description": "Calcula indicadores como Debt/EBITDA, liquidez o cobertura de intereses, y explica qué ha cambiado y por qué importa."},
            {"title": "Cruce con el histórico",
             "description": "Consulta operaciones anteriores, incidencias, impagos y productos contratados para dar contexto a los números."},
            {"title": "Señales externas",
             "description": "Busca noticias, cambios societarios, concursos o litigios públicos que puedan ser relevantes para la operación."},
            {"title": "Informe para el comité",
             "description": "Genera un resumen ejecutivo con hallazgos, riesgos y recomendaciones, listo para la decisión del analista y el comité."},
        ],
        "benefits": [
            {"metric": "2-4h → 15-30min", "title": "Reduce tiempos",
             "description": "Una revisión que hoy ocupa entre dos y cuatro horas puede quedar preparada en quince a treinta minutos."},
            {"metric": "Criterio único", "title": "Mejora la consistencia",
             "description": "Todos los expedientes se analizan con los mismos criterios y la misma estructura, reduciendo diferencias entre analistas."},
            {"metric": "Menos omisiones", "title": "Disminuye errores humanos",
             "description": "Es menos probable pasar por alto un documento caducado, un balance incompleto o una alerta KYC pendiente."},
            {"metric": "Trazabilidad total", "title": "Facilita las auditorías",
             "description": "Cada conclusión queda enlazada al documento, dato y agente de origen, lista para revisión interna o regulatoria."},
            {"metric": "Foco analítico", "title": "Aumenta la productividad",
             "description": "El analista dedica su tiempo a interpretar el riesgo y discutir excepciones, no a recopilar información."},
        ],
        "disclaimer": (
            "La IA no decide si se concede o deniega una operación. Construye "
            "un expediente inteligente y trazable para que el analista y el "
            "comité de riesgos decidan con más rapidez y confianza, "
            "manteniendo siempre el control humano sobre la decisión final."
        ),
        "agents": [
            {"name": "KYC Screener Agent",      "role": "Ingesta y validación KYC"},
            {"name": "Model Builder Agent",      "role": "Normalización financiera"},
            {"name": "Market Researcher Agent",  "role": "Señales externas"},
            {"name": "Valuation Reviewer Agent", "role": "Análisis de riesgo"},
            {"name": "Credit Risk Report Agent", "role": "Informe para comité"},
        ],
    },
    {
        "slug": "corporate-deal-intelligence",
        "status": "available",
        "code": "DEAL-01",
        "name": "Corporate & Deal Intelligence",
        "short_name": "Deal Intelligence",
        "tagline": "El equipo comercial llega a cada reunión con el contexto ya preparado.",
        "summary": (
            "Un sistema de cinco agentes especializados analiza un sector, "
            "identifica empresas con potencial de financiación o "
            "asesoramiento, revisa sus resultados financieros y construye "
            "un briefing de cliente y una propuesta comercial -incluido un "
            "pitchbook en PowerPoint- lista para revisar antes de cualquier "
            "interacción con el cliente."
        ),
        "problem": (
            "Antes de una reunión comercial, un banker puede dedicar entre "
            "varias horas y un día completo a tareas repetitivas: buscar "
            "empresas relevantes en un sector, leer cuentas anuales y "
            "resultados, revisar noticias, comparar con otras empresas del "
            "sector e identificar posibles necesidades, y preparar una "
            "presentación comercial desde cero."
        ),
        "how_it_works": [
            {"title": "Identificación de oportunidades",
             "description": "Analiza un sector y detecta empresas con señales relevantes -expansión, crecimiento, incremento de deuda- y las prioriza según el interés de la oportunidad."},
            {"title": "Análisis de resultados financieros",
             "description": "Revisa cuentas anuales, resultados trimestrales o presentaciones corporativas de la empresa objetivo e identifica tendencias clave de ingresos, márgenes y CAPEX."},
            {"title": "Construcción de visión financiera",
             "description": "Normaliza la información disponible, calcula indicadores clave y genera una interpretación de alto nivel sobre posibles necesidades de financiación."},
            {"title": "Preparación de briefing",
             "description": "Genera un resumen estructurado con el perfil de la empresa, su situación actual, necesidades potenciales, riesgos y puntos de conversación para la reunión."},
            {"title": "Generación de propuesta comercial",
             "description": "Construye una narrativa comercial y un pitchbook en PowerPoint con la oportunidad detectada, el encaje con productos del banco, comparables sectoriales y próximos pasos."},
            {"title": "Validación y ajuste humano",
             "description": "El equipo comercial revisa el análisis, ajusta el mensaje, personaliza la aproximación y define la estrategia de entrada antes de contactar al cliente."},
        ],
        "benefits": [
            {"metric": "Horas → minutos", "title": "Reduce tiempos de preparación",
             "description": "Una tarea que puede requerir varias horas pasa a resolverse en minutos, dejando más tiempo para la interacción con el cliente."},
            {"metric": "Originación proactiva", "title": "Incrementa la proactividad comercial",
             "description": "El banco deja de depender únicamente de solicitudes entrantes y puede identificar oportunidades de forma sistemática."},
            {"metric": "Contexto completo", "title": "Mejora la calidad de las reuniones",
             "description": "Cada interacción se apoya en contexto completo, datos actualizados y una narrativa estructurada."},
            {"metric": "Criterio único", "title": "Estandariza el enfoque comercial",
             "description": "Todos los equipos trabajan con la misma estructura de análisis, los mismos indicadores y la misma calidad de preparación."},
            {"metric": "Foco comercial", "title": "Aumenta la productividad",
             "description": "Los equipos comerciales reducen el trabajo manual y pueden centrarse en la relación con el cliente y la generación de negocio."},
        ],
        "disclaimer": (
            "El valor de este caso de uso no está en automatizar la venta, "
            "sino en preparar mejor cada interacción comercial. El equipo "
            "humano revisa, ajusta y personaliza la propuesta antes de "
            "cualquier contacto con el cliente; la decisión sobre la "
            "estrategia de entrada corresponde siempre al equipo comercial."
        ),
        "agents": [
            {"name": "Opportunity Researcher Agent", "role": "Identificación de oportunidades"},
            {"name": "Earnings Reviewer Agent",      "role": "Análisis financiero"},
            {"name": "Model Builder Agent",          "role": "Visión financiera (opcional)"},
            {"name": "Meeting Preparer Agent",       "role": "Briefing de cliente"},
            {"name": "Pitch Builder Agent",          "role": "Propuesta y pitchbook"},
        ],
    },
    {
        "slug": "proximo-caso-de-uso",
        "status": "coming_soon",
        "code": "··-··",
        "name": "Próximo caso de uso",
        "short_name": "Próximamente",
        "tagline": "Nuevos agentes especializados, en preparación.",
        "summary": (
            "Estamos preparando un nuevo caso de uso para esta plataforma. "
            "Aparecerá aquí en cuanto esté disponible."
        ),
        "problem": "",
        "how_it_works": [],
        "benefits": [],
        "disclaimer": "",
        "agents": [],
    },
]


def get_use_case(slug: str) -> dict | None:
    for uc in USE_CASES:
        if uc["slug"] == slug:
            return uc
    return None


def get_available_use_cases() -> list[dict]:
    return [uc for uc in USE_CASES if uc["status"] == "available"]