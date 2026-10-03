"""Etapa 6: análisis provincial. Gráficos originales + nuevos (heatmap, boxplot, comparador)."""

import plotly.express as px
import streamlit as st

from utils.datos import cargar_dataset_provincial, cargar_tabla, ruta_figura, PROVINCIAS_ORDEN
from utils.ui import (
    ETIQUETAS_VARIABLES, acordeon_pagina, ayuda, config_columnas, explicacion,
    para_que, termino,
)

st.header(":material/map: Análisis provincial")
acordeon_pagina("provincial")
st.caption(
    "Los rankings y comparaciones de esta página son descriptivos: no implican "
    "juicio de valor sobre ninguna provincia (proyecto.txt, secciones 16 y 29)."
)
para_que(
    "Comprobar si el calentamiento y la lluvia cambian igual en todo el país "
    "o si hay provincias que se comportan distinto."
)

provincial = cargar_dataset_provincial()
tendencias = cargar_tabla("tendencias_temperatura_provincial.csv")

st.subheader("Gráficos originales del proyecto")
para_que("Ver la evolución de cada provincia en el tiempo y quiénes se destacan.")
with st.container(border=True):
    st.markdown("**Evolución de temperatura por provincia**")
    st.image(str(ruta_figura("temperatura_provincias.png")), width="stretch")
explicacion(
    "Una línea por provincia, superpuestas: con 24 provincias el gráfico "
    "queda cargado, pero alcanza para ver si todas siguen la misma "
    "tendencia o si alguna se despega del resto — a ancho completo, no en "
    "media columna, para que se puedan distinguir las líneas. El detalle "
    "exacto de cada una está en el mapa de calor interactivo, más abajo."
)

with st.container(border=True):
    st.markdown("**Evolución de precipitación por provincia**")
    st.image(str(ruta_figura("precipitaciones_provincias.png")), width="stretch")
explicacion(
    "Mismo criterio que el gráfico de arriba, para precipitación en vez "
    "de temperatura: una línea por provincia, a ancho completo."
)

col_izq, col_centro, col_der = st.columns([1, 3, 1])
with col_centro:
    with st.container(border=True):
        st.markdown("**Ranking descriptivo de tendencia de temperatura**")
        st.image(str(ruta_figura("ranking_tendencia_temperatura_provincias.png")), width="stretch")
explicacion(
    "Barras horizontales y ordenadas, no un mapa acá, porque lo que "
    "importa es comparar el número exacto entre las 24 jurisdicciones — "
    "el mapa con la misma información está más abajo, en la página Mapas, "
    "para ver el patrón geográfico. Achicado a una columna central (la "
    "imagen original es casi cuadrada) para que no ocupe toda la pantalla."
)

st.space("large")
st.subheader(":material/add_chart: Gráficos adicionales interactivos")
para_que("Explorar los datos con más detalle: el valor exacto de cada provincia y año, y armar tus propias comparaciones.")

with st.container(border=True):
    st.markdown(f"**{termino('Mapa de calor', 'mapa_calor')}: {termino('anomalía', 'anomalia')} de temperatura por provincia y año**", unsafe_allow_html=True)
    pivote = provincial.pivot_table(index="jurisdiccion", columns="año", values="anomalia_temperatura")
    pivote = pivote.reindex([p for p in PROVINCIAS_ORDEN if p in pivote.index])
    fig = px.imshow(
        pivote, aspect="auto", color_continuous_scale="RdBu_r", color_continuous_midpoint=0,
        labels=dict(x="Año", y="Provincia", color="Anomalía (°C)"),
    )
    fig.update_layout(height=650)
    st.plotly_chart(fig, width="stretch")
    explicacion(
        "Mapa de calor (provincia × año) y no 24 líneas superpuestas: con "
        "24 provincias, un gráfico de líneas sería ilegible — acá cada "
        "celda de color se lee sola, y el color de la Provincia y el año "
        "que te interesan salta a la vista igual. Fuente: NASA POWER "
        "(" + termino("reanálisis", "reanalisis") + "), 1981-2025. Rojo = más cálido que la base 1991-2020."
    )

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown(f"**Distribución de {termino('anomalía', 'anomalia')} por provincia ({termino('boxplot', 'boxplot')})**", unsafe_allow_html=True)
        fig2 = px.box(provincial, x="jurisdiccion", y="anomalia_temperatura", points=False)
        fig2.update_layout(xaxis_tickangle=-70, height=500, xaxis_title="", yaxis_title="Anomalía (°C)")
        st.plotly_chart(fig2, width="stretch")
    explicacion(
        "Boxplot para ver, de cada provincia, no solo el promedio sino "
        "también cuánto varía año a año (la altura de la caja) — dos "
        "provincias pueden tener el mismo promedio y una ser mucho más "
        "estable que la otra."
    )

