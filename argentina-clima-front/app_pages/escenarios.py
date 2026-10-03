"""Etapa 9: escenarios de proyección futura, hasta 2050 (A y C) y fin de siglo (B)."""

import plotly.graph_objects as go
import streamlit as st

from utils.datos import ruta_figura, cargar_tabla, cargar_dataset_nacional
from utils.ui import acordeon_pagina, ayuda, explicacion, num, para_que, tarjetas, termino

st.header(":material/timeline: Escenarios futuros")
acordeon_pagina("escenarios")
para_que(
    "Estimar cuánto podría subir la temperatura de Argentina hacia 2050 "
    "y a fin de siglo, según tres formas distintas de mirar el futuro."
)
explicacion(
    "No se usaron los modelos multivariados de la página anterior (ya "
    "comprobados poco confiables) para proyectar el futuro: se usó "
    + termino("extrapolación", "extrapolacion") + " de tendencia simple, que no requiere inventar valores "
    "futuros de precipitación/CO2/PBI."
)

nacional = cargar_dataset_nacional()
esc_a = cargar_tabla("escenario_a_continuidad_tendencia.csv")
esc_c = cargar_tabla("escenario_c_aceleracion_reciente.csv")
esc_b = cargar_tabla("escenarios_proyeccion_b_ipcc.csv")

with st.container(border=True):
    st.markdown(f"**Gráfico original: observado + {termino('Escenarios A', 'escenario_a')} y {termino('C', 'escenario_c')}**", unsafe_allow_html=True)
    st.image(str(ruta_figura("prediccion_temperatura_escenarios.png")), width="stretch")
explicacion(
    "Serie de tiempo (línea) porque la pregunta es \"¿cómo sigue esto en "
    "el tiempo?\" — el tipo de gráfico hecho justamente para mostrar "
    "evolución, con lo observado y lo proyectado sobre el mismo eje para comparar."
)

st.space("large")
st.subheader(":material/add_chart: Comparación interactiva 2026-2050")

fig = go.Figure()
fig.add_trace(go.Scatter(x=nacional["año"], y=nacional["anomalia_temperatura"], mode="lines+markers",
                          name="Observado (1961-2025)", line=dict(color="black")))
fig.add_trace(go.Scatter(x=esc_a["año"], y=esc_a["anomalia_proyectada"], mode="lines", name="Escenario A",
                          line=dict(color="royalblue", dash="dash")))
fig.add_trace(go.Scatter(x=esc_a["año"], y=esc_a["ic95_superior"], mode="lines", line=dict(width=0),
                          showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=esc_a["año"], y=esc_a["ic95_inferior"], mode="lines", line=dict(width=0),
                          fill="tonexty", fillcolor="rgba(65,105,225,0.15)", showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=esc_c["año"], y=esc_c["anomalia_proyectada"], mode="lines", name="Escenario C",
                          line=dict(color="darkorange", dash="dash")))
fig.add_trace(go.Scatter(x=esc_c["año"], y=esc_c["ic95_superior"], mode="lines", line=dict(width=0),
                          showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=esc_c["año"], y=esc_c["ic95_inferior"], mode="lines", line=dict(width=0),
                          fill="tonexty", fillcolor="rgba(255,140,0,0.15)", showlegend=False, hoverinfo="skip"))
fig.update_layout(xaxis_title="Año", yaxis_title="Anomalía de temperatura (°C, base 1991-2020)",
                   legend=dict(orientation="h", y=-0.2), height=550)
st.plotly_chart(fig, width="stretch")
explicacion(
    f"Línea, con una banda sombreada alrededor de cada proyección: la "
    f"banda es el {termino('intervalo de confianza del 95%', 'ic95')} — "
    f"muestra que cuanto más lejos del último dato real, menos segura es "
    f"la proyección. Un solo número (sin banda) escondería esa incertidumbre creciente."
)

val_a_2050 = esc_a[esc_a["año"] == 2050]["anomalia_proyectada"].values[0]
val_c_2050 = esc_c[esc_c["año"] == 2050]["anomalia_proyectada"].values[0]
tarjetas([
    dict(etiqueta="Escenario A en 2050", valor=f"+{num(val_a_2050, 2)}", u="°C", unidad="Continuidad de la tendencia histórica",
         desc="La tendencia es estadísticamente significativa (p < 0,001).", ayuda=ayuda("escenario_a") + " " + ayuda("p_valor")),
    dict(etiqueta="Escenario C en 2050", valor=f"+{num(val_c_2050, 2)}", u="°C", unidad="Aceleración reciente",
         desc="La pendiente no es significativa (p = 0,11): proyección menos confiable.", ayuda=ayuda("escenario_c") + " " + ayuda("p_valor")),
    dict(etiqueta="Escenario B, fin de siglo", valor="+1,0 a +3,5", u="°C", unidad="Proyección externa del IPCC, fin de siglo",
         desc="Cita externa, con su propio horizonte y metodología: no comparable directamente.", ayuda=ayuda("escenario_b") + " " + ayuda("ipcc")),
])

st.space("medium")
st.markdown(f"### {termino('Escenario B', 'escenario_b')} — proyección científica externa ({termino('IPCC', 'ipcc')} AR5)", unsafe_allow_html=True)
st.caption("No calculado por este proyecto. Barros et al. (2014), vía Tercera Comunicación Nacional de Argentina.")
st.dataframe(
    esc_b[["escenario", "horizonte", "anomalia_proyectada_c_min", "anomalia_proyectada_c_max", "nota_geografica"]],
    hide_index=True, height="content",
    column_config={
        "escenario": st.column_config.Column("Escenario", help="Hipótesis sobre cuántas emisiones habrá en el futuro."),
        "horizonte": st.column_config.Column("Horizonte", help="Años para los que se hace la proyección."),
        "anomalia_proyectada_c_min": st.column_config.Column("Anomalía mínima (°C)", help="Suba de temperatura más baja proyectada, respecto de lo normal."),
        "anomalia_proyectada_c_max": st.column_config.Column("Anomalía máxima (°C)", help="Suba de temperatura más alta proyectada, respecto de lo normal."),
        "nota_geografica": st.column_config.Column("Nota geográfica", help="A qué parte del país corresponde la proyección."),
    },
)

st.caption(
    "'Observado' = dato real medido. 'A/C' = predicción de este proyecto "
    "(extrapolación, incertidumbre creciente cuanto más lejos del último dato). "
    "'B' = cita externa, con su propio horizonte y metodología. No se mezclan."
)
