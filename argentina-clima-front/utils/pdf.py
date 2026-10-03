"""
utils/pdf.py
==============

Genera un PDF tipo informe (hoja A4) a partir del texto en Markdown de
Conclusiones, para descargar desde la app. No inventa ni resume nada:
convierte a otro formato el mismo texto que ya se muestra en pantalla.
"""

import re
from datetime import date
from pathlib import Path

import markdown as md_lib
from fpdf import FPDF

FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"


def _sin_tags_anidados_en_celdas(html: str) -> str:
    """fpdf2.write_html no soporta tags anidados dentro de <td> (ej. **negrita**
    dentro de una celda de tabla markdown) — saca esas etiquetas y deja el
    texto plano, sin tocar el resto del HTML."""
    def limpiar(m):
        contenido = re.sub(r"</?(strong|em|b|i)>", "", m.group(1))
        return f"<td>{contenido}</td>"
    return re.sub(r"<td>(.*?)</td>", limpiar, html, flags=re.DOTALL)


def generar_pdf_conclusiones(texto_markdown: str, titulo: str = "Conclusiones") -> bytes:
    """Devuelve los bytes de un PDF A4 con `texto_markdown` convertido a HTML
    y renderizado como informe (título, fecha, cuerpo con encabezados,
    listas, negritas y tablas). Usa DejaVu Sans (no las fuentes core de PDF,
    que no soportan tildes, ñ, °, ² ni rayas largas — el texto real del
    proyecto las usa todas).

    Todo el HTML (encabezado + cuerpo) se renderiza en UN solo write_html():
    llamar dos veces seguidas a multi_cell/write_html con texto acentuado
    dispara un bug conocido de fpdf2 2.8.x ('Not enough horizontal space to
    render a single character') — un único llamado lo evita."""
    cuerpo_html = md_lib.markdown(texto_markdown, extensions=["tables"])
    cuerpo_html = _sin_tags_anidados_en_celdas(cuerpo_html)
    fecha = date.today().strftime("%d/%m/%Y")
    encabezado_html = (
        f"<h1>{titulo}</h1>"
        f"<p style=\"color:#6e6e6e; font-size: 9pt;\">"
        f"Proyecto: cambio climático y economía en Argentina — generado el {fecha}</p>"
        f"<hr>"
    )

    pdf = FPDF(format="A4", unit="mm")
    pdf.add_font("DejaVu", "", str(FONTS_DIR / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", str(FONTS_DIR / "DejaVuSans-Bold.ttf"))
    pdf.add_font("DejaVu", "I", str(FONTS_DIR / "DejaVuSans-Oblique.ttf"))
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    pdf.set_font("DejaVu", "", 11)

    pdf.write_html(encabezado_html + cuerpo_html)

    return bytes(pdf.output())
