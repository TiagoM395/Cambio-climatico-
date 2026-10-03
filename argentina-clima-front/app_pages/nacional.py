"""Etapa 5: análisis exploratorio nacional. Gráficos originales + nuevos interactivos."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.datos import cargar_dataset_nacional, cargar_tabla, ruta_figura
from utils.ui import (
    ETIQUETAS_VARIABLES, acordeon_pagina, ayuda, config_columnas, explicacion,
    para_que, tabla_legible, tarjetas, termino,
)

st.header(":material/public: Análisis nacional")
acordeon_pagina("nacional")

nacional = cargar_dataset_nacional()
tendencias = cargar_tabla("tendencias_nacional.csv")
estadistica = cargar_tabla("estadistica_descriptiva_nacional.csv")

st.subheader("Las 4 variables del análisis")
para_que(
    "Antes de mirar gráficos, saber qué mide cada cosa. Pasá el mouse por el "
    "signo de pregunta de cada tarjeta para ver qué significa, con un ejemplo."
)
items_n = []
_meta = {
    "anomalia_temperatura": ("°C", "Anomalía de temperatura respecto de 1991-2020"),
    "anomalia_precipitacion_pct": ("%", "Anomalía de lluvia respecto del promedio"),
    "emisiones_gei_co2eq": ("MtCO₂eq", "Gases de efecto invernadero (GEI)"),
    "pbi_crecimiento_pct": ("%", "Crecimiento anual del PBI (Producto Bruto Interno)"),
}
for var, clave in [
    ("anomalia_temperatura", "v_anomalia_temperatura"),
    ("anomalia_precipitacion_pct", "v_anomalia_precipitacion_pct"),
    ("emisiones_gei_co2eq", "v_emisiones_gei_co2eq"),
    ("pbi_crecimiento_pct", "v_pbi_crecimiento_pct"),
]:
    serie = nacional[["año", var]].dropna()
    dato = serie.iloc[-1]
    items_n.append(dict(
        etiqueta=ETIQUETAS_VARIABLES[var], valor=f"{dato[var]:.2f}".replace(".", ","), u=_meta[var][0], unidad=_meta[var][1],
        desc=f"Último dato ({int(dato['año'])}). La serie tiene {len(serie)} años con dato, de {int(serie['año'].min())} a {int(serie['año'].max())}.",
        ayuda=ayuda(clave),
    ))
tarjetas(items_n)

st.space("medium")
st.markdown(f"### {termino('Estadística descriptiva y tendencias', 'estadistica_descriptiva')}", unsafe_allow_html=True)
para_que(
    "Resume cada variable en pocos números: su promedio, cuánto varía, sus "
    "valores mínimo y máximo, y hacia dónde va con los años. Es el primer "
    "chequeo para conocer los datos antes de compararlos entre sí."
)
tabla_resumen = tendencias.merge(estadistica, on="variable")[
    ["variable", "media", "desvio_estandar", "minimo", "maximo", "pendiente", "p_valor"]
]
st.dataframe(
    tabla_legible(tabla_resumen), hide_index=True,
    column_config={
        **config_columnas(tabla_resumen),
        "pendiente": st.column_config.NumberColumn("Tendencia por año", format="%.4f", help=ayuda("tendencia_decada")),
        "p_valor": st.column_config.NumberColumn("p-valor", format="%.4f", help=ayuda("p_valor")),
    },
)
explicacion(
    "Cómo leerla: 'Tendencia por año' dice cuánto sube (+) o baja (-) la "
    "variable en promedio cada año. El 'p-valor' dice si esa tendencia es "
    "confiable: menor a 0,05 significa que es muy poco probable que sea "
    "casualidad. Una tabla y no un gráfico acá porque son 4 variables con "
    f"unidades distintas (°C, %, {termino('MtCO₂eq', 'mtco2eq')}, %) — "
    "mezclarlas en un solo gráfico requeriría normalizarlas, lo que ya se "
    "hace más abajo, en el gráfico de todas las variables normalizadas. La "
    "pendiente describe una tendencia estadística, no implica "
    f"{termino('causalidad', 'causalidad')}."
)

st.space("medium")
st.subheader("Gráficos originales del proyecto")
para_que("Ver, variable por variable, cómo cambió Argentina a lo largo de los años: si sube, baja o se mantiene.")
def _serie(var):
    d = nacional[["año", var]].dropna()
    return f"{len(d)} años con dato, de {int(d['año'].min())} a {int(d['año'].max())}"


figuras = [
    ("temperatura_argentina.png", "Anomalía de temperatura", "anomalia_temperatura",
     "Muestra cuánto más cálido o más frío fue cada año respecto de la temperatura de referencia (promedio 1991-2020), en grados centígrados. "
     "Un valor sobre cero es un año más cálido que lo normal. Fuente: CIAM / SMN."),
    ("precipitaciones_argentina.png", "Anomalía de precipitación", "anomalia_precipitacion_pct",
     "Muestra cuánto más o menos llovió cada año respecto del promedio de referencia, en porcentaje. Un valor sobre cero es un año más "
     "lluvioso que lo normal. Fuente: CIAM / SMN."),
    ("co2_argentina.png", f"Emisiones de gases de efecto invernadero ({termino('GEI', 'gei')})", "emisiones_gei_co2eq",
     f"Muestra cuánto emitió el país cada año de {termino('GEI', 'gei')} (gases como el dióxido de carbono y el metano, que atrapan calor en la atmósfera), "
     f"sumados en {termino('MtCO₂eq', 'mtco2eq')} (millones de toneladas de CO₂ equivalente). Fuente: Inventario Nacional de GEI, Secretaría de Ambiente."),
    ("pbi_argentina.png", f"Crecimiento del {termino('PBI', 'pbi')}", "pbi_crecimiento_pct",
     "Muestra cuánto creció o cayó la producción total del país (Producto Bruto Interno) respecto del año anterior, en porcentaje, a precios constantes. "
     "Sobre cero la economía creció; bajo cero se contrajo. Fuente: Banco Mundial."),
]
cols = st.columns(2)
for i, (archivo, titulo, var, texto) in enumerate(figuras):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"**{titulo}**", unsafe_allow_html=True)
            st.image(str(ruta_figura(archivo)), width="stretch")
            explicacion(f"{texto} <strong>{_serie(var)}.</strong>")

explicacion(
    "Son cuatro gráficos separados, uno por variable, porque cada una tiene su propia unidad y escala: juntarlas en un solo eje sería engañoso. "
    "Pasando el mouse por una sigla (GEI, MtCO₂eq, PBI) se ve su significado."
)

with st.container(border=True):
    st.markdown(f"**Comparación de tendencias normalizadas** ({termino('qué es', 'z_score')})", unsafe_allow_html=True)
    st.image(str(ruta_figura("correlaciones_argentina.png")), width="stretch")
explicacion(
    f"Acá sí van las 4 juntas en el mismo gráfico, a diferencia de los de "
    f"arriba: se puede, porque antes se convierte cada variable a "
    f"{termino('z-score', 'z_score')} — mismo tratamiento, sin unidades — "
    f"lo que permite compararlas en un solo eje sin engañar."
)

st.space("large")
st.subheader(":material/add_chart: Gráficos adicionales interactivos")
para_que("Elegir una variable y ver su evolución y su variabilidad por década, con el valor exacto al pasar el mouse.")

variable_sel = st.selectbox(
    "Variable a explorar",
    help="Elegí qué medida querés mirar; cada opción indica su unidad entre paréntesis.",
    options=["anomalia_temperatura", "anomalia_precipitacion_pct", "emisiones_gei_co2eq",
     "emisiones_co2_fosil", "pbi_crecimiento_pct", "pib_per_capita_crecimiento_pct"],
    format_func=lambda v: {
        "anomalia_temperatura": "Anomalía de temperatura (°C)",
        "anomalia_precipitacion_pct": "Anomalía de precipitación (%)",
        "emisiones_gei_co2eq": "Emisiones de gases de efecto invernadero (MtCO₂eq)",
        "emisiones_co2_fosil": "Emisiones de CO2 fósil, OWID (Mt)",
        "pbi_crecimiento_pct": "Crecimiento del PBI (%)",
        "pib_per_capita_crecimiento_pct": "Crecimiento del PBI per cápita (%) — nuevo",
    }[v],
)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(f"**{termino('Serie temporal', 'serie_temporal')} con {termino('media móvil', 'media_movil')} (5 años)**", unsafe_allow_html=True)
        df_var = nacional[["año", variable_sel]].dropna().sort_values("año")
        df_var["media_movil_5"] = df_var[variable_sel].rolling(5, min_periods=1).mean()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_var["año"], y=df_var[variable_sel], name="Valor anual", opacity=0.4))
        fig.add_trace(go.Scatter(x=df_var["año"], y=df_var["media_movil_5"], name="Media móvil 5 años",
                                  line=dict(width=3)))
        fig.update_layout(xaxis_title="Año", yaxis_title=ETIQUETAS_VARIABLES.get(variable_sel, variable_sel), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, width="stretch")
    explicacion(
        "Barras (el dato de cada año, que salta mucho) más una línea de "
        "media móvil (que lo suaviza): así se ve el ruido año a año y la "
        "tendencia de fondo en el mismo gráfico, sin perder ninguna de las dos."
    )

with col2:
    with st.container(border=True):
        st.markdown(f"**Distribución por década** ({termino('boxplot', 'boxplot')})", unsafe_allow_html=True)
        df_var2 = nacional[["año", variable_sel]].dropna().copy()
        df_var2["decada"] = (df_var2["año"] // 10 * 10).astype(str) + "s"
        fig2 = px.box(df_var2, x="decada", y=variable_sel, points="all",
                       labels={"decada": "Década", variable_sel: ETIQUETAS_VARIABLES.get(variable_sel, variable_sel)})
        st.plotly_chart(fig2, width="stretch")
    explicacion(
        "Boxplot (caja y bigotes) y no un promedio simple por década porque "
        "muestra además cuánto varió el valor dentro de cada década (la caja) y si hubo "
        "años atípicos (los puntos sueltos) — un promedio solo escondería esa dispersión."
    )

with st.container(border=True):
    st.markdown(f"**Todas las variables normalizadas ({termino('z-score', 'z_score')}), interactivo**", unsafe_allow_html=True)
    variables_norm = ["anomalia_temperatura", "anomalia_precipitacion_pct",
                       "emisiones_gei_co2eq", "pbi_crecimiento_pct"]
    df_norm = nacional[["año"] + variables_norm].copy()
    for v in variables_norm:
        df_norm[v] = (df_norm[v] - df_norm[v].mean()) / df_norm[v].std()
    df_largo = df_norm.melt(id_vars="año", value_vars=variables_norm, var_name="variable", value_name="z_score")
    df_largo["variable"] = df_largo["variable"].map(ETIQUETAS_VARIABLES)
    fig3 = px.line(df_largo.dropna(), x="año", y="z_score", color="variable", markers=True,
                    labels={"z_score": "Valor normalizado (z-score)", "año": "Año"})
    st.plotly_chart(fig3, width="stretch")
explicacion(
    "La versión interactiva del mismo gráfico de arriba ('Comparación de "
    "tendencias normalizadas'): mismo criterio de z-score, pero acá podés "
    "pasar el mouse para ver el valor exacto de cada año y cada variable."
)

st.caption(
    "Fuente: CIAM/SMN (temperatura, precipitación), Inventario Nacional de GEI, "
    "Global Carbon Project/OWID (CO2 fósil), Banco Mundial (PBI)."
)
