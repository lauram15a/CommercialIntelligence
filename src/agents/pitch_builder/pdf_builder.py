"""
src/agents/pitch_builder/pdf_builder.py
==========================================
Genera el pitchbook corporativo en formato PDF usando ReportLab.
No requiere LibreOffice ni ninguna dependencia externa al entorno Python.

El PDF replica la estructura de las 6 diapositivas del .pptx con la
paleta corporativa del cliente activo (config.py -> config_clienteA.json).

Uso:
    from agents.pitch_builder.pdf_builder import build_pitch_pdf
    build_pitch_pdf(output_path, company_name, sector, pitch, meeting_brief, model_output)
"""

import sys
from pathlib import Path

# Asegurar que src/ esta en el path
_SRC = Path(__file__).resolve().parent.parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, KeepTogether, HRFlowable,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

try:
    from config import BankConfig
    PRIMARY    = HexColor(BankConfig.COLOR_PRIMARY)
    PRIMARY_DK = HexColor(BankConfig.COLOR_PRIMARY_DARK)
    ACCENT     = HexColor(BankConfig.COLOR_ACCENT)
    BG         = HexColor(BankConfig.COLOR_BG)
    INK        = HexColor(BankConfig.COLOR_INK)
    INK_MUTED  = HexColor(BankConfig.COLOR_INK_MUTED)
    BANK_NAME  = BankConfig.BANK_NAME
    FOOTER_TXT = BankConfig.FOOTER_TEXT
except Exception:
    PRIMARY    = HexColor("#FF8D30")
    PRIMARY_DK = HexColor("#C05600")
    ACCENT     = HexColor("#FED227")
    BG         = HexColor("#F9F9F9")
    INK        = HexColor("#212425")
    INK_MUTED  = HexColor("#6B7280")
    BANK_NAME  = "Banco"
    FOOTER_TXT = "Documento de uso interno."

SURFACE   = white
BORDER    = HexColor("#E5E7EB")
NAVY      = HexColor("#1B2A4A")
SAND      = HexColor("#EDE6D9")
COPPER    = HexColor("#C97B4A")

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 1.8 * cm


# ---------------------------------------------------------------------------
# Helpers de estilo
# ---------------------------------------------------------------------------

def _style(name, **kwargs):
    defaults = dict(fontName="Helvetica", fontSize=11, leading=16,
                    textColor=INK, alignment=TA_LEFT)
    defaults.update(kwargs)
    return ParagraphStyle(name, **defaults)


S_EYEBROW   = _style("eyebrow",  fontSize=9,  textColor=INK_MUTED, fontName="Helvetica-Bold",
                      spaceAfter=2)
S_H1        = _style("h1",       fontSize=22, textColor=NAVY, fontName="Helvetica-Bold",
                      leading=28, spaceAfter=6)
S_H2        = _style("h2",       fontSize=15, textColor=NAVY, fontName="Helvetica-Bold",
                      leading=20, spaceAfter=4, spaceBefore=14)
S_H3        = _style("h3",       fontSize=12, textColor=INK,  fontName="Helvetica-Bold",
                      leading=16, spaceAfter=3, spaceBefore=8)
S_BODY      = _style("body",     fontSize=11, leading=17, spaceAfter=4)
S_BODY_MUTED= _style("bodym",    fontSize=10, leading=15, textColor=INK_MUTED, spaceAfter=3)
S_BULLET    = _style("bullet",   fontSize=10, leading=15, leftIndent=14, spaceAfter=3,
                      bulletIndent=4)
S_LABEL     = _style("label",    fontSize=8,  textColor=INK_MUTED, fontName="Helvetica-Bold",
                      spaceAfter=2, spaceBefore=10)
S_KPI_VAL   = _style("kpival",   fontSize=26, textColor=COPPER, fontName="Helvetica-Bold",
                      leading=30, alignment=TA_CENTER)
S_KPI_LBL   = _style("kpilbl",   fontSize=9,  textColor=INK_MUTED, alignment=TA_CENTER,
                      spaceAfter=6)
S_CENTER    = _style("center",   alignment=TA_CENTER)
S_FOOTER    = _style("footer",   fontSize=7.5, textColor=INK_MUTED, alignment=TA_CENTER)
S_DISCLAIMER= _style("disc",     fontSize=8.5, textColor=INK_MUTED, leading=12,
                      leftIndent=6, rightIndent=6)
S_TITLE_COVER = _style("tcover", fontSize=28, textColor=white, fontName="Helvetica-Bold",
                        leading=34, spaceAfter=8)
S_SUB_COVER   = _style("scover", fontSize=14, textColor=HexColor("#C9D2E6"),
                        fontName="Helvetica-Oblique", leading=20)


