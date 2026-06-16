"""
docx_builder.py
=================
Genera el informe de riesgo KYC en formato .docx a partir del markdown
producido por el Credit Risk Report Agent, con colores y logo del cliente.

Dependencias: pip install python-docx
"""

import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor as DocxRGB
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from config import BankConfig


def _rgb(hex_color: str) -> DocxRGB:
    h = hex_color.lstrip("#")
    return DocxRGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _clean(text: str) -> str:
    """Quita marcadores markdown y normaliza guiones."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*",     r"\1", text)
    text = re.sub(r"`(.*?)`",       r"\1", text)
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    return text.strip()


def _paragraph_border_bottom(para, hex_color: str, size: int = 6):
    """Pone un borde inferior a un parrafo."""
    pPr  = para._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot  = OxmlElement("w:bottom")
    bot.set(qn("w:val"),   "single")
    bot.set(qn("w:sz"),    str(size))
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), hex_color.lstrip("#"))
    pBdr.append(bot)
    pPr.append(pBdr)


def build_informe_docx(output_path: Path, entity_name: str, informe_md: str) -> Path:
    """
    Genera el .docx del informe y lo guarda en output_path.
    Devuelve la ruta del fichero generado.
    """
    primary   = BankConfig.COLOR_PRIMARY
    ink       = BankConfig.COLOR_INK
    muted     = BankConfig.COLOR_INK_MUTED

    doc = Document()

    # Margenes A4
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3.0)
        section.right_margin  = Cm(3.0)

    # Estilo base
    normal = doc.styles["Normal"]
    normal.font.name      = "Arial"
    normal.font.size      = Pt(11)
    normal.font.color.rgb = _rgb(ink)

    # ---- Cabecera ----
    bank_p = doc.add_paragraph()
    bank_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = bank_p.add_run(BankConfig.BANK_NAME.upper())
    r.font.name = "Arial"; r.font.size = Pt(9); r.bold = True
    r.font.color.rgb = _rgb(muted)

    title_p = doc.add_heading("", level=0)
    r = title_p.add_run("Informe de riesgo")
    r.font.name = "Arial"; r.font.size = Pt(22); r.bold = True
    r.font.color.rgb = _rgb(primary)

    if entity_name:
        sub_p = doc.add_paragraph()
        r = sub_p.add_run(entity_name)
        r.font.name = "Arial"; r.font.size = Pt(16); r.bold = True
        r.font.color.rgb = _rgb(ink)

    sep = doc.add_paragraph()
    sep.paragraph_format.space_after = Pt(4)
    _paragraph_border_bottom(sep, primary, size=6)
    doc.add_paragraph()

    # ---- Cuerpo: parseo del markdown ----
    for raw_line in informe_md.splitlines():
        line = raw_line.rstrip()
        line = line.replace("\u2014", "-").replace("\u2013", "-")

        if not line:
            doc.add_paragraph()
            continue

        if line.startswith("# "):
            h = doc.add_heading(_clean(line[2:]), level=1)
            for r in h.runs:
                r.font.name = "Arial"; r.font.size = Pt(16)
                r.font.color.rgb = _rgb(primary)
            h.paragraph_format.space_before = Pt(18)
            h.paragraph_format.space_after  = Pt(6)

        elif line.startswith("## "):
            h = doc.add_heading(_clean(line[3:]), level=2)
            for r in h.runs:
                r.font.name = "Arial"; r.font.size = Pt(13)
                r.font.color.rgb = _rgb(ink)
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after  = Pt(4)

        elif line.startswith("### "):
            h = doc.add_heading(_clean(line[4:]), level=3)
            for r in h.runs:
                r.font.name = "Arial"; r.font.size = Pt(11.5)
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after  = Pt(3)

        elif line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            r = p.add_run(_clean(line[2:]))
            r.font.name = "Arial"; r.font.size = Pt(11)

        elif re.match(r"^\d+\.\s", line):
            p = doc.add_paragraph(style="List Number")
            r = p.add_run(_clean(re.sub(r"^\d+\.\s", "", line)))
            r.font.name = "Arial"; r.font.size = Pt(11)

        else:
            # Parrafo normal con soporte de **negrita**
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            parts = re.split(r"(\*\*.*?\*\*)", line)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                else:
                    r = p.add_run(part)
                r.font.name = "Arial"; r.font.size = Pt(11)
                r.font.color.rgb = _rgb(ink)

    # ---- Pie ----
    doc.add_paragraph()
    fp = doc.add_paragraph()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run(BankConfig.FOOTER_TEXT)
    r.font.name = "Arial"; r.font.size = Pt(8.5); r.italic = True
    r.font.color.rgb = _rgb(muted)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path