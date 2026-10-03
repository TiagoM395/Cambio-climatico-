"""
streamlit_app.py — Entry point.

Front del proyecto "Análisis del cambio climático y su relación con el
crecimiento económico en Argentina". Presenta, navegable por etapas, todo
lo construido en el proyecto de análisis (argentina-clima-pbi), leyendo
únicamente datos ya generados y reales (copiados en data_front/). No
recalcula ni inventa nada.
"""

import streamlit as st

from utils.ui import inyectar_estilos

st.set_page_config(
    page_title="Clima y economía — Argentina",
    page_icon=":material/thermostat:",
    layout="wide",
)
inyectar_estilos()

page = st.navigation(
    {
        "": [
            st.Page("app_pages/inicio.py", title="Inicio", icon=":material/home:", default=True),
            st.Page("app_pages/respuesta.py", title="Respuesta a la pregunta", icon=":material/question_answer:"),
        ],
        "El proyecto": [
            st.Page("app_pages/fuentes.py", title="Fuentes de datos", icon=":material/database:"),
            st.Page("app_pages/dataset.py", title="Datos descargados", icon=":material/table_chart:"),
        ],
        "Análisis": [
            st.Page("app_pages/nacional.py", title="Análisis nacional", icon=":material/public:"),
            st.Page("app_pages/provincial.py", title="Análisis provincial", icon=":material/map:"),
            st.Page("app_pages/mapas.py", title="Mapas", icon=":material/travel_explore:"),
            st.Page("app_pages/correlaciones.py", title="Clima y economía", icon=":material/insights:"),
        ],
        "Modelos y proyecciones": [
            st.Page("app_pages/modelos.py", title="Modelos predictivos", icon=":material/model_training:"),
            st.Page("app_pages/escenarios.py", title="Escenarios futuros", icon=":material/timeline:"),
        ],
        "Explorar": [
            st.Page("app_pages/explorador.py", title="Explorador interactivo", icon=":material/tune:"),
        ],
        "Cierre": [
            st.Page("app_pages/conclusiones.py", title="Conclusiones", icon=":material/fact_check:"),
            st.Page("app_pages/checklist.py", title="Checklist del proyecto", icon=":material/checklist:"),
        ],
    },
    position="sidebar",
)

with st.sidebar:
    st.caption(
        "Datos reales, de fuentes oficiales, documentados en "
        "**Fuentes de datos**. Ningún valor es inventado."
    )

page.run()