def _p(text, style=None):
    return Paragraph(str(text or ""), style or S_BODY)


def _bullet(text):
    return Paragraph(f"- {text}", S_BULLET)


def _label(text):
    return Paragraph(text.upper(), S_LABEL)


def _hr(color=None, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color or BORDER, spaceAfter=8, spaceBefore=4)


def _safe(val, fallback=""):
    if val is None:
        return fallback
    v = str(val).strip()
    return v if v else fallback


def _kpi_table(indicators: list[dict]) -> Table:
    """Tabla de 3 KPIs en una fila."""
    cells = []
    for ind in indicators[:3]:
        val = _safe(ind.get("valor"), "-")
        nom = _safe(ind.get("nombre"), "")
        cells.append([
            Paragraph(val, S_KPI_VAL),
            Paragraph(nom, S_KPI_LBL),
        ])
    # Rellenar hasta 3 columnas
    while len(cells) < 3:
        cells.append([Paragraph("-", S_KPI_VAL), Paragraph("", S_KPI_LBL)])

    data = [[c[0] for c in cells], [c[1] for c in cells]]
    col_w = (PAGE_W - 2 * MARGIN) / 3
    t = Table(data, colWidths=[col_w] * 3)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SAND),
        ("BOX",        (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID",  (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def _two_col_table(left_items: list, right_items: list,
                   left_title: str, right_title: str) -> Table:
    """Tabla de dos columnas para necesidades/riesgos."""
    def _col(title, items):
        content = [_label(title)]
        for item in items:
            content.append(_bullet(item))
        return content

    left_col  = _col(left_title,  left_items)
    right_col = _col(right_title, right_items)
    max_rows  = max(len(left_col), len(right_col))
    while len(left_col)  < max_rows: left_col.append(Spacer(1, 1))
    while len(right_col) < max_rows: right_col.append(Spacer(1, 1))

    data = [[left_col[i], right_col[i]] for i in range(max_rows)]
    col_w = (PAGE_W - 2 * MARGIN) / 2 - 0.5 * cm
    t = Table(data, colWidths=[col_w, col_w])
    t.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("BACKGROUND",   (0, 0), (0, -1), SAND),
        ("BACKGROUND",   (1, 0), (1, -1), white),
        ("BOX",          (0, 0), (0, -1), 0.5, BORDER),
        ("BOX",          (1, 0), (1, -1), 0.5, BORDER),
    ]))
    return t


# ---------------------------------------------------------------------------
# Numeracion de paginas y cabecera / pie corporativo
# ---------------------------------------------------------------------------

class _NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_page_number(num_pages)
            super().showPage()
        super().save()

    def _draw_page_number(self, page_count):
        page_num = self._pageNumber
        self.setFont("Helvetica", 7.5)
        self.setFillColor(INK_MUTED)
        self.drawRightString(
            PAGE_W - MARGIN,
            0.8 * cm,
            f"{page_num} / {page_count}",
        )


def _cover_background(c, doc):
    """Fondo de portada en navy."""
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Circulo decorativo
    c.setFillColor(HexColor("#2E4066"))
    c.circle(PAGE_W - 3 * cm, PAGE_H - 2 * cm, 6 * cm, fill=1, stroke=0)
    c.setFillColor(COPPER)
    c.circle(PAGE_W - 1 * cm, 3 * cm, 3.5 * cm, fill=1, stroke=0)
    c.restoreState()


def _normal_background(c, doc):
    """Fondo blanco con franja superior de color primario."""
    c.saveState()
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(PRIMARY)
    c.rect(0, PAGE_H - 0.6 * cm, PAGE_W, 0.6 * cm, fill=1, stroke=0)
    # Footer
    c.setFillColor(HexColor("#F3F4F6"))
    c.rect(0, 0, PAGE_W, 1.2 * cm, fill=1, stroke=0)
    c.setFont("Helvetica", 7)
    c.setFillColor(INK_MUTED)
    c.drawString(MARGIN, 0.45 * cm, FOOTER_TXT[:120])
    c.restoreState()


# ---------------------------------------------------------------------------
# Constructor principal
# ---------------------------------------------------------------------------

