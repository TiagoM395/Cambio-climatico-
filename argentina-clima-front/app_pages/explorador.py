"""Explorador interactivo: elegí provincia(s) y variable, gráficos generados en el momento."""

import plotly.express as px
import streamlit as st

from utils.datos import cargar_dataset_provincial, cargar_dataset_nacional
from utils.ui import ETIQUETAS_VARIABLES, acordeon_pagina, ayuda, explicacion, num, para_que, tarjetas, termino

st.header(":material/tune: Explorador interactivo")
acordeon_pagina("explorador")
st.caption(
    "Todos los gráficos de esta página se generan en vivo a partir de "
    "`dataset_provincial.csv` y `dataset_nacional.csv` — nada está "
    "pregenerado. Elegí los filtros."
)
para_que(
    "Armar tus propias preguntas: elegís una provincia y ves su clima, sus emisiones y su economía, "
    "y la comparás con el país."
)

provincial = cargar_dataset_provincial()
nacional = cargar_dataset_nacional()

provincia = st.selectbox("Elegí una provincia", sorted(provincial["jurisdiccion"].unique()), index=0,
                         help="Al elegirla se actualizan todos los gráficos de la ficha.")
datos_prov = provincial[provincial["jurisdiccion"] == provincia]

st.subheader(f"Ficha de {provincia}")

if True:
    temp_media = datos_prov["anomalia_temperatura"].mean()
    precip_media = datos_prov["precipitaciones_mm"].mean()
    pbg_reciente = datos_prov.dropna(subset=["pbg"]).sort_values("año")["pbg"].iloc[-1] if datos_prov["pbg"].notna().any() else None
    pass

tarjetas([
    dict(etiqueta="Anomalía media de temperatura", valor=f"{num(temp_media, 2)}", u="°C", unidad="Respecto de la base 1991-2020", ayuda=ayuda("anomalia")),
    dict(etiqueta="Precipitación media", valor=f"{num(precip_media, 0)}" if precip_media == precip_media else "sin datos", u="mm por año", unidad="Promedio anual de la provincia", ayuda=ayuda("v_precipitaciones_mm")),
    dict(etiqueta="PBG más reciente", valor=f"{pbg_reciente:,.0f}".replace(",", ".") if pbg_reciente else "sin datos", u="millones de $", unidad="A precios de 2004", ayuda=ayuda("pbg")),
])

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown(f"**Temperatura ({termino('anomalía', 'anomalia')})**", unsafe_allow_html=True)
        fig = px.line(datos_prov.dropna(subset=["anomalia_temperatura"]), x="año", y="anomalia_temperatura", markers=True,
                      labels={"anomalia_temperatura": "Anomalía de temperatura (°C)", "año": "Año"})
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig, width="stretch")
    with st.container(border=True):
        st.markdown(f"**Emisiones de {termino('GEI', 'gei')}**", unsafe_allow_html=True)
        d = datos_prov.dropna(subset=["emisiones_gei_co2eq"])
        if not d.empty:
            fig = px.bar(d, x="año", y="emisiones_gei_co2eq",
                         labels={"emisiones_gei_co2eq": ETIQUETAS_VARIABLES["emisiones_gei_co2eq"], "año": "Año"})
            st.plotly_chart(fig, width="stretch")
        else:
            st.caption("Sin datos para esta jurisdicción.")

with col2:
    with st.container(border=True):
        st.markdown("**Precipitación**")
        d = datos_prov.dropna(subset=["precipitaciones_mm"])
        fig = px.bar(d, x="año", y="precipitaciones_mm",
                     labels={"precipitaciones_mm": "Precipitación (mm)", "año": "Año"})
        st.plotly_chart(fig, width="stretch")
    with st.container(border=True):
        st.markdown(f"**{termino('PBG', 'pbg')}**", unsafe_allow_html=True)
        d = datos_prov.dropna(subset=["pbg"])
        if not d.empty:
            fig = px.line(d, x="año", y="pbg", markers=True, color="pbg_preliminar",
                          labels={"pbg": "PBG (millones de $ de 2004)", "año": "Año", "pbg_preliminar": "¿Dato preliminar?"})
            st.plotly_chart(fig, width="stretch")
        else:
            st.caption("Sin datos para esta jurisdicción.")

explicacion(
    "Línea para temperatura y PBG (lo que importa es ver si suben o "
    "bajan con el tiempo), barras para precipitación y emisiones (lo que "
    "importa es el valor de cada año puntual, no tanto la curva)."
)

st.space("large")
st.subheader("Comparar contra el agregado nacional")
para_que("Ver si la provincia elegida se calienta al mismo ritmo que el país en su conjunto.")
variable_comp = st.selectbox("Variable climática", ["anomalia_temperatura"], key="comp_var",
                             format_func=lambda v: ETIQUETAS_VARIABLES.get(v, v),
                             help="Anomalía de temperatura: cuántos °C más cálido que lo normal (promedio 1991-2020).")
df_prov_norm = datos_prov[["año", variable_comp]].rename(columns={variable_comp: provincia})
df_nac_norm = nacional[["año", variable_comp]].rename(columns={variable_comp: "Argentina (nacional)"})
combinado = df_prov_norm.merge(df_nac_norm, on="año", how="outer").melt(id_vars="año", var_name="serie", value_name="valor")
fig = px.line(combinado.dropna(), x="año", y="valor", color="serie", markers=True,
              labels={"valor": "Anomalía de temperatura (°C)"})
st.plotly_chart(fig, width="stretch")
explicacion(
    "Dos líneas en el mismo gráfico, misma variable y misma unidad: es la "
    "forma directa de comparar una provincia contra el país. Nota "
    "metodológica: la serie nacional viene del SMN (estaciones en tierra); "
    "la provincial viene de NASA POWER (" + termino("reanálisis satelital", "reanalisis") + "). Métodos "
    "distintos, no estrictamente comparables número a número — solo para "
    "ver la forma de la tendencia."
)

st.space("large")
st.subheader("Ranking interactivo — ordená como quieras")
para_que("Ver qué provincias cambiaron más su temperatura entre el primer y el último año con datos.")
tendencias = provincial.groupby("jurisdiccion").apply(
    lambda g: g["anomalia_temperatura"].iloc[-1] - g["anomalia_temperatura"].iloc[0]
    if g["anomalia_temperatura"].notna().sum() > 1 else None,
    include_groups=False,
).reset_index(name="cambio_total_periodo")
orden = st.radio("Ordenar por", ["cambio_total_periodo"], horizontal=True, label_visibility="collapsed",
                 format_func=lambda v: "Ordenar por: cambio total en el período (°C)",
                 help="Cambio total: diferencia entre el último y el primer valor de anomalía de temperatura de cada provincia.")
fig = px.bar(tendencias.sort_values(orden), x=orden, y="jurisdiccion", orientation="h",
             labels={"cambio_total_periodo": "Cambio total en el período (°C)", "jurisdiccion": ""})
fig.update_layout(height=700)
st.plotly_chart(fig, width="stretch")
explicacion(
    "Barras horizontales ordenadas, para las 24 provincias a la vez: el "
    "mismo criterio que en la página Análisis provincial. Cambio entre el "
    "primer y el último valor disponible de anomalía de temperatura por provincia."
)
