"""Respuesta a la pregunta central: ¿el cambio climático afecta a la economía argentina?
Página en pestañas: pregunta, evidencia paso a paso y veredicto. Solo datos reales del proyecto."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.datos import cargar_dataset_nacional, cargar_dataset_provincial, cargar_tabla
from utils.ui import COLOR_ESTADO, acordeon_pagina, ayuda, claves, explicacion, num, paneles, para_que, svg_linea, svg_rango, tabla_html, tarjetas, termino

st.header(":material/question_answer: Respuesta a la pregunta")
acordeon_pagina("respuesta")

# ---------------------------------------------------------------- datos
nacional = cargar_dataset_nacional()
tend_nac = cargar_tabla("tendencias_nacional.csv").set_index("variable")
tend_prov = cargar_tabla("tendencias_temperatura_provincial.csv")
nac_pc = cargar_tabla("impacto_nacional_percapita.csv").set_index("variable")
sequia_nac = cargar_tabla("sequia_vs_crecimiento_nacional.csv").rename(columns={"Unnamed: 0": "variable"}).set_index("variable")
panel = cargar_tabla("impacto_agro_panel.csv")
res = cargar_tabla("impacto_agro_resultados.csv")
por_prov = cargar_tabla("impacto_agro_por_provincia.csv")
rob = cargar_tabla("robustez_resultados.csv")
rend = cargar_tabla("rendimiento_resultados.csv").set_index("cultivo")
rend_prov = cargar_tabla("rendimiento_por_provincia.csv")
rend_nac = cargar_tabla("rendimiento_nacional.csv").set_index("cultivo")
corr_prov = cargar_tabla("correlaciones_provincial.csv")
tend_lluvia = cargar_tabla("ranking_precipitacion_crecimiento_pbg_provincial.csv").set_index("jurisdiccion")
sequia_panel = cargar_tabla("sequia_vs_crecimiento_provincial.csv").iloc[0]
_lluvia = cargar_dataset_provincial()[["año", "precipitaciones_mm"]].dropna()
años_lluvia = f"{int(_lluvia['año'].min())}-{int(_lluvia['año'].max())}"

pend = tend_nac.loc["anomalia_temperatura", "pendiente"]
años_serie = nacional["año"].max() - nacional["año"].min()


def fila(resultado, factor):
    return res[(res["resultado"] == resultado) & (res["factor"] == factor)].iloc[0]


agro_seco = fila("Producción agropecuaria", "Año seco")
agro_temp = fila("Producción agropecuaria", "Temperatura (+1 °C)")
tot_seco = fila("Economía total de la provincia", "Año seco")
tot_temp = fila("Economía total de la provincia", "Temperatura (+1 °C)")
peso_min, peso_max = por_prov["peso_agro_medio_pct"].nlargest(8).iloc[-1], por_prov["peso_agro_medio_pct"].max()


def rb(prueba, detalle=None):
    """Fila de la tabla de robustez: la que empieza con `prueba` y (opcional) contiene `detalle`."""
    d = rob[rob["prueba"].str.startswith(prueba)]
    if detalle:
        d = d[d["detalle"].str.contains(detalle, regex=False)]
    return d.iloc[0]


# (fila, nombre con su significado, qué se hizo, qué se espera si el efecto es real, unidad del efecto)
PRUEBAS = [
    (rb("1. Corrección", "Temperatura (+1 °C) → Producción"), "Corrección de Holm",
     "Endurecer el criterio porque se probaron 6 combinaciones y alguna puede salir bien por pura suerte (como acertar un número tirando muchas veces).",
     "sig", "puntos por °C"),
    (rb("2. Sacar una provincia (peor"), "Sacar una provincia (el peor caso)",
     "Repetir el cálculo 24 veces, sacando de a una provincia, para ver si la señal depende de una sola. Se muestra el caso más desfavorable.",
     "sig", "puntos por °C"),
    (rb("3."), "Sin valores extremos", "Recortar los años de crecimiento agropecuario excepcionalmente altos o bajos (winsorizar al 5 % y 95 %).",
     "sig", "puntos por °C"),
    (rb("4."), "Prueba de permutación (2.000 mezclas al azar)",
     "Mezclar al azar las temperaturas entre años y contar cuántas veces el azar produce un efecto tan grande como el real.",
     "sig", "puntos por °C"),
    (rb("5.", "Construcción"), "Placebo: construcción",
     "Prueba placebo: el mismo cálculo sobre un sector que no depende del clima. Si diera efecto, el resultado sería sospechoso.",
     "nosig", "puntos por °C"),
    (rb("5.", "Comercio"), "Placebo: comercio", "Idem, sobre el comercio.", "nosig", "puntos por °C"),
    (rb("5.", "Transporte"), "Placebo: transporte", "Idem, sobre el transporte.", "nosig", "puntos por °C"),
    (rb("5.", "financiera"), "Placebo: finanzas", "Idem, sobre la intermediación financiera.", "nosig", "puntos por °C"),
    (rb("6."), "Industria de alimentos y bebidas",
     "El calor debería notarse también en la industria que procesa lo que produce el campo.",
     "sig", "puntos por °C"),
    (rb("7."), "Efecto rezagado (año anterior)",
     "Efecto rezagado: ver si el calor de un año frena la producción del año siguiente.",
     "info", "puntos por °C"),
    (rb("8."), "Año muy cálido",
     "En vez de grados de más, mirar solo el 25 % de los años más cálidos de cada provincia.",
     "sig", "puntos"),
    (rb("9. Dosis-respuesta (econom"), "Dosis-respuesta: economía total",
     "Dosis-respuesta: si el clima realmente causa el daño, debería pegar más donde el sector expuesto pesa más. Se mira si el calor frena más a la economía de las provincias donde el campo pesa más.",
     "sig", "puntos por °C, por cada punto más de peso del campo"),
    (rb("9. Dosis-respuesta (por"), "Dosis-respuesta: ranking de provincias",
     "Correlación de Spearman (compara solo el orden, no los valores exactos): ¿las provincias donde el campo pesa más son las más golpeadas por los años secos?",
     "sig", "correlación de −1 a +1"),
]


def veredicto_prueba(p, esperado):
    if esperado == "info":
        return "Informativo"
    if esperado == "nosig":
        return "Pasa" if p >= 0.05 else "No pasa"
    return "Pasa" if p < 0.05 else ("Justo" if p < 0.10 else "No pasa")


evaluadas = [(*t, veredicto_prueba(t[0]["p_valor"], t[3])) for t in PRUEBAS]


def chances(p):
    """p-valor dicho en chances de casualidad: 0,026 -> '2,6 chances en 100'."""
    if p < 0.001:
        return "menos de 1 chance en 1.000"
    v = p * 100
    txt = f"{v:.0f}" if v >= 10 else f"{v:.1f}".replace(".", ",")
    return f"{txt} chances en 100"

n_pasa = sum(1 for e in evaluadas if e[-1] == "Pasa")
n_eval = sum(1 for e in evaluadas if e[-1] != "Informativo")
dosis = rb("9. Dosis-respuesta (econom")
p_holm = rb("1. Corrección", "Temperatura (+1 °C) → Producción")["p_valor"]


def tres_claves(tengo, demuestro, como):
    """Bloque fijo al inicio de cada pestaña: qué datos hay, qué se demuestra y con qué método (tres tarjetas de igual tamaño)."""
    claves(tengo, demuestro, como)


def detalle_lluvia_provincia():
    """Dentro del resultado sobre años secos: qué le pasaría a una provincia concreta si lloviera más.

    Solo lee tablas ya generadas: el efecto de los años secos por provincia, la correlación entre
    precipitación y crecimiento dentro de la provincia y la tendencia de su lluvia."""
    st.markdown("**¿Y si lloviera más en una provincia concreta?**")
    _ops = sorted(por_prov["jurisdiccion"].unique())
    _inicial = _ops.index("Córdoba") if "Córdoba" in _ops else 0
    prov = st.selectbox("Provincia", _ops, index=_inicial)

    _fila = por_prov[por_prov["jurisdiccion"] == prov].iloc[0]
    _c = corr_prov[
        (corr_prov["jurisdiccion"] == prov)
        & (corr_prov["variable_climatica"] == "precipitaciones_mm")
        & (corr_prov["metodo"] == "pearson")
    ].iloc[0]
    _t = tend_lluvia.loc[prov]
    _r, _p = float(_c["coeficiente"]), float(_c["p_valor"])
    _tend = float(_t["tendencia_precipitacion_por_decada"])
    _p_tend = float(_t["precipitacion_p_valor"])
    _campo = float(_fila["perdida_agro_pp"])
    if _campo < 0:
        _desc_campo = f"El campo creció {num(_fila['crec_agro_secos'])} % en los años secos y {num(_fila['crec_agro_normales'])} % en los normales: el golpe va en el sentido esperado."
        _estado_campo = "Señal débil"
    else:
        _desc_campo = (
            f"En los años secos el campo se portó {'mejor' if _campo > 0 else 'igual'} que en los normales "
            f"({num(_fila['crec_agro_secos'])} % frente a {num(_fila['crec_agro_normales'])} %): no aparece el golpe esperado."
        )
        _estado_campo = "No detectado"
    if _r > 0.05:
        _desc_corr = f"p = {num(_p, 2)}: más lluvia acompaña más crecimiento, pero no se distingue de la casualidad."
    elif _r < -0.05:
        _desc_corr = f"p = {num(_p, 2)}: la correlación apunta al revés de lo esperado y tampoco se distingue de la casualidad."
    else:
        _desc_corr = f"p = {num(_p, 2)}: no hay relación entre la lluvia y el crecimiento de la provincia."
    if _p_tend < 0.05:
        _desc_tend = f"La lluvia de {prov} viene {'bajando' if _tend < 0 else 'subiendo'} de forma consistente, con p = {num(_p_tend, 2)}."
    else:
        _desc_tend = f"No se ve una tendencia clara de la lluvia: p = {num(_p_tend, 2)}."

    tarjetas([
        dict(etiqueta="Campo en años secos", valor=num(_campo), u="puntos",
             unidad=f"{int(_fila['n_secos'])} años secos frente a {int(_fila['n_normales'])} normales",
             desc=_desc_campo,
             ayuda=ayuda("pp"), estado=_estado_campo),
        dict(etiqueta="Economía total", valor=num(_fila["perdida_total_pp"]), u="puntos",
             unidad="Afecta a toda la economía de la provincia, no solo al campo",
             desc=f"El campo representa el {num(_fila['peso_agro_medio_pct'])} % de su economía, y el resto de los sectores amortigua el golpe.",
             ayuda="Por eso el efecto sobre el campo puede ser grande y sobre el total de la provincia no distinguirse del azar.",
             estado="No detectado"),
        dict(etiqueta="Lluvia y crecimiento", valor=f"r = {num(_r, 2)}",
             unidad=f"Correlación dentro de la provincia, n = {int(_c['n_observaciones'])} años",
             desc=_desc_corr,
             ayuda=ayuda("pearson"),
             estado="Señal moderada" if _p < 0.05 else "No detectado"),
        dict(etiqueta="Tendencia de la lluvia", valor=num(_tend, 2), u="mm por década",
             unidad=f"Precipitación anual de {prov}, {años_lluvia}",
             desc=_desc_tend,
             ayuda=ayuda("tendencia_decada"),
             estado="Demostrado" if _p_tend < 0.05 else "No detectado"),
    ], minimo=215)
    explicacion(
        "Una distinción importante: el dato es la lluvia acumulada en el año, no la frecuencia. Una provincia puede tener "
        "la misma lluvia en dos temporales o en muchos chubascos repartidos, y para el campo eso es distinto. Con datos "
        "anuales no se puede separar; haría falta la serie mensual y un índice de sequía como el SPI. "
        f"Y estas cifras por provincia son orientativas: cada una tuvo entre 2 y 8 años secos, y entre las {int(sequia_panel['n_provincias'])} "
        f"provincias juntas la diferencia es de {num(sequia_panel['diferencia'])} puntos, con p = {num(sequia_panel['p_valor'], 2)}, "
        "es decir, en el promedio de las provincias tampoco se distingue del azar."
    )


# ---------------------------------------------------------------- respuesta de un vistazo
COLOR_NIVEL = {"Demostrado": "#2e7d4f", "Señal moderada": "#d98b1f", "Señal débil": "#d98b1f", "No detectado": "#8a8a8a"}
NIVELES = {
    "Demostrado": "green",
    "Señal moderada": "orange",
    "Señal débil": "orange",
    "No detectado": "gray",
}
resumen = [
    ("¿Argentina se está calentando?",
     f"Sí, sube un +{pend * 10:.2f} °C por década ≈ {pend * años_serie:.2f} °C en {años_serie} años, p < 0,001 "
     f"(la temperatura promedio del país sube unos {pend * 10:.2f} grados cada 10 años, y en {años_serie} años eso suma casi 1 grado; "
     "el signo ≈ quiere decir \"aproximadamente\"; y la p es la probabilidad de que la suba sea pura casualidad: acá es menor a 1 chance en 1.000, "
     "o sea que casi seguro es real).",
     "Demostrado"),
    ("¿El calor reduce el rendimiento de los cultivos?",
     f"Sí: maíz {rend.loc['Maíz', 'temp_pct_por_grado']:.1f} %, soja {rend.loc['Soja', 'temp_pct_por_grado']:.1f} % y trigo "
     f"{rend.loc['Trigo', 'temp_pct_por_grado']:.1f} % de rendimiento por cada °C más de calor en la temporada, p < 0,001 en los tres "
     "(por cada grado más de calor durante la temporada de cultivo, las toneladas que rinde cada hectárea caen alrededor de esos porcentajes; "
     "la p es la probabilidad de que el resultado sea casualidad, y acá es menor a 1 chance en 1.000. El efecto aparece en casi todas las "
     "provincias productoras y se sostiene al sacar provincias, mezclar los datos al azar y descontar la tendencia. El girasol no muestra "
     "efecto, y en la soja una de las pruebas de control no se cumple, por lo que su resultado es algo menos firme).",
     "Demostrado"),
    ("¿El calor frena la producción del campo?",
     f"Sí, el campo crece menos: {agro_temp['coeficiente_pp']:.1f} puntos de crecimiento por cada °C más, p = {agro_temp['p_valor']:.3f} "
     f"(en los años más calurosos de una provincia, su producción agropecuaria creció unos {abs(agro_temp['coeficiente_pp']):.1f} puntos porcentuales menos por cada grado de más: "
     f"si iba a crecer 4 %, cae 1,6 %; hay {chances(agro_temp['p_valor'])} de que sea casualidad, lo que es una pista con bastante respaldo pero no una prueba).",
     "Señal moderada"),
    ("¿Los años secos frenan al campo?",
     f"Posiblemente, pero no está confirmado: {agro_seco['coeficiente_pp']:.1f} puntos, p = {agro_seco['p_valor']:.2f} "
     f"(en los años de poca lluvia el campo creció unos {abs(agro_seco['coeficiente_pp']):.0f} puntos menos, pero hay {chances(agro_seco['p_valor'])} de que sea casualidad: "
     "no alcanza para asegurarlo).",
     "Señal débil"),
    ("¿Se nota en la economía total de las provincias?",
     f"No se detecta: calor {tot_temp['coeficiente_pp']:.1f} puntos por °C, p = {tot_temp['p_valor']:.2f}; año seco: {tot_seco['coeficiente_pp']:.1f} puntos, p = {tot_seco['p_valor']:.2f} "
     f"(en promedio no se ve efecto sobre toda la economía de la provincia: hay {chances(tot_temp['p_valor'])} y {chances(tot_seco['p_valor'])} de casualidad; "
     "el campo es solo una parte chica de esa economía y el resto tapa el golpe. Pero donde el campo pesa más, el calor sí pega más: ver pestaña 6).",
     "No detectado"),
    ("¿Se nota en el PBI per cápita del país?",
     f"No, no se ve relación: correlación {nac_pc.loc['Anomalía de temperatura', 'pearson_r']:.2f}, p = {nac_pc.loc['Anomalía de temperatura', 'p_valor']:.2f} "
     "(la correlación es un número de −1 a +1 que dice si dos cosas se mueven juntas; cerca de 0 es casi nada. "
     f"Acá casi no hay relación entre la temperatura y el crecimiento por habitante, y hay {chances(nac_pc.loc['Anomalía de temperatura', 'p_valor'])} de que lo poco que se ve sea casualidad).",
     "No detectado"),
    ("¿La señal del campo aguanta pruebas duras?",
     f"En buena parte sí: pasa {n_pasa} de {n_eval} pruebas; con la corrección de Holm, p = {p_holm:.2f} "
     f"(se le hicieron {n_eval} ataques a la señal y resistió {n_pasa}: por ejemplo, no aparece en sectores que no dependen del clima y el daño crece donde el campo pesa más. "
     f"Pero la corrección de Holm, que endurece el criterio porque se probaron 6 combinaciones y alguna sale bien por suerte, la deja en {chances(p_holm)} de casualidad: "
     "es una pista fuerte, no una prueba).",
     "Señal moderada"),
]

st.markdown(
    '<div class="resp-eyebrow">Respuesta a la pregunta central</div>'
    '<div class="resp-titulo">¿El cambio climático afecta a la economía argentina?</div>'
    '<div class="resp-lead">El clima de Argentina cambió con seguridad y el calor reduce el rendimiento de los cultivos. '
    'Ese efecto se diluye en el resto de la economía y no es detectable en el PBI total ni en el PBI per cápita del país.</div>',
    unsafe_allow_html=True,
)
_anom = nacional[["año", "anomalia_temperatura"]].dropna().sort_values("año")["anomalia_temperatura"].rolling(5, min_periods=1).mean()
_r = nac_pc.loc["Anomalía de temperatura", "pearson_r"]
_n = int(nac_pc.loc["Anomalía de temperatura", "n"])
_z, _se = np.arctanh(_r), 1 / np.sqrt(_n - 3)
_r_inf, _r_sup = np.tanh(_z - 1.96 * _se), np.tanh(_z + 1.96 * _se)
_todos = rend.loc["Todos los cultivos"]
tarjetas([
    dict(etiqueta="Calentamiento", valor=f"+{num(pend * 10, 2)}", u="°C por década", unidad="Temperatura media del país, 1961-2025",
         grafico=svg_linea(_anom, COLOR_ESTADO["Demostrado"]), desc="La línea muestra la anomalía de temperatura de cada año, suavizada.",
         ayuda=ayuda("tendencia_decada"), estado="Demostrado"),
    dict(etiqueta="Rendimiento", valor=f"{num(_todos['temp_pct_por_grado'])} %", u="por °C", unidad="Promedio de soja, maíz, trigo y girasol",
         grafico=svg_rango(_todos["temp_pct_por_grado"], _todos["temp_ic95_inf"], _todos["temp_ic95_sup"], COLOR_ESTADO["Demostrado"]),
         desc="Cambio del rendimiento por cada grado más de calor en la temporada de cultivo.",
         ayuda="El punto es el efecto estimado; la barra, su rango probable (95 %). Si la barra no toca el cero (línea punteada), el efecto es firme.",
         estado="Demostrado"),
    dict(etiqueta="Economía total", valor=f"{num(tot_temp['coeficiente_pp'])}", u="puntos por °C", unidad="Efecto del calor sobre toda la economía provincial",
         grafico=svg_rango(tot_temp["coeficiente_pp"], tot_temp["ic95_inf"], tot_temp["ic95_sup"], COLOR_ESTADO["No detectado"]),
         desc="La barra cruza el cero: no se puede asegurar que haya efecto.",
         ayuda="El campo es una parte chica de la economía de cada provincia y el resto de los sectores tapa el golpe.", estado="No detectado"),
    dict(etiqueta="PBI per cápita", valor=f"r = {num(_r, 2)}", unidad="Correlación con la temperatura del país, 1961-2022",
         grafico=svg_rango(_r, _r_inf, _r_sup, COLOR_ESTADO["No detectado"]),
         desc="La barra cruza el cero: casi ninguna relación entre el calor y el crecimiento por habitante.", ayuda=ayuda("pearson"), estado="No detectado"),
])

st.markdown("##### Detalle de cada resultado")
for _i, (preg, dato, nivel) in enumerate(resumen):
    with st.expander(f"{preg}  ·  :{NIVELES[nivel]}[**{nivel}**]"):
        st.markdown(dato)
        if _i == 3:
            detalle_lluvia_provincia()
explicacion(
    "Cómo leerlo: verde = comprobado; naranja = una pista que apunta en esa dirección pero sin seguridad total; gris = con estos datos "
    "no se ve nada (no significa que no exista). En cada resultado, lo que está entre paréntesis explica lo que está antes. "
    f"La \"p\" ({termino('p-valor', 'p_valor')}) mide qué tan probable es que el resultado sea pura casualidad: cuanto más chica, más seguro. "
    "Las definiciones completas están en el glosario al final de la página Conclusiones."
)

t_pregunta, t_clima, t_pais, t_campo, t_cultivos, t_donde, t_pruebas, t_veredicto = st.tabs([
    "La pregunta",
    "1 · El clima",
    "2 · La economía",
    "3 · El campo",
    "4 · Cultivos",
    "5 · Dónde pega",
    "6 · Pruebas",
    "Veredicto",
])

# ================================================================ LA PREGUNTA
with t_pregunta:
    st.markdown("## ¿El cambio climático le pega a la economía de los argentinos?")
    st.markdown(
        "Detrás de cada punto de PBI hay trabajo, producción y familias que viven de lo que "
        "se produce en el país. Por eso la pregunta no es solo estadística: es saber "
        "**quién paga el costo cuando el clima cambia** y si el país está preparado para "
        "cuidar a los que producen."
    )
    para_que(
        "Ordenar todo el proyecto detrás de una sola pregunta y mostrar, paso a paso y con datos "
        "reales, qué se puede afirmar y qué no."
    )
    paneles([
        ("El trabajo",
         "Cuando una cosecha se pierde o una provincia produce menos, no baja solo un número: baja el empleo, el ingreso de los productores "
         "y la actividad de todo el pueblo que vive alrededor."),
        ("El interior productivo",
         f"En las 8 provincias más agropecuarias, el campo es entre el {peso_min:.0f} % y el {peso_max:.0f} % de la economía. "
         "Si el clima las golpea, la primera afectada es la producción del interior."),
        ("La justicia entre regiones",
         "El clima no cambia igual en todo el país y las economías provinciales no dependen de lo mismo. Saber dónde pega más "
         "permite decidir dónde hace falta más apoyo del Estado."),
    ])

    st.space("small")
    st.markdown("### Cómo se responde, en 6 pasos")
    st.markdown(
        """
