"""Etapa 8: modelos predictivos. Variable elegida: crecimiento económico (PBI/PBG),
explicado a partir del clima — no al revés."""

import plotly.express as px
import streamlit as st

from utils.datos import ruta_figura, cargar_tabla
from utils.ui import (
    acordeon_pagina, ayuda, config_columnas, explicacion, etiqueta_variable,
    para_que, tabla_legible, tarjetas, termino,
)

st.header(":material/model_training: Modelos predictivos")
acordeon_pagina("modelos")
para_que(
    "Comprobar si, conociendo el clima de un año, se puede adivinar cómo le va a la economía ese año. "
    "Si el modelo acierta, el clima aporta información útil; si no, la relación es débil."
)
explicacion(
    "En cada modelo se elige <strong>una sola variable a predecir</strong> "
    "— nunca varias a la vez. Acá, el crecimiento económico (PBI a nivel "
    "país, PBG a nivel provincia). Las demás — año, precipitación, "
    "temperatura, emisiones — no se predicen: son las pistas (predictoras) "
    "que el modelo usa para intentar adivinar esa única variable. Se "
    "eligió el crecimiento económico y no la temperatura porque la "
    "pregunta del proyecto es si el clima explica cómo le va a la economía."
)

st.subheader("Modelo nacional: crecimiento del PBI a partir del clima")
para_que("Probar si el clima del país (lluvia, temperatura, emisiones) sirve para predecir cuánto crece el PBI de un año.")
st.caption(
    "Variable que se predice (1 sola): crecimiento del PBI. Predictoras "
    "(las pistas, no lo que se predice): año, anomalía de precipitación, "
    "anomalía de temperatura, CO2 (serie OWID, no la oficial de GEI — esa "
    "solo tiene 13 años, insuficiente para dividir train/test)."
)

metricas_nac = cargar_tabla("modelo_nacional_comparacion_metricas.csv").rename(columns={"Unnamed: 0": "Modelo"})
r2_lineal = metricas_nac.loc[metricas_nac["Modelo"] == "Regresión lineal", "R2"].iloc[0]
r2_rf = metricas_nac.loc[metricas_nac["Modelo"] == "Random Forest", "R2"].iloc[0]

if r2_lineal > 0:
    explicacion(
        f"La <strong>regresión lineal</strong> predice el crecimiento del "
        f"PBI mejor que el promedio histórico ({termino('R²', 'r2')} = "
        f"{r2_lineal:.2f} sobre datos de prueba nunca vistos por el "
        f"modelo) — un resultado modesto pero real, no perfecto. El "
        f"<strong>Random Forest</strong>, en cambio, no logra superar al "
        f"promedio histórico ({termino('R²', 'r2')} = {r2_rf:.2f})."
    )
else:
    explicacion(
        f"Resultado honesto: ningún modelo predice mejor que el promedio "
        f"histórico ({termino('R²', 'r2')} negativo). No es un error de "
        f"ejecución: es un hallazgo real del proyecto, reportado sin maquillar."
    )

fig = px.bar(metricas_nac.melt(id_vars="Modelo", var_name="Métrica", value_name="Valor"),
             x="Métrica", y="Valor", color="Modelo", barmode="group")
fig.add_hline(y=0, line_color="gray")
st.plotly_chart(fig, width="stretch")
explicacion(
    f"Barras y no una tabla acá porque lo que importa es comparar de un "
    f"vistazo los dos modelos en sus tres métricas a la vez "
    f"({termino('MAE', 'mae')}, {termino('RMSE', 'rmse')}, "
    f"{termino('R²', 'r2')}) — la línea gris en cero marca el punto donde "
    f"un modelo deja de ser mejor que adivinar el promedio."
)

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown(f"**{termino('Predicción vs. observado', 'predecir_vs_observado')}**", unsafe_allow_html=True)
        st.image(str(ruta_figura("prediccion_temperatura.png")), width="stretch")
    explicacion(
        "Línea observada contra línea predicha, año por año: sirve para "
        "ver EN QUÉ años se equivoca el modelo, algo que el R² por sí solo no muestra."
    )
