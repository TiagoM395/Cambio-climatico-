"""Portada: presentación institucional del proyecto en 6 tarjetas de igual tamaño."""

import itertools

import streamlit as st
from scipy import stats

from utils.datos import cargar_dataset_nacional, cargar_tabla
from utils.ui import num

CSS = """
<style>
.block-container { padding: 10px !important; max-width: 100% !important; }
header[data-testid="stHeader"] { background: transparent; }

.card {
    box-sizing: border-box; height: calc(100vh - 20px); margin: 0 0 10px 0; overflow: hidden;
    border-radius: 24px; background: var(--bg); color: #fff;
    font-family: "Segoe UI", Inter, system-ui, sans-serif;
}

/* ---------- Card 1: institucional ---------- */
.card.inst {
    padding: 7vh 5rem; display: flex; flex-direction: column; justify-content: space-between;
    font-family: Georgia, "Times New Roman", serif; color: #f4f1ea;
}
.inst .institucion { font-size: clamp(1.3rem, 4vh, 2rem); font-weight: 700; letter-spacing: .3em; text-transform: uppercase; }
.inst .carrera { font-size: clamp(.95rem, 2.5vh, 1.25rem); margin-top: 1.2vh; opacity: .85; letter-spacing: .03em; }
.inst .filete { width: 120px; height: 3px; background: var(--acento); margin-top: 3vh; }
.inst .tp { font-family: "Segoe UI", system-ui, sans-serif; font-size: clamp(.7rem, 1.8vh, .9rem); font-weight: 700; letter-spacing: .3em; text-transform: uppercase; color: var(--acento); margin-bottom: 2.5vh; }
.inst h1 { color: #f4f1ea; font-family: Georgia, "Times New Roman", serif; font-size: clamp(1.9rem, 7.5vh, 3.9rem); line-height: 1.12; font-weight: 700; margin: 0; padding: 0; max-width: 62rem; }
.inst .ficha { display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr 1.2fr; gap: 2rem; border-top: 1px solid rgba(244,241,234,.3); padding-top: 3vh; }
.inst .ficha small { display: block; font-family: "Segoe UI", system-ui, sans-serif; font-size: clamp(.6rem, 1.5vh, .75rem); letter-spacing: .2em; text-transform: uppercase; color: var(--acento); font-weight: 700; margin-bottom: 1vh; }
.inst .ficha b { font-size: clamp(.9rem, 2.3vh, 1.2rem); font-weight: 600; line-height: 1.3; }

/* ---------- Cards 2-6: etapas ---------- */
.card.etapa { display: grid; grid-template-columns: 36% 64%; }
.etapa .izq { padding: 7vh 3.5rem; display: flex; flex-direction: column; justify-content: space-between; }
.etapa .num { font-size: clamp(4rem, 22vh, 10rem); font-weight: 800; line-height: .9; color: var(--acento); letter-spacing: -.04em; }
.etapa .fase { font-size: clamp(.7rem, 1.8vh, .9rem); font-weight: 700; letter-spacing: .26em; text-transform: uppercase; color: var(--acento); margin-bottom: 1.5vh; }
.etapa h2 { color: #fff; font-size: clamp(1.5rem, 5.2vh, 2.7rem); line-height: 1.12; font-weight: 800; letter-spacing: -.015em; margin: 0; padding: 0; }
.etapa .der { margin: 2.2vh 2.2vh 2.2vh 0; border-radius: 18px; background: rgba(255,255,255,.1); padding: 5vh 3rem; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: 1fr; gap: 4vh 3rem; align-content: center; }
.etapa .bloque { border-top: 3px solid var(--acento); padding-top: 1.8vh; }
.etapa .bloque h3 { color: #fff; font-size: clamp(.95rem, 2.5vh, 1.25rem); font-weight: 700; margin: 0 0 1vh 0; padding: 0; }
.etapa .bloque p { font-size: clamp(.82rem, 2.05vh, 1.05rem); line-height: 1.5; margin: 0; opacity: .92; }
.etapa .bloque .cifra { font-size: clamp(1.6rem, 5vh, 2.6rem); font-weight: 800; color: var(--acento); line-height: 1; margin-bottom: 1vh; }

/* ---------- Card de datasets (tabla) ---------- */
.etapa .der.tabla { display: block; padding: 3.5vh 2.5rem; }
.tabla table { width: 100%; border-collapse: collapse; }
.tabla th { text-align: left; font-size: clamp(.6rem, 1.5vh, .75rem); letter-spacing: .16em; text-transform: uppercase; color: var(--acento); font-weight: 700; padding: 0 .6rem 1vh .6rem; border: none; border-bottom: 2px solid var(--acento); background: transparent; }
.tabla td { font-size: clamp(.72rem, 1.85vh, .95rem); padding: .85vh .6rem; border: none; border-bottom: 1px solid rgba(255,255,255,.16); color: #fff; vertical-align: middle; line-height: 1.25; }
.tabla td.n, .tabla th.n { text-align: right; white-space: nowrap; }
.tabla td.n { font-weight: 800; font-variant-numeric: tabular-nums; color: var(--acento); font-size: clamp(.8rem, 2vh, 1.05rem); }
.tabla td small { display: block; opacity: .7; font-size: .8em; }
.tabla tr.int td { border-bottom: none; padding-top: 1.6vh; font-weight: 700; }

@media (max-width: 900px) {
    .card { height: auto; }
    .card.inst { padding: 2.5rem 1.5rem; gap: 2rem; }
    .inst .ficha { grid-template-columns: 1fr 1fr; }
    .card.etapa { grid-template-columns: 1fr; }
    .etapa .izq { padding: 2rem 1.5rem; gap: 1rem; }
    .etapa .der { margin: 0 10px 10px 10px; grid-template-columns: 1fr; padding: 1.5rem; }
}
</style>
"""


