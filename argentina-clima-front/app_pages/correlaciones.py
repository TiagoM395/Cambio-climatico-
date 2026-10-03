"""Etapa 7: relación clima-economía. Nacional y provincial, nunca mezclados."""

import plotly.express as px
import streamlit as st

from utils.datos import ruta_figura, cargar_tabla
from utils.ui import acordeon_pagina, ayuda, explicacion, num, para_que, tarjetas, termino

st.header(":material/insights: Clima y economía")
acordeon_pagina("correlaciones")
st.caption(
    "Todo lo que sigue describe **asociación estadística**, nunca causalidad "
    "(proyecto.txt, sección 21): que dos cosas se muevan juntas no prueba que "
    "una cause la otra."
)
para_que(
    "Evitar conclusiones equivocadas: ver que dos cosas cambian a la vez "
    "no demuestra que una provoque la otra."
)

st.subheader("¿A qué provincia le llueve cada vez menos, y cómo le fue su economía?")
para_que(
    "Comprobar si las provincias donde la lluvia viene bajando son también las que crecieron menos económicamente. "
    "Es la pregunta central del proyecto, mirada provincia por provincia."
)

ranking = cargar_tabla("ranking_precipitacion_crecimiento_pbg_provincial.csv")
cruce = cargar_tabla("correlacion_precipitacion_crecimiento_pbg_provincial.csv").iloc[0]

fig = px.bar(
    ranking.sort_values("tendencia_precipitacion_por_decada"),
    x="tendencia_precipitacion_por_decada", y="jurisdiccion", orientation="h",
    color="pbg_crecimiento_anual_pct", color_continuous_scale="PuOr",
    color_continuous_midpoint=ranking["pbg_crecimiento_anual_pct"].mean(),
    labels={
        "tendencia_precipitacion_por_decada": "Tendencia de precipitación (mm por década)",
        "jurisdiccion": "",
        "pbg_crecimiento_anual_pct": "Crecimiento anual del PBG (%)",
    },
    hover_data={"pbg_crecimiento_anual_pct": ":.2f", "tendencia_precipitacion_por_decada": ":.2f"},
)
fig.add_vline(x=0, line_dash="dash", line_color="gray")
fig.update_layout(height=700)
st.plotly_chart(fig, width="stretch")
explicacion(
    "Se eligió una barra horizontal con color en vez de dos gráficos "
    "separados porque hay que leer dos cosas de la misma provincia a la "
    "vez. Cada barra es una provincia. La <strong>posición</strong> "
    "muestra si la lluvia viene subiendo o bajando por década (barras a "
    "la izquierda = cada vez llueve menos ahí). El <strong>color</strong> "
    f"muestra cómo creció el {termino('PBG', 'pbg')} de esa provincia "
    "entre 2004 y 2024 (violeta = creció poco o se achicó, naranja = creció mucho)."
)

mas_seca = ranking.sort_values("tendencia_precipitacion_por_decada").iloc[0]
peor_crecimiento = ranking.sort_values("pbg_crecimiento_anual_pct").iloc[0]
promedio_crecimiento = ranking["pbg_crecimiento_anual_pct"].mean()
diferencia = mas_seca["pbg_crecimiento_anual_pct"] - promedio_crecimiento
tarjetas([
    dict(etiqueta="Donde más baja la lluvia", valor=mas_seca["jurisdiccion"], unidad=f"{num(mas_seca['tendencia_precipitacion_por_decada'], 2)} mm por década",
         desc=(f"Su PBG creció {num(mas_seca['pbg_crecimiento_anual_pct'], 2)} % anual entre {int(mas_seca['pbg_año_inicio'])} y {int(mas_seca['pbg_año_fin'])}: "
               f"{'por debajo' if diferencia < 0 else 'por encima'} del promedio de las 24 provincias ({num(promedio_crecimiento, 2)} %)."),
         ayuda=ayuda("tendencia_decada")),
    dict(etiqueta="Peor desempeño económico", valor=peor_crecimiento["jurisdiccion"], unidad=f"{num(peor_crecimiento['pbg_crecimiento_anual_pct'], 2)} % de crecimiento anual del PBG",
         desc=(f"Ahí la lluvia por década vino {'bajando' if peor_crecimiento['tendencia_precipitacion_por_decada'] < 0 else 'subiendo'} "
               f"({num(peor_crecimiento['tendencia_precipitacion_por_decada'], 2)} mm): "
               f"{'sí' if peor_crecimiento['tendencia_precipitacion_por_decada'] < -0.1 else 'no'} es de las provincias más secas del país."),
         ayuda=ayuda("cagr")),
], minimo=320)