def build_pitch_pdf(
    output_path: Path,
    company_name: str,
    sector: str,
    pitch: dict,
    meeting_brief: dict | None = None,
    model_output: dict | None = None,
) -> Path:
    """
    Genera el pitchbook en PDF y lo guarda en output_path.
    Devuelve la ruta del fichero generado.
    """
    meeting_brief = meeting_brief or {}
    model_output  = model_output  or {}
    indicadores   = model_output.get("indicadores_clave") or []
    tendencias    = model_output.get("tendencias_estructurales") or []
    interpretacion = _safe(model_output.get("interpretacion"),
                           "El equipo comercial completara la interpretacion durante la preparacion.")

    titulo         = _safe(pitch.get("titulo"),         f"Propuesta comercial - {company_name}")
    subtitulo      = _safe(pitch.get("subtitulo"),       "")
    oportunidad    = _safe(pitch.get("oportunidad_detectada"), "Oportunidad identificada en este sector.")
    contexto_fin   = pitch.get("contexto_financiero")  or []
    encaje_prod    = pitch.get("encaje_productos")      or []
    comparables    = pitch.get("comparables")           or []
    argumentos_val = pitch.get("argumentos_valor")      or []
    proximos_pasos = pitch.get("proximos_pasos")        or ["Agendar reunion de seguimiento."]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    story = []

    # =========================================================================
    # PAGINA 1: Portada
    # =========================================================================
    cover_frame = Frame(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN,
                        id="cover", showBoundary=0)
    cover_tpl   = PageTemplate(id="cover_tpl", frames=[cover_frame],
                                onPage=_cover_background)

    normal_frame = Frame(MARGIN, 1.5 * cm, PAGE_W - 2 * MARGIN, PAGE_H - MARGIN - 1.5 * cm,
                         id="normal", showBoundary=0)
    normal_tpl   = PageTemplate(id="normal_tpl", frames=[normal_frame],
                                 onPage=_normal_background)

    doc = BaseDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        pageTemplates=[cover_tpl, normal_tpl],
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN,  bottomMargin=MARGIN,
    )

    # -- Portada --
    story.append(Spacer(1, 3 * cm))
    if sector:
        story.append(_p(sector.upper(), _style("sect_pill", fontSize=10, textColor=COPPER,
                                                fontName="Helvetica-Bold", spaceAfter=12)))
    story.append(_p(titulo, S_TITLE_COVER))
    if subtitulo:
        story.append(_p(subtitulo, S_SUB_COVER))
    story.append(Spacer(1, 1.5 * cm))
    story.append(_p(f"{BANK_NAME}  ·  Corporate & Deal Intelligence  ·  Documento de uso interno",
                    _style("cover_footer", fontSize=9, textColor=HexColor("#8C99BA"))))

    # =========================================================================
    # PAGINA 2: Oportunidad detectada
    # =========================================================================
    from reportlab.platypus import NextPageTemplate, PageBreak
    story.append(NextPageTemplate("normal_tpl"))
    story.append(PageBreak())

    story.append(_p("1 · OPORTUNIDAD DETECTADA", S_EYEBROW))
    story.append(_p(company_name, S_H1))
    story.append(_hr(PRIMARY, thickness=1.5))
    story.append(_p(oportunidad, S_BODY))
    story.append(Spacer(1, 0.5 * cm))

    if proximos_pasos:
        story.append(_label("Proxima accion"))
        story.append(_p(proximos_pasos[0],
                        _style("next_action", fontSize=11, textColor=NAVY,
                               fontName="Helvetica-Oblique", leading=16)))

    # =========================================================================
    # PAGINA 3: Contexto financiero
    # =========================================================================
    story.append(PageBreak())
    story.append(_p("2 · CONTEXTO FINANCIERO", S_EYEBROW))
    story.append(_p("Lo que dicen los numeros", S_H1))
    story.append(_hr(PRIMARY, thickness=1.5))

    if indicadores:
        story.append(_kpi_table(indicadores))
        story.append(Spacer(1, 0.4 * cm))
    elif contexto_fin:
        for punto in contexto_fin[:4]:
            story.append(_bullet(punto))
        story.append(Spacer(1, 0.3 * cm))

    if tendencias:
        story.append(_label("Tendencias estructurales"))
        for t in tendencias:
            story.append(_bullet(t))
        story.append(Spacer(1, 0.3 * cm))

    story.append(_label("Interpretacion"))
    story.append(Table(
        [[_p(interpretacion, _style("interp", fontSize=10, textColor=white,
                                    fontName="Helvetica-Oblique", leading=15))]],
        colWidths=[PAGE_W - 2 * MARGIN],
        style=TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), NAVY),
            ("TOPPADDING",   (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 12),
            ("LEFTPADDING",  (0, 0), (-1, -1), 16),
            ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ])
    ))

    # =========================================================================
    # PAGINA 4: Briefing de cliente
    # =========================================================================
    story.append(PageBreak())
    story.append(_p("3-4 · BRIEFING DE CLIENTE", S_EYEBROW))
    story.append(_p("Perfil y situacion actual", S_H1))
    story.append(_hr(PRIMARY, thickness=1.5))

    perfil    = _safe(meeting_brief.get("perfil"),
                      f"{company_name} es una de las oportunidades priorizadas.")
    situacion = _safe(meeting_brief.get("situacion_actual"), "")

    story.append(_p(perfil, S_BODY))
    if situacion:
        story.append(_p(situacion, S_BODY_MUTED))
    story.append(Spacer(1, 0.4 * cm))

    necesidades = meeting_brief.get("necesidades_potenciales") or ["Por definir con el equipo comercial."]
    riesgos     = meeting_brief.get("riesgos") or ["Sin riesgos identificados con la informacion disponible."]
    story.append(_two_col_table(necesidades[:4], riesgos[:4],
                                "Necesidades potenciales", "Riesgos y puntos de atencion"))

    talking_points = meeting_brief.get("talking_points") or []
    if talking_points:
        story.append(Spacer(1, 0.3 * cm))
        story.append(_label("Talking points para la reunion"))
        for tp in talking_points[:5]:
            story.append(_bullet(tp))

    # =========================================================================
    # PAGINA 5: Encaje y comparables
    # =========================================================================
    story.append(PageBreak())
    story.append(_p("4 · ENCAJE Y COMPARABLES", S_EYEBROW))
    story.append(_p("Como podemos ayudar", S_H1))
    story.append(_hr(PRIMARY, thickness=1.5))

    # Dos columnas: productos + comparables
    left_prods = []
    if encaje_prod:
        left_prods.append(_label("Encaje con productos del banco"))
        for i, prod in enumerate(encaje_prod[:4]):
            left_prods.append(_p(f"{i+1}.  {prod}", S_BODY))
    left_prods.append(Spacer(1, 0.3 * cm))

    right_comps = []
    if comparables:
        right_comps.append(_label("Comparables sectoriales"))
        for comp in comparables[:3]:
            right_comps.append(_bullet(comp))

    max_r = max(len(left_prods), len(right_comps))
    while len(left_prods)  < max_r: left_prods.append(Spacer(1, 1))
    while len(right_comps) < max_r: right_comps.append(Spacer(1, 1))

    col_w = (PAGE_W - 2 * MARGIN) / 2 - 0.3 * cm
    prod_table = Table(
        [[left_prods[i], right_comps[i]] for i in range(max_r)],
        colWidths=[col_w, col_w],
    )
    prod_table.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    story.append(prod_table)

    if argumentos_val:
        story.append(Spacer(1, 0.4 * cm))
        story.append(_label("Argumentos de valor"))
        arg_cells = [[_p(a, _style("arg", fontSize=10, leading=14))]
                     for a in argumentos_val[:3]]
        arg_col_w = (PAGE_W - 2 * MARGIN) / 3 - 0.3 * cm
        args_table = Table(
            [[ _p(a, _style("arg", fontSize=10, leading=14)) for a in argumentos_val[:3] ]],
            colWidths=[arg_col_w] * min(len(argumentos_val), 3),
        )
        args_table.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), SAND),
            ("BOX",          (0, 0), (-1, -1), 0.5, BORDER),
            ("INNERGRID",    (0, 0), (-1, -1), 0.3, BORDER),
            ("TOPPADDING",   (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
            ("LEFTPADDING",  (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(args_table)

    # =========================================================================
    # PAGINA 6: Proximos pasos
    # =========================================================================
    story.append(NextPageTemplate("cover_tpl"))
    story.append(PageBreak())

    story.append(Spacer(1, 2 * cm))
    story.append(_p("Proximos pasos", S_TITLE_COVER))
    story.append(_p(
        "El equipo comercial revisa, ajusta y personaliza esta propuesta "
        "antes de cualquier interaccion con el cliente.",
        _style("sub_closing", fontSize=13, textColor=HexColor("#C9D2E6"),
               fontName="Helvetica-Oblique", leading=18, spaceAfter=20)
    ))
    story.append(_hr(COPPER, thickness=1))
    story.append(Spacer(1, 0.5 * cm))

    for i, paso in enumerate(proximos_pasos[:4]):
        story.append(_p(
            f"{i+1}.   {paso}",
            _style(f"paso{i}", fontSize=14, textColor=white,
                   fontName="Helvetica", leading=22, spaceAfter=12)
        ))

    story.append(Spacer(1, 1.5 * cm))
    story.append(_p(
        f"{BANK_NAME}  ·  Corporate & Deal Intelligence  ·  Documento de uso interno",
        _style("closing_footer", fontSize=9, textColor=HexColor("#8C99BA"),
               alignment=TA_CENTER)
    ))

    # =========================================================================
    doc.build(story, canvasmaker=_NumberedCanvas)
    return output_path