def card_institucional():
    st.markdown(
        """
<div class="card inst" style="--bg:#0d1b2a;--acento:#c9a24b">
<div>
<div class="institucion">Instituto 57</div>
<div class="carrera">Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial</div>
<div class="filete"></div>
</div>
<div>
<div class="tp">Trabajo Práctico Integrador</div>
<h1>Cambio climático en Argentina y su relación con el crecimiento económico (PBI)</h1>
</div>
<div class="ficha">
<div><small>Materia</small><b>Análisis y Exploración de Datos</b></div>
<div><small>Autor</small><b>Elías Campos</b></div>
<div><small>Docente</small><b>Ibarra Martín</b></div>
<div><small>Comisión</small><b>2.º año · Grupo 6</b></div>
<div><small>Fecha de entrega</small><b>30 de noviembre de 2026</b></div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def card_etapa(bg, acento, numero, fase, titulo, bloques):
    """bloques: lista de (encabezado, texto) o (cifra, encabezado, texto)."""
    html = ""
    for b in bloques:
        if len(b) == 3:
            html += f'<div class="bloque"><div class="cifra">{b[0]}</div><h3>{b[1]}</h3><p>{b[2]}</p></div>'
        else:
            html += f'<div class="bloque"><h3>{b[0]}</h3><p>{b[1]}</p></div>'
    st.markdown(
        f'<div class="card etapa" style="--bg:{bg};--acento:{acento}">'
        f'<div class="izq"><div class="num">{numero}</div>'
        f'<div><div class="fase">{fase}</div><h2>{titulo}</h2></div></div>'
        f'<div class="der">{html}</div></div>',
        unsafe_allow_html=True,
    )


def card_datasets(bg, acento, numero, fase, titulo, conteo):
    fmt = lambda n: f"{int(n):,}".replace(",", ".")
    filas = ""
    for r in conteo[conteo["tipo"] == "descargado"].itertuples():
        filas += (f"<tr><td>{r.dataset}<small>{r.fuente} · {r.unidad}</small></td>"
                  f"<td>{r.periodo}</td><td class='n'>{fmt(r.filas)}</td></tr>")
    total = int(conteo.loc[conteo["tipo"] == "descargado", "filas"].sum())
    filas += (f"<tr class='int'><td>Total de registros descargados</td><td></td>"
              f"<td class='n'>{fmt(total)}</td></tr>")
    st.markdown(
        f'<div class="card etapa" style="--bg:{bg};--acento:{acento}">'
        f'<div class="izq"><div class="num">{numero}</div>'
        f'<div><div class="fase">{fase}</div><h2>{titulo}</h2></div></div>'
        f'<div class="der tabla"><table><tr><th>Dataset descargado</th><th>Período</th><th class="n">Filas</th></tr>{filas}</table></div></div>',
        unsafe_allow_html=True,
    )


st.markdown(CSS, unsafe_allow_html=True)
conteo = cargar_tabla("conteo_datasets.csv")

nacional = cargar_dataset_nacional()
tend = cargar_tabla("tendencias_nacional.csv").set_index("variable")
cobertura = cargar_tabla("informe_cobertura.csv")
pendiente = tend.loc["anomalia_temperatura"]["pendiente"]
p_tendencia = tend.loc["anomalia_temperatura"]["p_valor"]
anom_max = nacional["anomalia_temperatura"].max()
anio_max = int(nacional.loc[nacional["anomalia_temperatura"].idxmax(), "año"])
serie_temp = nacional["año"][nacional["anomalia_temperatura"].notna()]
temp_desde, temp_hasta = int(serie_temp.min()), int(serie_temp.max())

# Correlaciones de Pearson entre las cuatro variables del dataset nacional (años con las cuatro completas)
VARIABLES = {
    "temperatura": "anomalia_temperatura", "precipitación": "anomalia_precipitacion_pct",
    "CO₂": "emisiones_co2_fosil", "PBI": "pbi_crecimiento_pct",
}
_completo = nacional[list(VARIABLES.values())].dropna()
_años = nacional.loc[_completo.index, "año"]
conj_desde, conj_hasta = int(_años.min()), int(_años.max())
pares = []
for (na, ca), (nb, cb) in itertools.combinations(VARIABLES.items(), 2):
    r_, p_ = stats.pearsonr(_completo[ca], _completo[cb])
    pares.append((na, nb, r_, p_))
significativos = [q for q in pares if q[3] < 0.05]
pbi_significativos = [q for q in significativos if "PBI" in (q[0], q[1])]

n_duplicados = int(nacional.duplicated(["año"]).sum())
gei = cobertura[(cobertura["dataset"] == "nacional") & (cobertura["variable"] == "emisiones_gei_co2eq")].iloc[0]
AÑO_CORTE_MODELO = 2009  # corte cronológico de src/modelo_nacional.py (AÑO_CORTE)

if len(significativos) == 1:
    q = significativos[0]
    bloque_corr = (f"r = {num(q[2], 2)}", f"{q[0].capitalize()} y {q[1]}",
                   "Única asociación significativa entre las variables del dataset nacional.")
else:
    bloque_corr = (f"{len(significativos)} de {len(pares)}", "Asociaciones significativas",
                   "Cantidad de pares de variables del dataset nacional con correlación significativa (p menor a 0,05).")
if pbi_significativos:
    bloque_pbi = ("PBI", "Relación con el clima",
                  "El crecimiento económico muestra al menos una relación lineal significativa con otra variable. Ver la página Clima y economía.")
else:
    bloque_pbi = ("PBI", "Relación débil",
                  "El crecimiento económico no muestra una relación lineal significativa con el clima. Se informa tal cual.")
texto_tendencia = ("Calentamiento sostenido y estadísticamente significativo" if p_tendencia < 0.05 else "Tendencia no significativa")

card_institucional()

card_etapa(
    "#1b3f8b", "#9cc0ff", "01", "Fase 1 · Comprensión del problema",
    "Planteo del problema y objetivos",
    [
        ("Contexto", "Argentina busca crecer económicamente en el marco del Acuerdo de París y su Contribución Determinada a Nivel Nacional (NDC)."),
        ("Pregunta central", "¿Cómo se relacionan el PBI, las emisiones de CO₂ y las precipitaciones con la anomalía de temperatura, y es posible predecirla?"),
        ("Objetivo general", f"Analizar la evolución histórica de tres indicadores climáticos entre {conj_desde} y {conj_hasta} y su relación con el crecimiento del PBI."),
        ("Alcance", "Argentina a nivel nacional, las 23 provincias y la Ciudad Autónoma de Buenos Aires. Sin otros países como observaciones."),
    ],
)

card_datasets(
    "#0b5d57", "#8be8d8", "02", "Fase 2 · Comprensión de los datos",
    "Datasets descargados de fuentes oficiales", conteo,
)

card_etapa(
    "#9a4210", "#ffc590", "03", "Fase 3 · Preparación de los datos",
    "Preparación de los datos descargados",
    [
        ("Selección", "Se descartó la serie oficial de emisiones de GEI por cubrir solo 2010-2022 y se documentó la decisión."),
        ("Integración", "Los archivos descargados se unen por año y por provincia. No se genera ni se completa ningún dato: si una fuente no cubre un año, queda vacío."),
        ("Variable económica", "Se usa la tasa de crecimiento del PBI y no su nivel, para evitar correlaciones espurias entre series que solo crecen con el tiempo."),
        ("Validación", f"{'Sin años duplicados' if n_duplicados == 0 else str(n_duplicados) + ' años duplicados'}. Los años sin dato quedan vacíos: las emisiones oficiales de GEI tienen {int(gei['observaciones'])} años ({int(gei['primer_año'])}-{int(gei['ultimo_año'])}). Partición temporal: entrenamiento {conj_desde}-{AÑO_CORTE_MODELO} y prueba {AÑO_CORTE_MODELO + 1}-{conj_hasta}."),
    ],
)

card_etapa(
    "#5a2a83", "#dcb8ff", "04", "Fase 4 · Modelado",
    "Análisis exploratorio y modelado",
    [
        ("Exploración", "Evolución de cada variable, pruebas de tendencia y correlaciones de Pearson entre las variables del dataset nacional."),
        ("Modelos", "Regresión Lineal y Random Forest, evaluados con partición cronológica (nunca aleatoria) y comparados contra el promedio histórico."),
        ("Territorio", "Ranking de calentamiento, mapas y análisis por jurisdicción para las 24 provincias."),
        ("Escenarios", "Proyección de la temperatura futura con tres escenarios: continuidad de la tendencia, referencia IPCC y aceleración reciente."),
    ],
)

card_etapa(
    "#8f1d33", "#ffb8c6", "05", "Fase 5 · Evaluación",
    "Resultados y conclusiones",
    [
        (f"+{pendiente:.4f} °C".replace(".", ","), "Tendencia por año", f"{texto_tendencia} entre {temp_desde} y {temp_hasta}."),
        (f"+{num(anom_max, 2)} °C", f"Anomalía máxima ({anio_max})", "Mayor desvío respecto de la base 1991-2020 de toda la serie."),
        bloque_corr,
        bloque_pbi,
    ],
)