with col2:
    with st.container(border=True):
        st.markdown(f"**Diagnóstico de {termino('residuos', 'residuo')} ({termino('Random Forest', 'random_forest')})**", unsafe_allow_html=True)
        st.image(str(ruta_figura("residuos_modelo_rf_nacional.png")), width="stretch")
    explicacion(
        "El residuo es la diferencia entre lo real y lo predicho. Si el "
        "modelo fuera bueno, estos puntos caerían al azar alrededor de "
        "cero — un patrón visible acá es señal de que al modelo se le "
        "escapa algo sistemático."
    )

with st.expander("Coeficientes de la regresión lineal (statsmodels OLS)"):
    para_que("Ver cuánto pesa cada variable en la fórmula del modelo y si ese peso es estadísticamente confiable (p-valor).")
    coef = cargar_tabla("modelo_lineal_nacional_coeficientes.csv").rename(columns={"Unnamed: 0": "variable"})
    st.dataframe(tabla_legible(coef), hide_index=True, column_config={
        **config_columnas(coef),
        "coeficiente": st.column_config.NumberColumn(
            format="%.4f", help="Cuánto cambia el PBI, en puntos porcentuales, por cada unidad que sube esa variable, manteniendo las demás fijas."),
        "p_valor": st.column_config.NumberColumn(format="%.4f", help=ayuda("p_valor")),
    })

with st.expander("¿Qué variable climática pesa más para explicar el crecimiento?"):
    para_que("Ordenar las pistas (variables) según cuánto las usó el modelo para acertar.")
    importancia_nac = cargar_tabla("modelo_rf_nacional_importancia_variables.csv").rename(
        columns={"Unnamed: 0": "variable"}
    )
    importancia_nac["Variable"] = importancia_nac["variable"].apply(etiqueta_variable)
    importancia_nac["Importancia (%)"] = importancia_nac["feature_importance"] * 100
    importancia_nac = importancia_nac.sort_values("Importancia (%)", ascending=True)
    fig_imp = px.bar(
        importancia_nac, x="Importancia (%)", y="Variable", orientation="h",
        text=importancia_nac["Importancia (%)"].map(lambda v: f"{v:.0f}%"),
    )
    fig_imp.update_traces(textposition="outside")
    fig_imp.update_layout(xaxis_ticksuffix="%")
    st.plotly_chart(fig_imp, width="stretch")
    variable_top = importancia_nac.sort_values("Importancia (%)", ascending=False).iloc[0]["Variable"]
    explicacion(
        f"Qué es este número: NO es un porcentaje del PBI explicado ni una "
        f"probabilidad. Random Forest entrena 300 arbolitos de decisión "
        f"por separado y promedia cuánto usó cada variable, en todos "
        f"ellos, para achicar el error — a esa cuenta se la llama "
        f"'importancia'. Entre las 4 variables siempre suman 100%, así que "
        f"se lee como un reparto: \"de las pistas que usó el modelo, "
        f"{variable_top} fue la que más peso tuvo\". Ojo: estas barras "
        f"<strong>no son 4 predicciones</strong> — sigue habiendo una sola "
        f"(el crecimiento del PBI); esto solo ordena qué tanto ayudó cada pista a lograrla."
    )

st.space("large")
st.subheader("Modelo provincial conjunto: crecimiento del PBG a partir del clima")
para_que("Lo mismo que el modelo nacional, pero con las 24 provincias juntas: probar si el clima predice cuánto crece la economía de cada provincia.")
st.caption(
    f"Variable que se predice (1 sola): la variación del PBG de cada "
    f"provincia respecto del año anterior (no el nivel de PBG, que está "
    f"dominado por el tamaño de cada economía y no serviría para comparar "
    f"provincias grandes con chicas). Predictoras: año, precipitación, "
    f"temperatura, emisiones y la provincia (codificada con variables "
    f"dummy, nunca con números arbitrarios) — ninguna de estas se predice, son las pistas."
)