with col2:
    with st.container(border=True):
        st.markdown(f"**Precipitación media vs. tendencia de temperatura** ({termino('gráfico de dispersión', 'dispersion')})", unsafe_allow_html=True)
        precip_media = provincial.groupby("jurisdiccion")["precipitaciones_mm"].mean().reset_index()
        combinado = tendencias.merge(precip_media, on="jurisdiccion")
        fig3 = px.scatter(
            combinado, x="precipitaciones_mm", y="pendiente", text="jurisdiccion",
            labels={"precipitaciones_mm": "Precipitación media (mm/año)", "pendiente": "Tendencia de temperatura (°C/año)"},
        )
        fig3.update_traces(textposition="top center", textfont_size=8)
        fig3.update_layout(height=500)
        st.plotly_chart(fig3, width="stretch")
    explicacion(
        "Dispersión (scatter) con una provincia por punto: es el gráfico "
        "correcto para ver si dos variables numéricas distintas — cuánto "
        "llueve y cuánto sube la temperatura — se relacionan entre "
        "provincias. Una línea de tiempo no serviría acá porque no hay un eje de años."
    )

st.space("medium")
with st.container(border=True):
    st.markdown("**Comparador de provincias — elegí y compará**")
    seleccionadas = st.multiselect(
        "Provincias a comparar", sorted(provincial["jurisdiccion"].unique()),
        default=["CABA", "Buenos Aires", "Santa Cruz"],
    )
    variable_cmp = st.segmented_control(
        "Variable", ["anomalia_temperatura", "precipitaciones_mm", "pbg", "emisiones_gei_co2eq"],
        default="anomalia_temperatura",
        format_func=lambda v: ETIQUETAS_VARIABLES.get(v, v),
        help=(
            "Anomalía de temperatura: cuánto más cálido que lo normal (°C). "
            "Precipitación: milímetros de lluvia por año. PBG: producto bruto "
            "geográfico, lo que produce la economía de la provincia. Emisiones: "
            "gases de efecto invernadero en millones de toneladas de CO₂ equivalente."
        ),
    )
    if seleccionadas and variable_cmp:
        datos_cmp = provincial[provincial["jurisdiccion"].isin(seleccionadas)]
        fig4 = px.line(datos_cmp.dropna(subset=[variable_cmp]), x="año", y=variable_cmp,
                        color="jurisdiccion", markers=True,
                        labels={variable_cmp: ETIQUETAS_VARIABLES.get(variable_cmp, variable_cmp),
                                "año": "Año", "jurisdiccion": "Provincia"})
        st.plotly_chart(fig4, width="stretch")
        explicacion(
            "Línea de tiempo, una por provincia elegida: es el gráfico que "
            "permite comparar la evolución año a año de hasta un puñado de "
            "provincias a la vez — con las 24 juntas (como arriba) ya no se distingue nada."
        )
    else:
        st.caption("Elegí al menos una provincia y una variable.")

st.markdown("**Ranking de calentamiento por provincia**")
para_que("Ordenar las provincias de la que más se calienta a la que menos, con qué confianza y con cuántos años de datos.")
_tabla_prov = tendencias[["jurisdiccion", "pendiente", "p_valor", "n_observaciones"]].sort_values("pendiente", ascending=False)
st.dataframe(
    _tabla_prov,
    hide_index=True,
    column_config={
        **config_columnas(_tabla_prov),
        "pendiente": st.column_config.NumberColumn("Tendencia (°C/año)", format="%.4f", help=ayuda("tendencia_decada")),
        "p_valor": st.column_config.NumberColumn("p-valor", format="%.4f", help=ayuda("p_valor")),
    },
)