1. **¿El clima realmente cambió?** Se mide el calentamiento de Argentina y de cada provincia.
2. **¿Se nota en la economía del país?** Se compara el PBI per cápita con el clima, año por año.
3. **¿Se nota en el campo?** Se mira el sector más expuesto al clima, provincia por provincia.
4. **¿Se nota en los cultivos?** Se mide cuánto rinde menos cada hectárea de soja, maíz, trigo y girasol cuando hace más calor.
5. **¿Dónde pega más?** Se busca qué provincias pierden más cuando el clima es adverso.
6. **¿La señal aguanta pruebas duras?** Se intenta romper el resultado del campo de varias maneras; si sobrevive, es más creíble.
"""
    )
    explicacion(
        "Regla del proyecto: se muestra lo que dicen los datos, aunque no sea lo que uno esperaba. "
        "Que dos cosas se muevan juntas no prueba que una cause la otra; por eso cada resultado "
        "aclara qué tan fuerte es la evidencia."
    )

# ================================================================ 1. EL CLIMA CAMBIÓ
with t_clima:
    st.subheader("1 · ¿El clima realmente cambió?")
    para_que("Confirmar que hay un cambio climático medible en Argentina antes de preguntarse por sus efectos.")
    tres_claves(
        "Temperatura de Argentina año por año, 1961-2025 (CIAM/SMN), y de las 24 jurisdicciones, 1981-2025 (NASA POWER).",
        "Que Argentina se calienta y que lo hace en todas las provincias, aunque a distinto ritmo.",
        "Se traza la línea de tendencia (hacia dónde van los datos con los años) de la temperatura y se calcula el p-valor "
        "(la probabilidad de que esa pendiente sea pura casualidad; cuanto más chico, más seguro).",
    )
    tarjetas([
        dict(etiqueta="Calentamiento por década", valor=f"+{num(pend * 10, 2)}", u="°C", unidad="Tendencia 1961-2025", ayuda=ayuda("tendencia_decada")),
        dict(etiqueta="Calentamiento acumulado", valor=f"+{num(pend * años_serie, 2)}", u="°C", unidad=f"En {años_serie} años",
             desc="Lo que subió la temperatura media del país entre el primer y el último año de la serie, según la tendencia."),
        dict(etiqueta="¿Es casualidad?", valor="p < 0,001", unidad="Menos de 1 chance en 1.000",
             desc="Probabilidad de que la suba de temperatura sea pura casualidad.", ayuda=ayuda("p_valor")),
    ])

    d = nacional[["año", "anomalia_temperatura"]].dropna()
    coef = np.polyfit(d["año"], d["anomalia_temperatura"], 1)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=d["año"], y=d["anomalia_temperatura"], name="Anomalía de cada año",
        marker_color=np.where(d["anomalia_temperatura"] >= 0, "#c0392b", "#2e6fa3"),
    ))
    fig.add_trace(go.Scatter(x=d["año"], y=np.polyval(coef, d["año"]), name="Tendencia", line=dict(color="black", width=3)))
    fig.update_layout(
        xaxis_title="Año", yaxis_title="Anomalía de temperatura (°C)", height=430,
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig, width="stretch")
    explicacion(
        f"Cada barra es un año: <strong>roja</strong> si fue más cálido que lo normal "
        f"(promedio 1991-2020) y <strong>azul</strong> si fue más frío. Las azules dominan al principio "
        f"y las rojas al final: el país se calienta. La línea negra es la {termino('tendencia', 'tendencias')}."
    )

    orden = tend_prov.assign(por_decada=tend_prov["pendiente"] * 10).sort_values("por_decada")
    fig2 = px.bar(
        orden, x="por_decada", y="jurisdiccion", orientation="h", color="por_decada",
        color_continuous_scale="OrRd",
        labels={"por_decada": "Calentamiento (°C por década)", "jurisdiccion": "", "color": ""},
    )
    fig2.update_layout(height=650, coloraxis_showscale=False)
    st.plotly_chart(fig2, width="stretch")
    explicacion(
        "Todas las provincias se calientan, unas más que otras. Barras horizontales y ordenadas para comparar "
        "el número exacto de las 24 jurisdicciones. Datos: NASA POWER (estimación satelital), 1981-2025."
    )
    explicacion("<strong>Conclusión del paso 1:</strong> el cambio climático en Argentina es un hecho medible y estadísticamente sólido.")

# ================================================================ 2. LA ECONOMÍA DEL PAÍS
with t_pais:
    st.subheader("2 · ¿Se nota en la economía del país?")
    para_que(
        f"Comparar, año por año, cuánto creció el {termino('PBI per cápita', 'pbi_per_capita')} "
        "(lo que produce el país por habitante) con cómo fue el clima ese año."
    )
    tres_claves(
        "PBI per cápita de Argentina, 1961-2022 (62 años, Maddison Project vía OWID), junto con temperatura, lluvia y CO₂ de cada año.",
        "Que a nivel país, con estos datos, no se detecta relación entre el clima y el PBI per cápita.",
        "Se comparan año por año el clima y el crecimiento por habitante (correlación: un número de −1 a +1 que dice si dos cosas "
        "se mueven juntas) y se contrastan los años secos con los normales (prueba t: compara dos promedios y dice si la diferencia puede ser casualidad).",
    )
    x = nacional[["año", "anomalia_temperatura", "pib_per_capita_crecimiento_pct"]].dropna()
    fig = px.scatter(
        x, x="anomalia_temperatura", y="pib_per_capita_crecimiento_pct", hover_name="año", trendline="ols",
        trendline_color_override="black",
        labels={"anomalia_temperatura": "Anomalía de temperatura (°C)", "pib_per_capita_crecimiento_pct": "Crecimiento del PBI per cápita (%)"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, width="stretch")
    r = nac_pc.loc["Anomalía de temperatura"]
    explicacion(
        f"Cada punto es un año (pasá el mouse para ver cuál). Si el calor frenara la economía por habitante, los puntos "
        f"bajarían de izquierda a derecha. Se ve una leve inclinación, pero los puntos están muy dispersos: "
        f"{termino('correlación', 'pearson')} de {r['pearson_r']:.2f} (cerca de 0 = casi ninguna relación) con p = {r['p_valor']:.2f} "
        f"(hay {chances(r['p_valor'])} de que lo poco que se ve sea casualidad), es decir, "
        f"<strong>no se distingue de la casualidad</strong> ({int(r['n'])} años, hasta 2022)."
    )

    c1, c2 = st.columns(2)
    with c1:
        pc = sequia_nac.loc["pib_per_capita_crecimiento_pct"]
        comp = pd.DataFrame({
            "Tipo de año": ["Años secos", "Años normales"],
            "Crecimiento del PBI per cápita (%)": [pc["media_crecimiento_secos"], pc["media_crecimiento_normales"]],
        })
        fig = px.bar(comp, x="Tipo de año", y="Crecimiento del PBI per cápita (%)", color="Tipo de año",
                     color_discrete_sequence=["#c8842b", "#4a7c59"], text_auto=".2f")
        fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig, width="stretch")
        explicacion(
            f"Promedio de crecimiento por habitante en {int(pc['n_años_secos'])} años secos contra {int(pc['n_años_normales'])} "
            f"normales: prácticamente igual (p = {pc['p_valor']:.2f}: {chances(pc['p_valor'])} de que la diferencia sea casualidad). Un {termino('año seco', 'año_seco')} es "
            "uno de lluvia en el 25 % más bajo de la historia."
        )
    with c2:
        tabla = nac_pc.reset_index().rename(columns={"variable": "Variable", "pearson_r": "Correlación", "p_valor": "p-valor", "n": "Años"})
        st.dataframe(
            tabla, hide_index=True,
            column_config={
                "Correlación": st.column_config.NumberColumn(format="%.3f", help=ayuda("pearson")),
                "p-valor": st.column_config.NumberColumn(format="%.3f", help=ayuda("p_valor")),
                "Años": st.column_config.NumberColumn(help="Cantidad de años comparados."),
            },
        )
        explicacion(
            "Ninguna de las tres variables climáticas ni el CO₂ muestra una relación significativa con el "
            "crecimiento del PBI per cápita del país."
        )
        explicacion(
        "<strong>Conclusión del paso 2:</strong> a nivel país, con estos datos, no se detecta relación entre el clima y el PBI per cápita. "
        "Eso <strong>no significa que no exista</strong>: puede quedar escondida en el promedio, porque un país tiene muchos sectores y "
        "muchas regiones. El paso siguiente mira dónde debería notarse primero."
    )

# ================================================================ 3. EL CAMPO
with t_campo:
    st.subheader("3 · ¿Se nota en el campo?")
    para_que(
        "Mirar el sector más expuesto al clima (la producción agropecuaria) en las 24 provincias, y compararlo con la "
        "economía total de cada una. Si el clima pega en algún lado, debería notarse acá primero."
    )
    tres_claves(
        f"Producción por sector de las 24 provincias, 2005-2023 (CEPAL), cruzada con temperatura y lluvia provinciales (NASA POWER): {len(panel)} observaciones.",
        "Que el calor frena el crecimiento del campo (señal moderada) y que en la economía total el efecto no se detecta.",
        "Regresión con efectos fijos: compara cada provincia contra sí misma y contra lo que le pasó a todo el país ese año, "
        "para aislar el efecto del clima.",
    )
    st.markdown(
        f"Se compararon **{len(panel)} observaciones** (24 provincias × 19 años, 2005-2023). La comparación descuenta "
        f"lo propio de cada provincia y lo que le pasa a todo el país en un mismo año (crisis, pandemia), con "
        f"{termino('efectos fijos', 'efectos_fijos')} (un cálculo que compara cada provincia contra sí misma, por ejemplo un año caluroso de Córdoba contra uno normal de Córdoba). "
        f"El resultado se expresa en {termino('puntos porcentuales', 'pp')} de crecimiento (la diferencia entre dos porcentajes: si el campo iba a crecer 4 % y creció 1 %, perdió 3 puntos)."
    )

    r = res.copy()
    r["etiqueta"] = r["factor"] + " → " + r["resultado"]
    r["significativo"] = np.where(r["p_valor"] < 0.05, "Estadísticamente significativo", "No se distingue de la casualidad")
    r = r.iloc[::-1]
    fig = go.Figure()
    for sig, color in [("Estadísticamente significativo", "#c0392b"), ("No se distingue de la casualidad", "#8a8a8a")]:
        s = r[r["significativo"] == sig]
        fig.add_trace(go.Scatter(
            x=s["coeficiente_pp"], y=s["etiqueta"], mode="markers", name=sig, marker=dict(size=13, color=color),
            error_x=dict(type="data", symmetric=False, array=s["ic95_sup"] - s["coeficiente_pp"], arrayminus=s["coeficiente_pp"] - s["ic95_inf"], color=color),
            customdata=s[["p_valor"]], hovertemplate="%{y}<br>Efecto: %{x:.2f} puntos<br>p = %{customdata[0]:.3f}<extra></extra>",
        ))
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    fig.update_layout(
        xaxis_title="Efecto sobre el crecimiento (puntos porcentuales)", yaxis_title="", height=430,
        legend=dict(orientation="h", y=-0.25),
    )
    st.plotly_chart(fig, width="stretch")
    explicacion(
        f"Cada punto es el efecto estimado y la línea es su {termino('intervalo de confianza del 95 %', 'ic95')}: "
        "el rango donde probablemente está el efecto real. <strong>Si la línea cruza el cero</strong> (línea punteada), no se puede "
        "asegurar que el efecto exista. Punto a la izquierda del cero = el clima adverso frena el crecimiento."
    )

    tarjetas([
        dict(etiqueta="Calor → campo", valor=f"{num(agro_temp['coeficiente_pp'])}", unidad="puntos por cada °C más",
             desc=f"p = {num(agro_temp['p_valor'], 3)}: {chances(agro_temp['p_valor'])} de que sea casualidad.",
             ayuda="Por cada °C más cálido que lo normal en una provincia, la producción agropecuaria crece en promedio esta cantidad de puntos porcentuales menos."),
        dict(etiqueta="Año seco → campo", valor=f"{num(agro_seco['coeficiente_pp'])}", unidad="puntos en un año seco",
             desc=f"p = {num(agro_seco['p_valor'], 2)}: {chances(agro_seco['p_valor'])} de que sea casualidad.",
             ayuda="Efecto de un año seco sobre el crecimiento agropecuario. Negativo, pero no alcanza significancia estadística."),
        dict(etiqueta="Calor → economía total", valor=f"{num(tot_temp['coeficiente_pp'])}", unidad="puntos por cada °C más",
             desc=f"p = {num(tot_temp['p_valor'], 2)}: {chances(tot_temp['p_valor'])} de que sea casualidad.",
             ayuda="Mismo cálculo, pero sobre toda la economía de la provincia. Diluido: el campo es solo una parte."),
        dict(etiqueta="Año seco → economía total", valor=f"{num(tot_seco['coeficiente_pp'])}", unidad="puntos en un año seco",
             desc=f"p = {num(tot_seco['p_valor'], 2)}: {chances(tot_seco['p_valor'])} de que sea casualidad.",
             ayuda="Efecto de un año seco sobre el crecimiento de toda la economía provincial. No se distingue de cero."),
    ])

    # gráfico de dispersión con efectos fijos removidos
    p = panel.copy()
    for col in ["crec_agro", "temp_anom"]:
        p[col + "_aj"] = p[col] - p.groupby("jurisdiccion")[col].transform("mean") - p.groupby("año")[col].transform("mean") + p[col].mean()
    fig = px.scatter(
        p, x="temp_anom_aj", y="crec_agro_aj", hover_data=["jurisdiccion", "año"], trendline="ols", trendline_color_override="black",
        opacity=0.6,
        labels={"temp_anom_aj": "Calor del año, respecto de lo normal en esa provincia (°C)", "crec_agro_aj": "Crecimiento agropecuario ajustado (puntos)"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, width="stretch")
    explicacion(
        "Cada punto es una provincia en un año. Los valores están ajustados: se les quitó lo que es propio de cada provincia y lo "
        "que le pasó a todo el país ese año, para que quede solo el efecto del calor. La recta baja: en los años más cálidos de una "
        "provincia, su producción agropecuaria creció menos. Hay mucha dispersión, por eso el resultado es una señal y no una prueba definitiva."
    )
    explicacion(
        f"<strong>Conclusión del paso 3:</strong> hay una señal en el campo. Con más calor, la producción agropecuaria crece unos "
        f"{abs(agro_temp['coeficiente_pp']):.1f} puntos menos por cada °C (p = {agro_temp['p_valor']:.3f}: {chances(agro_temp['p_valor'])} de que sea casualidad), y los años secos también "
        f"apuntan en esa dirección ({agro_seco['coeficiente_pp']:.1f} puntos), aunque este último no alcanza significancia (con p = {agro_seco['p_valor']:.2f} sigue habiendo demasiada chance de casualidad para asegurarlo). "
        f"En la economía total de la provincia el efecto es mucho menor y no se distingue de cero: incluso en las 8 provincias más "
        f"agropecuarias el campo es solo entre el {peso_min:.0f} % y el {peso_max:.0f} % de la economía, y el resto la amortigua."
    )

# ================================================================ 4. LOS CULTIVOS
with t_cultivos:
    st.subheader("4 · ¿El calor reduce el rendimiento de los cultivos?")
    para_que(
        "Medir el efecto del clima donde es más directo: cuánto rinde cada hectárea (kilos por hectárea) de cada cultivo. "
        "El rendimiento no depende de los precios ni de cuánta superficie se decidió sembrar."
    )
    tres_claves(
        f"Rendimiento de soja, maíz, trigo y girasol por provincia y campaña, 1981-2023 (Ministerio de Economía, "
        f"{int(rend.loc['Todos los cultivos', 'n']):,} observaciones".replace(",", ".") + "), cruzado con la temperatura y la lluvia de la "
        "temporada de cultivo de cada provincia (NASA POWER).",
        "Que el calor de la temporada reduce el rendimiento de maíz, soja y trigo en casi todas las provincias productoras; "
        "el girasol no muestra efecto detectable.",
        "Regresión con efectos fijos sobre el logaritmo del rendimiento (por eso el resultado se lee en porcentaje): compara cada provincia "
        "contra sí misma y descuenta lo que le pasó a todo el país en cada campaña, incluido el avance tecnológico.",
    )
    items_c = []
    for cult in ["Maíz", "Soja", "Trigo", "Girasol"]:
        r = rend.loc[cult]
        p_txt = "p < 0,001" if r["temp_p"] < 0.001 else f"p = {num(r['temp_p'], 4 if r['temp_p'] < 0.01 else 2)}"
        firme = r["temp_p"] < 0.05
        items_c.append(dict(
            etiqueta=cult, valor=f"{num(r['temp_pct_por_grado'])} %", u="por °C", unidad=f"{p_txt}: {chances(r['temp_p'])} de casualidad",
            grafico=svg_rango(r["temp_pct_por_grado"], r["temp_ic95_inf"], r["temp_ic95_sup"], COLOR_ESTADO["Demostrado"] if firme else COLOR_ESTADO["No detectado"]),
            desc=f"{int(r['provincias'])} provincias, campañas {r['anios']}.",
            ayuda="El punto es el efecto estimado sobre el rendimiento; la barra, su rango probable (95 %). Si toca el cero, no se puede asegurar el efecto.",
            estado="Demostrado" if firme else "No detectado",
        ))
    tarjetas(items_c)

    st.markdown("**¿Cuánto rinde menos cada cultivo por cada grado más de calor?**")
    orden_c = ["Maíz", "Soja", "Trigo", "Girasol", "Todos los cultivos"]
    d = rend.loc[orden_c].reset_index()
    d["sig"] = np.where(d["temp_p"] < 0.05, "Estadísticamente significativo", "No se distingue de la casualidad")
    fig = go.Figure()
    for sig, color in [("Estadísticamente significativo", "#c0392b"), ("No se distingue de la casualidad", "#8a8a8a")]:
        x = d[d["sig"] == sig]
        fig.add_trace(go.Scatter(
            x=x["temp_pct_por_grado"], y=x["cultivo"], mode="markers", name=sig, marker=dict(size=13, color=color),
            error_x=dict(type="data", symmetric=False, array=x["temp_ic95_sup"] - x["temp_pct_por_grado"],
                         arrayminus=x["temp_pct_por_grado"] - x["temp_ic95_inf"], color=color),
            customdata=x[["temp_p"]], hovertemplate="%{y}<br>Efecto: %{x:.1f} %<br>p = %{customdata[0]:.4f}<extra></extra>",
        ))
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(xaxis_title="Cambio del rendimiento por cada °C más de calor (%)", yaxis_title="", height=400,
                      legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig, width="stretch")
    explicacion(
        f"Cada punto es el efecto estimado y la línea es su {termino('intervalo de confianza del 95 %', 'ic95')} (el rango donde probablemente "
        "está el efecto real): si cruza el cero (línea punteada), no se puede asegurar que el efecto exista. Se usa este gráfico porque "
        "la pregunta es cuánto y con qué certeza, y cada cultivo tiene una escala propia de rendimiento. A la izquierda del cero, el "
        "calor reduce el rendimiento."
    )

    st.markdown("**¿Pasa en todas las provincias o solo en algunas?**")
    dp = rend_prov[rend_prov["cultivo"].isin(["Maíz", "Soja", "Trigo", "Girasol"])].copy()
    dp["Significancia"] = np.where(dp["temp_p"] < 0.05, "Significativo (p < 0,05)", "No significativo")
    fig_p = px.scatter(
        dp.sort_values("jurisdiccion", ascending=False), x="temp_pct_por_grado", y="jurisdiccion", color="Significancia",
        facet_col="cultivo", facet_col_spacing=0.03, category_orders={"cultivo": ["Maíz", "Soja", "Trigo", "Girasol"]},
        color_discrete_map={"Significativo (p < 0,05)": "#c0392b", "No significativo": "#b0b0b0"},
        labels={"temp_pct_por_grado": "Cambio del rendimiento por °C (%)", "jurisdiccion": ""},
    )
    fig_p.add_vline(x=0, line_dash="dash", line_color="gray")
    fig_p.update_layout(height=520, legend=dict(orientation="h", y=-0.15, title=""))
    fig_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig_p, width="stretch")
    sig_n = {c: int(((dp["cultivo"] == c) & (dp["temp_pct_por_grado"] < 0)).sum()) for c in ["Maíz", "Soja", "Trigo", "Girasol"]}
    tot_n = {c: int((dp["cultivo"] == c).sum()) for c in sig_n}
    explicacion(
        "Un panel por cultivo y un punto por provincia, porque la pregunta es si el efecto se repite provincia por provincia y no depende "
        "de una sola. Cada provincia se estima sola, con solo 12 a 42 campañas, por lo que muchos puntos individuales no llegan a ser "
        f"significativos; lo que importa es el conjunto: el efecto es negativo en {sig_n['Maíz']} de {tot_n['Maíz']} provincias de maíz, "
        f"{sig_n['Soja']} de {tot_n['Soja']} de soja, {sig_n['Trigo']} de {tot_n['Trigo']} de trigo y {sig_n['Girasol']} de {tot_n['Girasol']} de girasol."
    )

    st.markdown("**¿Se ve también en el rendimiento de todo el país?**")
    dn = rend_nac.loc[["Maíz", "Soja", "Trigo", "Girasol"]].reset_index()
    dn["sig"] = np.where(dn["temp_p"] < 0.05, "Estadísticamente significativo", "Al borde (p entre 0,05 y 0,10)")
    fig_n = go.Figure()
    for sig, color in [("Estadísticamente significativo", "#c0392b"), ("Al borde (p entre 0,05 y 0,10)", "#d98b1f")]:
        x = dn[dn["sig"] == sig]
        fig_n.add_trace(go.Scatter(
            x=x["temp_pct_por_grado"], y=x["cultivo"], mode="markers", name=sig, marker=dict(size=13, color=color),
            error_x=dict(type="data", symmetric=False, array=x["temp_ic95_sup"] - x["temp_pct_por_grado"],
                         arrayminus=x["temp_pct_por_grado"] - x["temp_ic95_inf"], color=color),
            customdata=x[["temp_p"]], hovertemplate="%{y}<br>Efecto: %{x:.1f} %<br>p = %{customdata[0]:.3f}<extra></extra>",
        ))
    fig_n.add_vline(x=0, line_dash="dash", line_color="gray")
    fig_n.update_yaxes(autorange="reversed")
    fig_n.update_layout(xaxis_title="Cambio del rendimiento nacional por °C (%)", yaxis_title="", height=340,
                        legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig_n, width="stretch")
    explicacion(
        "Serie del país entero (rendimiento nacional de cada campaña contra el calor promedio de las provincias productoras, con "
        "tendencia lineal que descuenta el avance tecnológico y errores robustos a que un año se parezca al anterior). Con solo 42 "
        "campañas hay menos precisión que en el panel provincial, por eso los rangos son más anchos: el girasol y el trigo son "
        "significativos y la soja y el maíz quedan al borde, con el mismo signo."
    )
    tarjetas([
        dict(etiqueta=f"{cult}: pérdida por °C", valor=f"{num(rend_nac.loc[cult, 'perdida_mt_por_grado'])} Mt", unidad="millones de toneladas",
             desc=f"Sobre {num(rend_nac.loc[cult, 'produccion_reciente_mt'], 0)} millones de toneladas de producción reciente.",
             ayuda="Orden de magnitud: el porcentaje estimado a nivel país aplicado a la producción promedio de las últimas cinco campañas. "
                   "Es una estimación con incertidumbre, no una predicción.")
        for cult in ["Maíz", "Soja", "Trigo", "Girasol"]
    ])

    st.markdown("**¿Aguanta las pruebas de control?**")
    ctrl = pd.DataFrame({
        "Cultivo": rend.index,
        "Efecto (% por °C)": rend["temp_pct_por_grado"].round(1).values,
        "p": rend["temp_p"].values,
        "Mezclando al azar (p)": rend["temp_p_permutacion"].values,
        "Sacando de a una provincia": rend["sacar_provincia_significativas"].values,
        "Con tendencia propia por provincia (p)": rend["temp_p_con_tendencia"].values,
        "Placebo: clima de la campaña siguiente (p)": rend["placebo_temp_futura_p"].values,
        "Placebo": np.where(rend["placebo_temp_futura_p"].values >= 0.05, "Pasa", "No pasa"),
    })
    tabla_html(
        ["Cultivo", "Efecto (% por °C)", "p", "Mezclando al azar (p)", "Sacando de a una provincia", "Con tendencia propia (p)", "Placebo: clima siguiente (p)", "Placebo"],
        [[r["Cultivo"], num(r["Efecto (% por °C)"]), num(r["p"], 4), num(r["Mezclando al azar (p)"], 3), r["Sacando de a una provincia"],
          num(r["Con tendencia propia por provincia (p)"], 4), num(r["Placebo: clima de la campaña siguiente (p)"], 4), r["Placebo"]] for _, r in ctrl.iterrows()],
        anchos=[13, 11, 9, 13, 15, 13, 15, 11], col_estado=7, col_num=(1, 2, 3, 5, 6),
    )
    explicacion(
        "Las pruebas de control intentan romper el resultado: sacar provincias, mezclar los datos al azar, permitir una tendencia propia de cada "
        f"provincia y un {termino('placebo', 'placebo')} con el clima de la campaña siguiente (que no puede haber afectado la cosecha). "
        "Maíz y trigo pasan todas. En la soja el placebo no se cumple (p = "
        f"{rend.loc['Soja', 'placebo_temp_futura_p']:.4f}): el clima de la campaña siguiente también aparece asociado, lo que indica que parte de su "
        "efecto podría deberse a otra cosa; por eso el resultado de la soja es menos firme. El girasol no muestra efecto."
    )

    pend_temp = rend.loc["Todos los cultivos", "calentamiento_temporada_por_decada"]
    explicacion(
        f"<strong>Conclusión del paso 4:</strong> el calor de la temporada de cultivo reduce el rendimiento: alrededor de "
        f"{abs(rend.loc['Maíz', 'temp_pct_por_grado']):.0f} % en el maíz, {abs(rend.loc['Trigo', 'temp_pct_por_grado']):.0f} % en el trigo y "
        f"{abs(rend.loc['Soja', 'temp_pct_por_grado']):.0f} % en la soja por cada grado más, con el mismo signo en casi todas las provincias y "
        f"efecto significativo también en el total del país para el trigo y el girasol. Es una asociación estadística sólida, no una prueba de "
        f"causalidad. Como las temporadas se calentaron unos {pend_temp:.2f} °C por década, el efecto acumulado ya medido ronda "
        f"{abs(rend.loc['Todos los cultivos', 'efecto_por_decada_pct']):.1f} % por década; el riesgo grande está en los años calurosos, donde "
        "cada grado de más se lleva cerca de una décima parte de la cosecha."
    )

# ================================================================ 5. DÓNDE PEGA MÁS
with t_donde:
    st.subheader("5 · ¿Dónde pega más?")
    para_que(
        "Ver qué provincias vieron caer más su producción agropecuaria en los años secos, y si eso tiene que ver con cuánto "
        "depende su economía del campo."
    )
    tres_claves(
        "Para cada provincia: crecimiento del campo y de la economía total en años secos y en años normales, y el peso del campo en su economía.",
        "Que el golpe de los años secos al campo no es igual en todas las provincias y que las más agropecuarias tienden a sentirlo más.",
        "Se compara, provincia por provincia, el crecimiento en años secos contra años normales. "
        "Cada provincia tiene pocos años secos (2 a 8), por eso es orientativo (con tan pocos datos no se puede estar seguro). "
        "\"Puntos\" es la diferencia entre dos porcentajes de crecimiento.",
    )
    d = por_prov.sort_values("perdida_agro_pp")
    fig = px.bar(
        d, x="perdida_agro_pp", y="jurisdiccion", orientation="h", color="peso_agro_medio_pct", color_continuous_scale="YlOrBr",
        hover_data={"n_secos": True, "peso_agro_medio_pct": ":.1f", "perdida_agro_pp": ":.1f"},
        labels={"perdida_agro_pp": "Diferencia de crecimiento agropecuario: años secos menos años normales (puntos)",
                "jurisdiccion": "", "peso_agro_medio_pct": "Peso del campo en la economía (%)"},
    )
    fig.update_layout(height=700)
    st.plotly_chart(fig, width="stretch")
    explicacion(
        "Cada barra muestra cuántos puntos menos creció el campo de esa provincia en los años secos comparado con los normales. "
        "El color indica cuánto pesa el campo en su economía (más oscuro = más dependiente). Barras a la izquierda = el campo la pasa peor cuando falta agua."
    )

    fig = px.scatter(
        por_prov, x="peso_agro_medio_pct", y="perdida_total_pp", text="jurisdiccion", size="n_secos",
        labels={"peso_agro_medio_pct": "Peso del campo en la economía de la provincia (%)",
                "perdida_total_pp": "Diferencia de crecimiento de toda la economía: años secos menos normales (puntos)"},
    )
    fig.update_traces(textposition="top center", textfont_size=9)
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(height=520)
    st.plotly_chart(fig, width="stretch")
    explicacion(
        f"{termino('Gráfico de dispersión', 'dispersion')}: si las provincias más agropecuarias sufrieran más los años secos, los puntos de la derecha "
        "estarían por debajo de cero. Se ve algo de eso en Córdoba, Entre Ríos y Santa Fe, pero no en todas (Santiago del Estero y La Pampa "
        "crecieron igual). Cada provincia tiene solo entre 2 y 8 años secos, por lo que son datos orientativos."
    )
    tabla = por_prov[["jurisdiccion", "peso_agro_medio_pct", "n_secos", "crec_agro_secos", "crec_agro_normales", "perdida_agro_pp"]].sort_values("perdida_agro_pp")
    st.dataframe(
        tabla, hide_index=True,
        column_config={
            "jurisdiccion": "Provincia",
            "peso_agro_medio_pct": st.column_config.NumberColumn("Peso del campo (%)", format="%.1f", help="Qué parte de la economía de la provincia corresponde a la producción agropecuaria."),
            "n_secos": st.column_config.NumberColumn("Años secos", help="Cantidad de años secos en el período comparado."),
            "crec_agro_secos": st.column_config.NumberColumn("Crecimiento del campo en años secos (%)", format="%.1f"),
            "crec_agro_normales": st.column_config.NumberColumn("Crecimiento del campo en años normales (%)", format="%.1f"),
            "perdida_agro_pp": st.column_config.NumberColumn("Diferencia (puntos)", format="%.1f", help=ayuda("pp")),
        },
    )

# ================================================================ 5. ¿AGUANTA LAS PRUEBAS?
with t_pruebas:
    st.subheader("6 · ¿La señal del campo aguanta pruebas duras?")
    para_que(
        "Una señal solo vale si sobrevive a intentos serios de romperla. Acá se la ataca de varias maneras distintas: "
        "las que pasa la hacen más creíble; las que no pasa se dicen igual."
    )
    tres_claves(
        "El mismo panel del paso 3 (24 provincias × 19 años, 456 datos) y la producción de todos los sectores de cada provincia (CEPAL), "
        "incluidos los que no dependen del clima.",
        f"Que la señal del calor sobre el campo pasa {n_pasa} de {n_eval} pruebas y que el calor pega más donde el campo pesa más. "
        "También que, al corregir por probar muchas cosas, deja de ser estadísticamente sólida.",
        "Se repite el cálculo cambiando algo cada vez: sacando provincias, sacando extremos, mezclando al azar, mirando sectores "
        "que no deberían verse afectados (prueba placebo: si también dieran efecto, el resultado sería sospechoso) y viendo si el daño crece "
        "donde el campo pesa más (dosis-respuesta: si el clima realmente causa el daño, debería pegar más donde el sector expuesto pesa más).",
    )
    tarjetas([
        dict(etiqueta="Pruebas que pasa", valor=f"{n_pasa} de {n_eval}", unidad="dieron lo esperado si el efecto es real",
             desc="En los placebos, lo esperado es que no haya efecto.",
             ayuda="\"Pasa\" significa que el resultado fue el esperado si el efecto es real. \"Justo\" (p entre 0,05 y 0,10) no se cuenta como pasada."),
        dict(etiqueta="Azar iguala el efecto", valor="6 de 2.000", unidad="mezclas al azar",
             desc=f"p = {num(rb('4.')['p_valor'], 4)}: 0,35 chances en 100 de que sea casualidad.", ayuda=ayuda("p_valor")),
        dict(etiqueta="Dosis-respuesta", valor="p < 0,001", unidad="el daño crece con el peso del campo",
             desc="Menos de 1 chance en 1.000 de que sea casualidad.",
             ayuda="Por cada punto más de peso del campo en la economía de una provincia, el calor frena a la economía total unos "
                   f"{num(abs(dosis['coeficiente']), 2)} puntos más por °C."),
    ])

    tabla = pd.DataFrame([{
        "Prueba": nombre, "Qué se hizo": que, "Efecto estimado": f"{fila_['coeficiente']:.2f} ({unidad})",
        "p": fila_["p_valor"], "Resultado": ver,
    } for fila_, nombre, que, esperado, unidad, ver in evaluadas])
    tabla_html(
        ["Prueba", "Qué se hizo", "Efecto estimado", "p (probabilidad de casualidad)", "Resultado"],
        [[r["Prueba"], r["Qué se hizo"], r["Efecto estimado"], num(r["p"], 4), r["Resultado"]] for _, r in tabla.iterrows()],
        anchos=[18, 38, 18, 13, 13], col_estado=4, col_num=(3,),
    )

    colores = {"Pasa": "#2e7d4f", "Justo": "#b8961e", "No pasa": "#c0392b", "Informativo": "#6b6b6b"}
    g = tabla.iloc[::-1]
    fig = go.Figure(go.Bar(
        x=g["p"].clip(lower=1e-6), y=g["Prueba"], orientation="h", marker_color=[colores[v] for v in g["Resultado"]],
        customdata=g[["Resultado"]], hovertemplate="%{y}<br>p = %{x:.4f}<br>%{customdata[0]}<extra></extra>",
    ))
    fig.add_vline(x=0.05, line_dash="dash", line_color="black", annotation_text="p = 0,05", annotation_position="top")
    fig.update_xaxes(type="log", title="p (escala logarítmica: cuanto más a la izquierda, menos probable que sea casualidad)")
    fig.update_layout(height=520, margin=dict(l=10))
    st.plotly_chart(fig, width="stretch")
    explicacion(
        "Cada barra es el p-valor (la probabilidad de que el resultado sea casualidad) de una prueba. La línea punteada es el 0,05. "
        "<strong>Para las pruebas de efecto, una barra a la izquierda de la línea es buena señal (verde)</strong>. "
        "<strong>Para los placebos es al revés</strong>: se espera que no haya efecto, así que a la derecha de la línea pasan. "
        "Escala logarítmica porque los valores van de 0,000001 a casi 1."
    )

    peor = rb("2. Sacar una provincia (peor")
    st.markdown("#### Qué se aprende de cada grupo de pruebas")
    st.markdown(
        f"""