metricas_prov = cargar_tabla("modelo_provincial_metricas.csv")
r2_prov = metricas_prov["R2"][0]
tarjetas([
    dict(etiqueta="MAE", valor=f"{metricas_prov['MAE'][0]:.2f}".replace(".", ","), u="p.p.", unidad="Puntos porcentuales", desc="Error absoluto medio de la predicción.", ayuda=ayuda("mae")),
    dict(etiqueta="RMSE", valor=f"{metricas_prov['RMSE'][0]:.2f}".replace(".", ","), u="p.p.", unidad="Puntos porcentuales", desc="Error cuadrático medio: penaliza más los errores grandes.", ayuda=ayuda("rmse")),
    dict(etiqueta="R²", valor=f"{r2_prov:.3f}".replace(".", ",").replace("-", "\u2212"),
         unidad="sin poder predictivo útil" if r2_prov <= 0 else "predice mejor que el promedio",
         desc="Si es negativo, el modelo predice peor que adivinar siempre el promedio.", ayuda=ayuda("r2")),
])

explicacion(
    f"{termino('R²', 'r2')} negativo: a nivel provincial, el clima solo no "
    f"alcanza para predecir cuánto va a crecer o achicarse la economía de "
    f"una provincia de un año al otro — coherente con lo que muestra la "
    f"página \"Clima y economía\": el vínculo entre lluvia y crecimiento, "
    f"provincia por provincia, es débil."
)

with st.container(border=True):
    st.markdown(f"**{termino('Predicción vs. observado', 'predecir_vs_observado')}, por provincia**", unsafe_allow_html=True)
    st.image(str(ruta_figura("prediccion_pbg_provincial.png")), width="stretch")
explicacion(
    "Dispersión (cada punto, una provincia-año) contra la diagonal de "
    "predicción perfecta: mientras más lejos de esa línea caen los "
    "puntos, peor predice el modelo — acá se ve disperso, no pegado a la diagonal."
)

with st.expander("¿Qué variable pesa más en el modelo provincial?"):
    para_que("Ver cuáles de las variables (clima, año, provincia) usó más el modelo provincial para intentar acertar.")
    importancia_prov = cargar_tabla("modelo_rf_provincial_importancia_variables.csv").rename(
        columns={"Unnamed: 0": "variable", "0": "importancia"}
    )
    importancia_prov["Variable"] = importancia_prov["variable"].apply(etiqueta_variable)
    importancia_prov["Importancia (%)"] = importancia_prov["importancia"] * 100
    top10 = importancia_prov.sort_values("Importancia (%)", ascending=False).head(10)
    top10 = top10.sort_values("Importancia (%)", ascending=True)
    fig_imp_prov = px.bar(
        top10, x="Importancia (%)", y="Variable", orientation="h",
        text=top10["Importancia (%)"].map(lambda v: f"{v:.1f}%"),
    )
    fig_imp_prov.update_traces(textposition="outside")
    fig_imp_prov.update_layout(xaxis_ticksuffix="%")
    st.plotly_chart(fig_imp_prov, width="stretch")
    explicacion(
        "Mismo tipo de número que en el modelo nacional (arriba): no es "
        "un porcentaje del PBG explicado, es cuánto usó el modelo cada "
        "variable, en promedio, a lo largo de sus 300 arbolitos de "
        "decisión — de ahí sale el 'reparto' en % que ves acá. Hay ~28 "
        "variables en total (4 climáticas + 24 provincias, una dummy por "
        "cada una) y se muestran solo las 10 con más peso. Estas barras "
        "tampoco son varias predicciones — sigue habiendo una sola (la "
        "variación del PBG). 'año' domina — probablemente refleja un "
        "shock general a todas las provincias en el mismo año (por "
        "ejemplo 2020, pandemia), más que una relación con el clima."
    )

st.caption(
    "No se construyeron modelos individuales por provincia: máximo 13 años de "
    "datos con las 4 predictoras completas simultáneamente por jurisdicción."
)
