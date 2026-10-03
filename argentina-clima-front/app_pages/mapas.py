"""Etapa 11: mapas coropléticos. Los 3 mapas originales + un mapa interactivo nuevo."""

import json
import plotly.express as px
import streamlit as st

from utils.datos import cargar_dataset_provincial, cargar_geometria, cargar_tabla, ruta_figura
from utils.ui import acordeon_pagina, explicacion, para_que, termino

st.header(":material/travel_explore: Mapas")
acordeon_pagina("mapas")
st.caption(
    "Geometría oficial del Instituto Geográfico Nacional (IGN). El polígono "
    "de Tierra del Fuego incluye el sector antártico reclamado por "
    "Argentina; en los mapas originales se recortó el encuadre visual "
    "(no el dato) al territorio continental."
)

para_que("Ver dónde está cada dato en el territorio: qué provincias se calientan más, cuáles reciben más lluvia y dónde se produce más.")
st.subheader("Mapas originales del proyecto")
cols = st.columns(3)
mapas_originales = [
    ("mapa_temperatura.png", "Tendencia de temperatura (°C/año)"),
    ("mapa_anomalia_termica.png", "Anomalía media 2016-2025"),
    ("mapa_precipitaciones.png", "Precipitación media anual"),
]
for i, (archivo, titulo) in enumerate(mapas_originales):
    with cols[i]:
        st.markdown(f"**{titulo}**")
        st.image(str(ruta_figura(archivo)), width="stretch")
explicacion(
    f"Se eligió el {termino('mapa coroplético', 'coropletico')} porque acá "
    f"lo que importa es la ubicación geográfica de cada dato — un mapa lo "
    f"muestra de un vistazo, algo que ni una tabla ni un gráfico de barras "
    f"pueden hacer."
)

st.space("large")
st.subheader(":material/add_chart: Mapa interactivo nuevo")


@st.cache_data
def _geojson_y_datos():
    gdf = cargar_geometria()
    gdf = gdf.copy()
    gdf["jurisdiccion"] = gdf["NAM"].replace({"Ciudad Autónoma de Buenos Aires": "CABA"})
    gdf = gdf[["jurisdiccion", "geometry"]]
    geojson = json.loads(gdf.to_json())
    return geojson


geojson = _geojson_y_datos()
provincial = cargar_dataset_provincial()
tendencias = cargar_tabla("tendencias_temperatura_provincial.csv")

variable_mapa = st.radio(
    "Variable a mostrar", ["Tendencia de temperatura (°C/año)", "Precipitación media (mm/año)", "PBG más reciente"],
    horizontal=True,
    help=(
        "Tendencia de temperatura: cuántos °C por año sube la temperatura. "
        "Precipitación media: milímetros de lluvia por año. PBG: producto "
        "bruto geográfico, el valor de lo que produce la economía de cada "
        "provincia (equivalente al PBI, pero provincial)."
    ),
)

if variable_mapa == "Tendencia de temperatura (°C/año)":
    datos_mapa = tendencias[["jurisdiccion", "pendiente"]].rename(columns={"pendiente": "valor"})
    escala = "Reds"
elif variable_mapa == "Precipitación media (mm/año)":
    datos_mapa = provincial.groupby("jurisdiccion")["precipitaciones_mm"].mean().reset_index()
    datos_mapa.columns = ["jurisdiccion", "valor"]
    escala = "Blues"
else:
    ultimo_año_pbg = provincial.dropna(subset=["pbg"])["año"].max()
    datos_mapa = provincial[provincial["año"] == ultimo_año_pbg][["jurisdiccion", "pbg"]].rename(columns={"pbg": "valor"})
    escala = "Greens"

fig = px.choropleth(
    datos_mapa, geojson=geojson, locations="jurisdiccion", featureidkey="properties.jurisdiccion",
    color="valor", color_continuous_scale=escala,
    labels={"valor": variable_mapa, "jurisdiccion": "Provincia"},
)
fig.update_geos(
    fitbounds="locations", visible=False,
    lataxis_range=[-56, -21], lonaxis_range=[-75, -53],
)
fig.update_layout(height=650, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, width="stretch")
explicacion(
    "Versión interactiva del mismo tipo de mapa de arriba, pero con la "
    "variable que elijas — pasá el mouse sobre cada provincia para ver el valor exacto."
)
