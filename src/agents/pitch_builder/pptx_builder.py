"""
src/agents/pitch_builder/pptx_builder.py
===========================================
Generador del pitchbook .pptx para el Pitch Builder Agent.

6 diapositivas, 16:9, paleta "Deal Room":
  - Navy #1B2A4A  + arena #EDE6D9  + cobre #C97B4A
  - Tipografia Cambria (display) + Calibri (cuerpo)

Uso:
    from src.agents.pitch_builder.pptx_builder import build_pitch_deck
    build_pitch_deck(output_path, company_name, sector, pitch, meeting_brief, model_output)
"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------------------------------------------------------------------------
# Paleta "Deal Room"
# ---------------------------------------------------------------------------
NAVY        = RGBColor(0x1B, 0x2A, 0x4A)
NAVY_LIGHT  = RGBColor(0x2E, 0x40, 0x66)
SAND        = RGBColor(0xED, 0xE6, 0xD9)
SAND_DARK   = RGBColor(0xDD, 0xD2, 0xBE)
COPPER      = RGBColor(0xC9, 0x7B, 0x4A)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
INK         = RGBColor(0x22, 0x2A, 0x39)
INK_MUTED   = RGBColor(0x6B, 0x73, 0x85)
LAVENDER    = RGBColor(0xC9, 0xD2, 0xE6)
MUTED_NAVY  = RGBColor(0x8C, 0x99, 0xBA)

FONT_DISPLAY = "Cambria"
FONT_BODY    = "Calibri"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


# ---------------------------------------------------------------------------
# Helpers de bajo nivel
# ---------------------------------------------------------------------------

def _add_bg(slide, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    sp = shape._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)
    return shape


def _add_text(slide, x, y, w, h, text, size, color, bold=False, italic=False,
               font=FONT_BODY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
               line_spacing=None):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, line in enumerate(str(text).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.italic = italic
        run.font.name = font
    return tb


def _add_bullets(slide, x, y, w, h, items, size, color, font=FONT_BODY,
                  space_after=8, line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        run = p.add_run()
        run.text = "\u2014  " + item
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.name = font
    return tb


def _add_pill(slide, x, y, w, h, text, fill_color, text_color, size=12, bold=True):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.adjustments[0] = 0.5
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = Pt(4)
    tf.margin_right = Pt(4)
    tf.margin_top = Pt(0)
    tf.margin_bottom = Pt(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = text_color
    run.font.name = FONT_BODY
    return shape


def _add_circle_icon(slide, x, y, d, fill_color, glyph, glyph_color, glyph_size=18):
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, d, d)
    circle.fill.solid()
    circle.fill.fore_color.rgb = fill_color
    circle.line.fill.background()
    circle.shadow.inherit = False
    tf = circle.text_frame
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = glyph
    run.font.size = Pt(glyph_size)
    run.font.bold = True
    run.font.color.rgb = glyph_color
    run.font.name = FONT_BODY
    return circle


def _add_card(slide, x, y, w, h, fill_color=WHITE, line_color=None, shadow=True, radius=0.06):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.adjustments[0] = radius
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(0.75)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    if shadow:
        el = shape._element.spPr
        effect_lst = el.makeelement(qn('a:effectLst'), {})
        outer_shdw = el.makeelement(qn('a:outerShdw'), {
            'blurRad': '90000', 'dist': '50000', 'dir': '5400000', 'rotWithShape': '0'
        })
        srgb = el.makeelement(qn('a:srgbClr'), {'val': '1B2A4A'})
        alpha = el.makeelement(qn('a:alpha'), {'val': '18000'})
        srgb.append(alpha)
        outer_shdw.append(srgb)
        effect_lst.append(outer_shdw)
        el.append(effect_lst)
    return shape


def _section_header(slide, number, label):
    _add_circle_icon(slide, Inches(0.7), Inches(0.65), Inches(0.5), NAVY, str(number), WHITE, 18)
    _add_text(slide, Inches(1.35), Inches(0.6), Inches(10), Inches(0.6),
              label.upper(), 14, NAVY, bold=True, font=FONT_BODY, anchor=MSO_ANCHOR.MIDDLE)


def _footer(slide, dark=False):
    color = MUTED_NAVY if dark else INK_MUTED
    _add_text(slide, Inches(0.7), Inches(7.0), Inches(9), Inches(0.35),
              "Corporate & Deal Intelligence  \u00b7  Documento de uso interno",
              10.5, color, font=FONT_BODY)


def _safe(value, fallback=""):
    if value is None:
        return fallback
    if isinstance(value, str) and not value.strip():
        return fallback
    return value


# ---------------------------------------------------------------------------
# Constructor principal
# ---------------------------------------------------------------------------

def build_pitch_deck(
    output_path: Path,
    company_name: str,
    sector: str,
    pitch: dict,
    meeting_brief: dict | None = None,
    model_output: dict | None = None,
) -> Path:
    """
    Genera el pitchbook .pptx y lo guarda en output_path. Devuelve la ruta.
    """
    meeting_brief = meeting_brief or {}
    model_output  = model_output  or {}
    indicadores   = model_output.get("indicadores_clave") or []
    tendencias    = model_output.get("tendencias_estructurales") or []
    interpretacion = _safe(
        model_output.get("interpretacion"),
        "El equipo comercial completar\u00e1 la interpretaci\u00f3n financiera "
        "durante la preparaci\u00f3n de la reuni\u00f3n.",
    )

    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    titulo          = _safe(pitch.get("titulo"), f"Propuesta comercial \u2014 {company_name}")
    subtitulo       = _safe(pitch.get("subtitulo"), "")
    oportunidad     = _safe(pitch.get("oportunidad_detectada"),
                            "Oportunidad identificada en este sector. "
                            "Los detalles se completar\u00e1n durante la preparaci\u00f3n de la reuni\u00f3n.")
    contexto_fin    = pitch.get("contexto_financiero") or []
    encaje_prod     = pitch.get("encaje_productos")    or []
    comparables     = pitch.get("comparables")         or []
    argumentos_val  = pitch.get("argumentos_valor")    or []
    proximos_pasos  = pitch.get("proximos_pasos")      or ["Agendar reuni\u00f3n de seguimiento con el cliente."]

    # =====================================================================
    # SLIDE 1 -- Portada
    # =====================================================================
    s = prs.slides.add_slide(blank)
    _add_bg(s, NAVY)

    # Motivo decorativo: dos circulos superpuestos (sin stripes)
    c1 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.6), Inches(-1.2), Inches(4.2), Inches(4.2))
    c1.fill.solid(); c1.fill.fore_color.rgb = NAVY_LIGHT; c1.line.fill.background(); c1.shadow.inherit = False
    c2 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(11.6), Inches(4.6), Inches(2.6), Inches(2.6))
    c2.fill.solid(); c2.fill.fore_color.rgb = COPPER; c2.line.fill.background(); c2.shadow.inherit = False

    if sector:
        _add_pill(s, Inches(0.7), Inches(0.7), Inches(2.0), Inches(0.42),
                  sector.upper(), COPPER, WHITE, size=12)

    title_size = 40 if len(titulo) <= 70 else 32
    _add_text(s, Inches(0.7), Inches(2.5), Inches(11.5), Inches(2.4),
              titulo, title_size, WHITE, bold=True, font=FONT_DISPLAY, line_spacing=1.08)

    if subtitulo:
        _add_text(s, Inches(0.7), Inches(4.9), Inches(10.8), Inches(1.0),
                  subtitulo, 18, LAVENDER, italic=True, font=FONT_BODY, line_spacing=1.25)

    _footer(s, dark=True)

    # =====================================================================
    # SLIDE 2 -- Oportunidad detectada
    # =====================================================================
    s = prs.slides.add_slide(blank)
    _add_bg(s, SAND)
    _section_header(s, 1, "Oportunidad detectada")

    _add_text(s, Inches(0.7), Inches(1.5), Inches(7.5), Inches(0.9),
              company_name, 28, INK, bold=True, font=FONT_DISPLAY)
    _add_text(s, Inches(0.7), Inches(2.35), Inches(7.5), Inches(2.7),
              oportunidad, 15, INK, font=FONT_BODY, line_spacing=1.35)

    if proximos_pasos:
        _add_text(s, Inches(0.7), Inches(5.7), Inches(7.5), Inches(0.4),
                  "PR\u00d3XIMA ACCI\u00d3N", 11, INK_MUTED, bold=True, font=FONT_BODY)
        _add_text(s, Inches(0.7), Inches(6.05), Inches(7.5), Inches(1.0),
                  proximos_pasos[0], 14, NAVY, italic=True, font=FONT_BODY, line_spacing=1.25)

    # Tarjeta lateral: cifra + sector + prioridad
    _add_card(s, Inches(8.6), Inches(1.5), Inches(4.0), Inches(5.3), fill_color=WHITE)
    _add_text(s, Inches(9.0), Inches(1.85), Inches(3.3), Inches(0.4),
              "EN UNA CIFRA", 11, INK_MUTED, bold=True, font=FONT_BODY)

    if indicadores:
        first = indicadores[0]
        val = str(first.get("valor", ""))
        val_size = 48 if len(val) <= 8 else 26
        _add_text(s, Inches(9.0), Inches(2.25), Inches(3.3), Inches(1.0),
                  val, val_size, COPPER, bold=True, font=FONT_DISPLAY, line_spacing=1.0)
        _add_text(s, Inches(9.0), Inches(3.35), Inches(3.3), Inches(0.8),
                  first.get("nombre", ""), 13, INK_MUTED, font=FONT_BODY, line_spacing=1.2)
    else:
        _add_text(s, Inches(9.0), Inches(2.25), Inches(3.3), Inches(1.0),
                  "\u2014", 48, COPPER, bold=True, font=FONT_DISPLAY)
        _add_text(s, Inches(9.0), Inches(3.35), Inches(3.3), Inches(0.8),
                  "Sin indicador disponible", 13, INK_MUTED, font=FONT_BODY)

    _add_text(s, Inches(9.0), Inches(4.4), Inches(3.3), Inches(0.4),
              "SECTOR", 11, INK_MUTED, bold=True, font=FONT_BODY)
    _add_text(s, Inches(9.0), Inches(4.7), Inches(3.3), Inches(0.5),
              _safe(sector, "No especificado"), 16, INK, bold=True, font=FONT_DISPLAY)
    _add_text(s, Inches(9.0), Inches(5.4), Inches(3.3), Inches(0.4),
              "PRIORIDAD", 11, INK_MUTED, bold=True, font=FONT_BODY)
    _add_pill(s, Inches(9.0), Inches(5.7), Inches(1.5), Inches(0.42), "ALTA", COPPER, WHITE, size=12)

    _footer(s)

    # =====================================================================
    # SLIDE 3 -- Contexto financiero
    # =====================================================================
    s = prs.slides.add_slide(blank)
    _add_bg(s, WHITE)
    _section_header(s, 2, "Contexto financiero")

    _add_text(s, Inches(0.7), Inches(1.45), Inches(11.9), Inches(0.8),
              "Lo que dicen los n\u00fameros", 28, INK, bold=True, font=FONT_DISPLAY)

    card_w, card_h, gap = Inches(3.85), Inches(2.3), Inches(0.3)
    if indicadores:
        for i, ind in enumerate(indicadores[:3]):
            x = Inches(0.7) + i * (card_w + gap)
            _add_card(s, x, Inches(2.55), card_w, card_h, fill_color=SAND)
            value = str(ind.get("valor", ""))
            val_size = 22 if len(value) > 10 else 36
            _add_text(s, x + Inches(0.3), Inches(2.8), card_w - Inches(0.6), Inches(0.9),
                      value, val_size, NAVY, bold=True, font=FONT_DISPLAY, line_spacing=1.0)
            _add_text(s, x + Inches(0.3), Inches(4.15), card_w - Inches(0.6), Inches(0.7),
                      ind.get("nombre", ""), 13, INK_MUTED, font=FONT_BODY, line_spacing=1.15)
    elif contexto_fin:
        _add_card(s, Inches(0.7), Inches(2.55), Inches(11.95), card_h, fill_color=SAND)
        _add_bullets(s, Inches(1.1), Inches(2.85), Inches(11.2), Inches(1.9),
                      contexto_fin[:4], 14, INK, space_after=8)
    else:
        _add_card(s, Inches(0.7), Inches(2.55), Inches(11.95), card_h, fill_color=SAND)
        _add_text(s, Inches(1.1), Inches(3.4), Inches(11.2), Inches(0.6),
                  "No se han recibido indicadores financieros estructurados para esta oportunidad.",
                  14, INK_MUTED, italic=True, font=FONT_BODY)

    if tendencias:
        _add_text(s, Inches(0.7), Inches(5.2), Inches(5.8), Inches(0.4),
                  "TENDENCIAS ESTRUCTURALES", 11, INK_MUTED, bold=True, font=FONT_BODY)
        _add_bullets(s, Inches(0.7), Inches(5.6), Inches(5.8), Inches(1.6),
                      tendencias[:4], 13, INK, space_after=6)
    elif not indicadores and contexto_fin:
        _add_text(s, Inches(0.7), Inches(5.2), Inches(5.8), Inches(0.4),
                  "RESUMEN", 11, INK_MUTED, bold=True, font=FONT_BODY)
        _add_text(s, Inches(0.7), Inches(5.6), Inches(5.8), Inches(1.4),
                  "Datos de contexto recopilados por el Earnings Reviewer Agent (ver tarjeta superior).",
                  13, INK_MUTED, italic=True, font=FONT_BODY, line_spacing=1.3)

    _add_card(s, Inches(6.85), Inches(5.2), Inches(5.75), Inches(1.9), fill_color=NAVY)
    _add_text(s, Inches(7.2), Inches(5.42), Inches(5.1), Inches(0.4),
              "INTERPRETACI\u00d3N", 11, LAVENDER, bold=True, font=FONT_BODY)
    _add_text(s, Inches(7.2), Inches(5.8), Inches(5.1), Inches(1.2),
              interpretacion, 13, WHITE, italic=True, font=FONT_BODY, line_spacing=1.25)

    _footer(s)

    # =====================================================================
    # SLIDE 4 -- Briefing de cliente
    # =====================================================================
    s = prs.slides.add_slide(blank)
    _add_bg(s, WHITE)
    _section_header(s, 3, "Briefing de cliente")

    _add_text(s, Inches(0.7), Inches(1.45), Inches(11.9), Inches(0.8),
              "Perfil y situaci\u00f3n actual", 28, INK, bold=True, font=FONT_DISPLAY)

    perfil    = _safe(meeting_brief.get("perfil"),
                       f"{company_name} es una de las oportunidades priorizadas para este sector.")
    situacion = _safe(meeting_brief.get("situacion_actual"), "")

    _add_text(s, Inches(0.7), Inches(2.35), Inches(11.9), Inches(0.9),
              perfil, 14, INK, font=FONT_BODY, line_spacing=1.3)
    if situacion:
        _add_text(s, Inches(0.7), Inches(3.15), Inches(11.9), Inches(0.9),
                  situacion, 14, INK_MUTED, italic=True, font=FONT_BODY, line_spacing=1.3)

    necesidades = meeting_brief.get("necesidades_potenciales") or ["Por definir con el equipo comercial."]
    riesgos     = meeting_brief.get("riesgos") or ["Sin riesgos identificados con la informaci\u00f3n disponible."]

    _add_card(s, Inches(0.7), Inches(4.15), Inches(5.85), Inches(2.95), fill_color=SAND)
    _add_circle_icon(s, Inches(1.0), Inches(4.45), Inches(0.42), NAVY, "+", WHITE, 18)
    _add_text(s, Inches(1.6), Inches(4.45), Inches(4.6), Inches(0.45),
              "NECESIDADES POTENCIALES", 12, NAVY, bold=True, font=FONT_BODY, anchor=MSO_ANCHOR.MIDDLE)
    _add_bullets(s, Inches(1.0), Inches(5.1), Inches(5.3), Inches(1.9),
                  necesidades[:4], 13, INK, space_after=8)

    _add_card(s, Inches(6.8), Inches(4.15), Inches(5.85), Inches(2.95),
               fill_color=WHITE, line_color=SAND_DARK)
    _add_circle_icon(s, Inches(7.1), Inches(4.45), Inches(0.42), COPPER, "!", WHITE, 18)
    _add_text(s, Inches(7.7), Inches(4.45), Inches(4.6), Inches(0.45),
              "RIESGOS Y PUNTOS DE ATENCI\u00d3N", 12, NAVY, bold=True, font=FONT_BODY, anchor=MSO_ANCHOR.MIDDLE)
    _add_bullets(s, Inches(7.1), Inches(5.1), Inches(5.3), Inches(1.9),
                  riesgos[:4], 13, INK, space_after=8)

    # =====================================================================
    # SLIDE 5 -- Encaje, comparables y argumentos de valor
    # =====================================================================
    s = prs.slides.add_slide(blank)
    _add_bg(s, SAND)
    _section_header(s, 4, "Encaje y comparables")

    _add_text(s, Inches(0.7), Inches(1.45), Inches(11.9), Inches(0.8),
              "C\u00f3mo podemos ayudar", 28, INK, bold=True, font=FONT_DISPLAY)

    if encaje_prod:
        _add_text(s, Inches(0.7), Inches(2.45), Inches(7.0), Inches(0.4),
                  "ENCAJE CON PRODUCTOS DEL BANCO", 11, INK_MUTED, bold=True, font=FONT_BODY)
        y = Inches(2.9)
        for i, prod in enumerate(encaje_prod[:4]):
            _add_circle_icon(s, Inches(0.7), y, Inches(0.4), NAVY, str(i + 1), WHITE, 14)
            _add_text(s, Inches(1.3), y, Inches(6.4), Inches(0.55),
                      prod, 13.5, INK, font=FONT_BODY, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1)
            y += Inches(0.72)

    if comparables:
        _add_card(s, Inches(8.1), Inches(2.45), Inches(4.55), Inches(3.5), fill_color=WHITE)
        _add_text(s, Inches(8.45), Inches(2.75), Inches(3.9), Inches(0.4),
                  "COMPARABLES SECTORIALES", 11, INK_MUTED, bold=True, font=FONT_BODY)
        yc = Inches(3.25)
        for comp in comparables[:2]:
            _add_text(s, Inches(8.45), yc, Inches(3.9), Inches(1.5),
                      comp, 12.5, INK, font=FONT_BODY, line_spacing=1.3)
            yc += Inches(1.4)

    if argumentos_val:
        _add_text(s, Inches(0.7), Inches(5.95), Inches(11.9), Inches(0.4),
                  "ARGUMENTOS DE VALOR", 11, INK_MUTED, bold=True, font=FONT_BODY)
        arg_w, arg_h, gap = Inches(3.85), Inches(1.0), Inches(0.3)
        for i, arg in enumerate(argumentos_val[:3]):
            x = Inches(0.7) + i * (arg_w + gap)
            _add_card(s, x, Inches(6.3), arg_w, arg_h, fill_color=WHITE,
                       shadow=False, line_color=SAND_DARK)
            _add_text(s, x + Inches(0.25), Inches(6.43), arg_w - Inches(0.5), Inches(0.75),
                      arg, 11.5, INK, font=FONT_BODY, line_spacing=1.15, anchor=MSO_ANCHOR.MIDDLE)

    # =====================================================================
    # SLIDE 6 -- Proximos pasos (cierre)
    # =====================================================================
    s = prs.slides.add_slide(blank)
    _add_bg(s, NAVY)

    _add_text(s, Inches(0.7), Inches(0.75), Inches(11.9), Inches(0.9),
              "Pr\u00f3ximos pasos", 34, WHITE, bold=True, font=FONT_DISPLAY)
    _add_text(s, Inches(0.7), Inches(1.6), Inches(11.0), Inches(0.6),
              "El equipo comercial revisa, ajusta y personaliza esta propuesta "
              "antes de cualquier interacci\u00f3n con el cliente.",
              15, LAVENDER, italic=True, font=FONT_BODY, line_spacing=1.3)

    y = Inches(2.6)
    for i, step in enumerate(proximos_pasos[:4]):
        _add_circle_icon(s, Inches(0.7), y, Inches(0.55), COPPER, str(i + 1), WHITE, 20)
        _add_text(s, Inches(1.45), y - Inches(0.02), Inches(10.8), Inches(0.95),
                  step, 17, WHITE, font=FONT_BODY, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2)
        y += Inches(1.1)

    _footer(s, dark=True)

    # =====================================================================
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    return output_path