- **La señal no depende de una sola provincia ni de valores extraños.** Sacando de a una provincia, la señal se mantiene en {rb('2. Sacar una provincia (cuántas')['detalle']} casos (p < 0,05: menos de 5 chances en 100 de casualidad); el peor (sin {peor['detalle'].replace('p más alto al sacar ', '')}) queda justo en el límite (p = {peor['p_valor']:.3f}). Sin valores extremos el efecto baja a {rb('3.')['coeficiente']:.1f} puntos por °C y sigue siendo significativo (es decir, con p menor a 0,05).
- **No es casualidad de mezclar datos** (prueba de permutación: se mezclan las temperaturas al azar y se cuenta cuántas veces el azar iguala el efecto real): de 2.000 mezclas, solo 6 lo igualaron.
- **Es específico del campo** (prueba placebo: repetir el cálculo en sectores que no deberían verse afectados): en construcción, comercio, transporte y finanzas no aparece efecto. Y sí aparece, más chico, en la industria de alimentos y bebidas, que procesa lo que produce el campo.
- **Pega más donde el campo pesa más** (dosis-respuesta: si el calor realmente causara el daño, tendría que crecer con el peso del sector expuesto): es la prueba más fuerte. Si el calor no tuviera nada que ver, no habría razón para que el daño creciera con el peso del campo.
- **Es un efecto del mismo año, no arrastrado** (efecto rezagado: ver si el clima de un año afecta a los siguientes): el calor del año anterior no frena la producción del siguiente (p = {rb('7.')['p_valor']:.2f}, o sea {chances(rb('7.')['p_valor'])} de casualidad).
- **Lo que la debilita:** al corregir por haber probado 6 combinaciones a la vez (corrección de Holm: endurece el criterio para compensar que, si se prueba mucho, alguna sale bien por suerte), el resultado del calor sobre el campo pasa a p = {p_holm:.2f} ({chances(p_holm)} de casualidad): deja de ser estadísticamente sólido. Y mirando solo los años muy cálidos queda justo (p = {rb('8.')['p_valor']:.3f}).
"""
    )
    explicacion(
        f"<strong>Conclusión del paso 6:</strong> la señal del calor sobre el campo es <strong>creíble pero no está probada</strong>. Sobrevive a casi todos los ataques "
        f"({n_pasa} de {n_eval}) y tiene la marca típica de un efecto real (crece con el peso del campo, no aparece en sectores sin relación). "
        "Pero con solo 19 años de datos y 24 provincias, al exigirle el criterio más duro (corregir por comparaciones múltiples) no alcanza. "
        "Para pasar de \"señal\" a \"demostrado\" hacen falta más años y datos por cultivo (ver PENDIENTES_PARA_DEMOSTRAR_MAS.md)."
    )

# ================================================================ VEREDICTO
with t_veredicto:
    st.subheader("Veredicto: ¿el cambio climático afecta a la economía argentina?")
    para_que("Resumir, sin maquillaje, qué quedó demostrado, qué es una señal y qué no se pudo detectar.")
    veredicto = pd.DataFrame(resumen, columns=["Pregunta", "Qué mostraron los datos (el paréntesis explica lo anterior)", "Nivel de evidencia"])
    tabla_html(
        ["Pregunta", "Qué mostraron los datos (el paréntesis explica lo anterior)", "Nivel de evidencia"],
        veredicto.values.tolist(), anchos=[22, 60, 18], col_estado=2,
    )

    st.markdown("### La respuesta")
    st.markdown(
        "**El cambio climático es real y medible en Argentina, y el calor reduce el rendimiento de los cultivos: cerca de un 11 % en el maíz, "
        "un 13 % en el trigo y un 9 % en la soja por cada grado más en la temporada.** "
        "En cambio, con los datos disponibles **no se puede demostrar que afecte al PBI total ni al PBI per cápita del país**: "
        "el golpe se diluye en una economía diversa donde el campo es una parte. Decirlo así es más fuerte, y más "
        "útil para decidir políticas, que afirmar algo que los números no sostienen."
    )
    st.markdown("### Por qué importa socialmente")
    st.markdown(
        """
