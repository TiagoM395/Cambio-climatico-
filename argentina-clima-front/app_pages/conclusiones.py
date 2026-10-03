"""Conclusiones finales, tal como quedaron redactadas en el proyecto (sección 36).
Mostradas como hoja A4 (estilo informe) y descargables en PDF."""

import streamlit as st

from utils.datos import leer_markdown
from utils.pdf import generar_pdf_conclusiones
from utils.ui import acordeon_pagina, glosario_markdown

st.header(":material/fact_check: Conclusiones")
acordeon_pagina("conclusiones")
st.caption("Contenido íntegro de CONCLUSIONES.md del proyecto argentina-clima-pbi, sin editar; al final se agrega un glosario.")

texto_md = leer_markdown("CONCLUSIONES.md") + "\n\n---\n\n" + glosario_markdown()


@st.cache_data
def _pdf_conclusiones(texto: str) -> bytes:
    return generar_pdf_conclusiones(texto, titulo="Conclusiones")


st.download_button(
    ":material/download: Descargar como PDF",
    data=_pdf_conclusiones(texto_md),
    file_name="conclusiones_cambio_climatico_argentina.pdf",
    mime="application/pdf",
)

st.markdown(f'<div class="hoja-informe">\n\n{texto_md}\n\n</div>', unsafe_allow_html=True)