explicacion(
    f"Con los datos disponibles (24 provincias, 2004-2024), la relación "
    f"entre perder lluvia y crecer menos es débil y no se puede afirmar "
    f"con confianza: {termino('correlación', 'pearson')} de "
    f"{cruce['pearson_r']:.2f} ({termino('p', 'p_valor')}={cruce['pearson_p']:.2f}, "
    f"con p&lt;0.05 se consideraría significativa). Las tres provincias "
    f"donde más bajó la lluvia (Misiones, Chaco, Corrientes) tuvieron un "
    f"crecimiento del PBG cercano o por encima del promedio nacional — no "
    f"son las que peor le fue. Las de peor desempeño económico (Catamarca, "
    f"Santa Cruz) no son las más secas: en Catamarca la lluvia incluso "
    f"viene en aumento. Esto sugiere que, en el período analizado, la "
    f"economía de cada provincia depende más de otros factores (qué "
    f"sectores produce, precios internacionales, ciclos nacionales) que "
    f"de cuánto llueve."
)

with st.container(border=True):
    st.markdown("**Provincia por provincia: tendencia de lluvia vs. crecimiento del PBG**")
    st.image(str(ruta_figura("precipitacion_vs_crecimiento_pbg_provincial.png")), width="stretch")
explicacion(
    termino("Dispersión (scatter)", "dispersion") + " además de la barra de arriba, y no un segundo "
    "gráfico de barras, porque acá el objetivo es distinto: ver de un "
    "vistazo si TODOS los puntos siguen un patrón (una diagonal) o no. "
    "Cada punto es una provincia. Si la lluvia explicara el crecimiento, "
    "los puntos formarían una diagonal clara — acá aparecen dispersos, lo "
    "que respalda que la relación es débil."
)

st.dataframe(
    ranking, hide_index=True, height="content",
    column_config={
        "jurisdiccion": "Provincia",
        "tendencia_precipitacion_por_decada": st.column_config.NumberColumn(
            "Tendencia de lluvia (mm/década)", format="%.2f", help=ayuda("tendencia_decada")),
        "precipitacion_p_valor": st.column_config.NumberColumn("p-valor tendencia", format="%.3f", help=ayuda("p_valor")),
        "pbg_crecimiento_anual_pct": st.column_config.NumberColumn(
            "Crecimiento anual del PBG (%)", format="%.2f", help=ayuda("cagr")),
        "pbg_año_inicio": "Desde", "pbg_año_fin": "Hasta", "pbg_n_años": "Años con dato",
    },
)

st.space("large")
st.subheader("¿En los años de sequía, la economía creció menos?")
para_que("Comparar directamente cómo creció la economía en los años secos contra los años normales.")
explicacion(
    f"Hasta acá, la lluvia se miró como un número (mm, tendencia). Acá se "
    f"hace la pregunta directamente: se define {termino('año seco', 'año_seco')} "
    f"y se compara el crecimiento económico de esos años contra el resto, "
    f"con una {termino('prueba t', 'prueba_t')} — la forma más simple y "
    f"directa de comparar dos grupos, más fácil de leer que un coeficiente "
    f"de correlación."
)

seq_nac = cargar_tabla("sequia_vs_crecimiento_nacional.csv").rename(columns={"Unnamed: 0": "variable"})
seq_prov = cargar_tabla("sequia_vs_crecimiento_provincial.csv").iloc[0]
fila_pbi = seq_nac[seq_nac["variable"] == "pbi_crecimiento_pct"].iloc[0]
fila_percapita = seq_nac[seq_nac["variable"] == "pib_per_capita_crecimiento_pct"].iloc[0]