- Un efecto chico en el promedio del país puede ser **muy grande para las familias y las comunidades** que dependen de una cosecha.
- Lo que se ve en el agregado nacional **no alcanza para tranquilizarse**: hay que mirar el sector y la región.
- Proteger la producción del interior (riego, seguros, financiamiento, adaptación) es **proteger el trabajo argentino**.
"""
    )
    st.markdown("### Límites de este análisis")
    st.markdown(
        """
- Solo hay **19 años** de datos económicos provinciales por sector (2005-2023): poco tiempo para eventos extremos.
- La lluvia y la temperatura provinciales son **estimaciones satelitales** (NASA POWER), no mediciones de una estación en cada provincia.
- Se probaron 6 combinaciones (2 resultados × 3 factores): con tantas pruebas, un resultado aislado puede salir significativo por azar. Por eso el calor sobre el campo se califica como **señal moderada** y no como prueba.
- El **PBI per cápita provincial no se pudo calcular**: no hay población por provincia en las fuentes usadas.
"""
    )
    st.markdown("### Qué haría falta para demostrar más")
    st.markdown(
        """
- Población por provincia (Censo/INDEC) para medir el **PBI per cápita provincial**.
- Datos de **empleo y exportaciones agropecuarias**, para ver el efecto sobre el trabajo y no solo sobre la producción.
- Registro de **eventos extremos** (inundaciones, sequías declaradas como emergencia agropecuaria) en lugar de solo la lluvia anual.
- Series más largas y por **cultivo** (soja, maíz, trigo), donde el efecto del clima es más directo.
"""
    )
