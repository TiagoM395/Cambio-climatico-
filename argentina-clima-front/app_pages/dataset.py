"""Etapa 4: datos descargados, cantidad de filas y unión por año/provincia."""

import plotly.express as px
import streamlit as st

from utils.datos import cargar_dataset_nacional, cargar_dataset_provincial, cargar_tabla
from utils.ui import acordeon_pagina, ayuda, config_columnas, explicacion, para_que, tabla_legible, tarjetas

st.header(":material/table_chart: Datos descargados")
acordeon_pagina("dataset")
st.markdown(
    "Todos los datos se **descargaron** de fuentes oficiales; no se generó ni "
    "inventó ninguno. Lo único que se hace es **unir por año (y por provincia)** "
    "lo descargado en dos tablas de trabajo: **nacional** (1 fila por año) y "
    "**provincial** (1 fila por año-jurisdicción). No se imputan faltantes: si "
    "una fuente no cubre un año o provincia, la celda queda vacía."
)

para_que(
    "Mostrar con exactitud qué datos se descargaron, cuántos registros tiene cada uno y cómo quedan "
    "después de unirlos por año y provincia. Sirve para confiar en los datos."
)
conteo = cargar_tabla("conteo_datasets.csv")
st.subheader("Cantidad de filas de cada dataset")
st.dataframe(
    conteo.rename(columns={"dataset": "Dataset", "fuente": "Fuente", "periodo": "Período", "filas": "Filas", "unidad": "Unidad", "tipo": "Tipo"}),
    hide_index=True, height="content",
)
nacional = cargar_dataset_nacional()
provincial = cargar_dataset_provincial()

tarjetas([
    dict(etiqueta="Dataset nacional", valor=f"{len(nacional)}", unidad="filas, una por año", desc=f"Período {nacional['año'].min()}–{nacional['año'].max()}."),
    dict(etiqueta="Dataset provincial", valor=f"{len(provincial)}", unidad="filas, una por año y jurisdicción", desc=f"{provincial['jurisdiccion'].nunique()} jurisdicciones."),
    dict(etiqueta="Validaciones", valor="0", unidad="duplicados y 0 jurisdicciones inválidas",
         desc="Se comprobó que no haya filas repetidas (mismo año y provincia dos veces) ni nombres de provincia inexistentes."),
])

st.space("medium")

tab1, tab2, tab3 = st.tabs(["Cobertura por variable", "Vista previa nacional", "Vista previa provincial"])

with tab1:
    cobertura = cargar_tabla("informe_cobertura.csv")
    para_que("Ver cuántos datos hay de cada variable: si está completa o le faltan años.")
    st.dataframe(tabla_legible(cobertura), hide_index=True, column_config={
        **config_columnas(cobertura),
        "dataset": st.column_config.Column("Tabla", help="Nacional: una fila por año. Provincial: una fila por año y provincia."),
        "jurisdicciones_con_datos": st.column_config.Column("Provincias con datos", help="En cuántas jurisdicciones esta variable tiene información."),
    })

    fig = px.bar(
        cobertura, x="variable", y="observaciones", color="dataset",
        title="Observaciones disponibles por variable (nacional vs. provincial)",
        labels={"observaciones": "Observaciones", "variable": "Variable"},
        barmode="group",
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, width="stretch")
    explicacion(
        "Barras agrupadas (nacional al lado de provincial) para comparar "
        "cuántos datos hay de cada variable en cada nivel — la tabla de "
        "arriba tiene el mismo dato, pero acá se ve de un vistazo cuál "
        "variable está más completa."
    )

with tab2:
    para_que("Ver la tabla nacional tal cual quedó: una fila por año. Pasá el mouse por cada título de columna para saber qué es.")
    st.dataframe(nacional, hide_index=True, column_config=config_columnas(nacional))

with tab3:
    provincia_sel = st.selectbox("Filtrar por jurisdicción (opcional)", ["(todas)"] + sorted(provincial["jurisdiccion"].unique()))
    df_mostrar = provincial if provincia_sel == "(todas)" else provincial[provincial["jurisdiccion"] == provincia_sel]
    para_que("Ver la tabla provincial: una fila por provincia y año. Pasá el mouse por cada título de columna para saber qué es.")
    st.dataframe(df_mostrar, hide_index=True, column_config=config_columnas(df_mostrar))

st.space("medium")
st.subheader("Problemas reales encontrados al leer los archivos")
st.markdown(
    """
- La hoja de Excel usada para el total nacional de GEI no existía en el archivo que se creía (estaba en otro archivo, para 2010-2022).
- Los años "2023 (2)" y "2024 (2)" de CEPAL venían como texto (nota al pie de "dato preliminar") y se perdían silenciosamente al filtrar solo números.
- NASA POWER usa `-999.0` como código de dato faltante — se filtró explícitamente para que nunca se lea como una temperatura real.
"""
)