col_nac, col_prov = st.columns(2)
with col_nac:
    with st.container(border=True):
        st.markdown("**País: años secos vs. normales**")
        st.image(str(ruta_figura("sequia_vs_crecimiento_nacional.png")), width="stretch")
        st.caption(
            f"PBI: {fila_pbi['media_crecimiento_secos']:.2f}% en años secos contra {fila_pbi['media_crecimiento_normales']:.2f}% en normales "
            f"(p = {fila_pbi['p_valor']:.2f}). PBI per cápita: {fila_percapita['media_crecimiento_secos']:.2f}% contra "
            f"{fila_percapita['media_crecimiento_normales']:.2f}% (p = {fila_percapita['p_valor']:.2f}). "
            f"{int(fila_pbi['n_años_secos'])} años secos, {int(fila_pbi['n_años_normales'])} normales."
        )
with col_prov:
    with st.container(border=True):
        st.markdown(f"**{int(seq_prov['n_provincias'])} provincias, cada una contra su propio promedio**")
        st.image(str(ruta_figura("sequia_vs_crecimiento_provincial.png")), width="stretch")
        st.caption(
            f"PBG en años secos: {seq_prov['media_relativa_secos']:.2f} puntos respecto de lo normal de esa provincia; "
            f"en años no secos: {seq_prov['media_relativa_normales']:.2f}. Diferencia de {seq_prov['diferencia']:.2f} puntos "
            f"(p = {seq_prov['p_valor']:.2f})."
        )

explicacion(
    "<strong>Conclusión:</strong> ni a nivel país ni comparando las provincias contra sí mismas el crecimiento de los años secos "
    "se distingue del de los años normales (p mayor a 0,05: más de 5 chances en 100 de que la diferencia sea casualidad). "
    "No haber encontrado diferencia también responde la pregunta."
)

st.space("large")
with st.expander(":material/table_chart: Detalle estadístico — 96 + 4 pruebas de correlación técnicas"):
    para_que(
        "Revisar, provincia por provincia, si hay relación entre las variables. "
        "Es un detalle técnico: la conclusión general ya está más arriba."
    )
    explicacion(
        "Estas son las pruebas de correlación <strong>dentro de cada "
        "provincia</strong> (entre sus propios años), no el cruce entre "
        "provincias de arriba. Con apenas 13 a 15 años de datos por "
        "provincia tienen muy poco poder estadístico — por eso casi "
        "ninguna da significativa. Se muestran igual, sin maquillar el resultado."
    )
    corr_nac = cargar_tabla("correlaciones_nacional.csv")
    corr_prov = cargar_tabla("correlaciones_provincial.csv")

    st.markdown("**Nacional**")
    st.dataframe(
        corr_nac, hide_index=True,
        column_config={
            "metodo": st.column_config.TextColumn("Método", help=ayuda("metodo")),
            "coeficiente": st.column_config.NumberColumn(format="%.3f", help=ayuda("pearson")),
            "p_valor": st.column_config.NumberColumn(format="%.4f", help=ayuda("p_valor")),
        },
    )
    st.caption("Ninguna asociación nacional resultó estadísticamente significativa (todos los p-valores > 0.05).")

    st.markdown("**Provincial — 96 pruebas, nunca mezcladas entre provincias**")
    sig = corr_prov[(corr_prov["p_valor"].notna()) & (corr_prov["p_valor"] < 0.05)]
    tarjetas([dict(etiqueta="Pruebas con p < 0,05", valor=f"{len(sig)} de {corr_prov['p_valor'].notna().sum()}", unidad="menos de lo esperable por azar (unas 5 de 96)", ayuda=ayuda("p_valor"))], minimo=320)
    st.dataframe(
        corr_prov, hide_index=True,
        column_config={
            "metodo": st.column_config.TextColumn("Método", help=ayuda("metodo")),
            "coeficiente": st.column_config.NumberColumn(format="%.3f", help=ayuda("pearson")),
            "p_valor": st.column_config.NumberColumn(format="%.4f", help=ayuda("p_valor")),
        },
    )
