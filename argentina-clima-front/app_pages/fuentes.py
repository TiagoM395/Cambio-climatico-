"""Etapas 1-3: inspección, estructura y fuentes de datos reales."""

import streamlit as st

from utils.datos import cargar_fuentes, cargar_tabla
from utils.ui import acordeon_pagina, explicacion

st.header(":material/database: Fuentes de datos")
acordeon_pagina("fuentes")
st.markdown(
    "El proyecto usa **13 fuentes reales**, verificadas por acceso directo "
    "(no solo enlaces de una búsqueda), documentadas con nombre, dirección, "
    "institución, variable, unidad, cobertura, metodología y limitaciones "
    "(proyecto.txt, sección 4)."
)

fuentes = cargar_fuentes()
conteo = cargar_tabla("conteo_datasets.csv")

st.subheader("Cantidad de filas de cada dataset descargado")
st.dataframe(
    conteo[conteo["tipo"] == "descargado"].rename(
        columns={"dataset": "Dataset", "fuente": "Fuente", "periodo": "Período", "filas": "Filas", "unidad": "Unidad"}
    ).drop(columns="tipo"),
    hide_index=True, height="content",
)
st.caption("Filas contadas directamente sobre los archivos descargados (src/conteo_datasets.py).")


def _filas_de(claves: str) -> str:
    """Cantidad de filas de los archivos de una fuente, tomadas del conteo real."""
    if not isinstance(claves, str) or not claves.strip():
        return "no se descargó (se cita solo como referencia)"
    partes = []
    for clave in [c.strip() for c in claves.split("|")]:
        r = conteo[conteo["dataset"] == clave]
        if len(r):
            n = f"{int(r.iloc[0]['filas']):,}".replace(",", ".")
            partes.append(f"{n} filas ({r.iloc[0]['unidad']})" if len(claves.split("|")) == 1 else f"{clave}: {n} filas")
    return " · ".join(partes) if partes else "sin dato"


st.space("medium")
st.subheader("Cada dataset: qué es, por qué se usa y para qué sirve")
explicacion(
    "Una ficha por dataset, con su cantidad de filas, el período que cubre, la institución que lo publica, por qué se eligió esa fuente "
    "y para qué análisis se usa. Son fichas y no una tabla porque los nombres y las explicaciones son largos y una grilla los cortaría."
)
for _, fila in fuentes.iterrows():
    with st.container(border=True):
        st.markdown(f"**{fila['nombre_fuente']}**")
        st.caption(f"{fila['institucion']}")
        st.markdown(
            f"**Cantidad de datos:** {_filas_de(fila.get('conteo_claves'))}  \n"
            f"**Período:** {fila['cobertura_temporal']}  \n"
            f"**Alcance geográfico:** {fila['cobertura_geografica']}  \n"
            f"**Frecuencia de publicación:** {fila['frecuencia']}"
        )
        st.markdown(f"**Por qué se usa:** {fila.get('por_que', '')}")
        st.markdown(f"**Para qué sirve:** {fila.get('para_que', '')}")
        st.markdown(f"**Qué mide y en qué unidad:** {fila['variable']} ({fila['unidad']}).")
        st.caption(f"Limitaciones: {fila['limitaciones']}")
        st.caption(f"Dirección: {fila['url']}")

st.space("medium")
st.subheader("Problemas reales resueltos durante la búsqueda")
st.markdown(
    """
- `smn.gob.ar` bloquea accesos automatizados (403) → se usó CIAM (Centro de Información Ambiental), que republica los mismos datos del SMN.
- OWID no tiene a Argentina en su gráfico de temperatura por país → se adoptó NASA POWER (reanálisis satelital), documentando la limitación.
- INDEC discontinuó el PBG provincial oficial en 2017 (falta de Censo Económico actualizado) → se adoptó la actualización de CEPAL (2004-2024).
- El Inventario Nacional de GEI solo llega a 2022 (rezago estructural de 2-3 años en este tipo de reportes en todo el mundo, no una falla de búsqueda).
"""
)
