"""Checklist honesto de las 40 secciones de proyecto.txt: qué se cumplió, qué quedó parcial."""

import pandas as pd
import streamlit as st

from utils.ui import acordeon_pagina

st.header(":material/checklist: Checklist del proyecto original")
acordeon_pagina("checklist")
st.caption(
    "Mapeo sección por sección de `proyecto.txt` (documento de especificación "
    "original) contra lo efectivamente construido. Reportado con honestidad: "
    "lo parcial se marca como parcial, no se infla el cumplimiento."
)

FILAS = [
    (1, "Objetivo general", "✅ Completo", "Todo el proyecto"),
    (2, "Objetivos específicos", "✅ Completo", "Conclusiones"),
    (3, "Jurisdicciones (23 prov. + CABA)", "✅ Completo", "Datos descargados"),
    (4, "Fuentes de datos documentadas", "✅ Completo", "Fuentes de datos (13 fuentes)"),
    (5, "Regla geográfica (solo Argentina)", "✅ Completo", "Datos descargados"),
    (6, "Variables principales", "✅ Completo", "Datos descargados"),
    (7, "PBI y PBG (crecimiento real, no nominal)", "✅ Completo", "Análisis nacional / provincial"),
    (8, "Temperatura (anomalía, período base)", "✅ Completo", "Análisis nacional / provincial"),
    (9, "Precipitaciones", "✅ Completo", "Análisis provincial"),
    (10, "Emisiones de CO2 (diferenciar metodologías)", "✅ Completo", "Fuentes de datos, Análisis nacional"),
    (11, "Estructura del proyecto", "✅ Completo", "Proyecto argentina-clima-pbi"),
    (12, "Tecnologías (Python, stack recomendado)", "✅ Completo", "requirements.txt"),
    (13, "Flujo de trabajo incremental por etapas", "✅ Completo", "RESUMEN_FUNCIONAMIENTO.md"),
    (14, "Validación de datos (duplicados, merges)", "✅ Completo", "Datos descargados"),
    (15, "Análisis exploratorio nacional", "✅ Completo", "Análisis nacional"),
    (16, "Análisis provincial + mapas", "✅ Completo", "Análisis provincial, Mapas"),
    (17, "Regiones argentinas (NOA/NEA/Cuyo/...)", "✗ Pendiente", "No se agregó una columna de región secundaria"),
    (18, "Estadística descriptiva", "✅ Completo", "Análisis nacional / provincial"),
    (19, "Tendencias temporales", "✅ Completo", "Análisis nacional / provincial"),
    (20, "Relación clima-economía", "✅ Completo", "Clima y economía"),
    (21, "No afirmar causalidad", "✅ Completo", "Aplicado en todas las páginas"),
    (22, "Modelo predictivo (lineal + Random Forest)", "✅ Completo", "Modelos predictivos"),
    (23, "Variables predictoras (codificación adecuada)", "✅ Completo", "Modelos predictivos"),
    (24, "División cronológica (no aleatoria)", "✅ Completo", "Modelos predictivos"),
    (25, "Métricas (MAE, RMSE, R²), transparencia", "✅ Completo", "Modelos predictivos"),
    (26, "Validación (overfitting, residuos, importancia)", "✅ Completo", "Modelos predictivos"),
    (27, "Predicción futura con escenarios explícitos", "✅ Completo", "Escenarios futuros"),
    (28, "Modelo nacional y provincial", "✅ Completo", "Modelos predictivos"),
    (29, "Comparación territorial (descriptiva)", "✅ Completo", "Análisis provincial, Explorador"),
    (30, "Visualizaciones (título/ejes/unidades/fuente)", "✅ Completo", "Todas las páginas de gráficos"),
    (31, "README", "✅ Completo", "argentina-clima-pbi/README.md"),
    (32, "Reproducibilidad (sin valores a mano)", "✅ Completo", "COMO_EJECUTAR.md, verificado end-to-end"),
    (33, "Manejo de datos faltantes", "⚠️ Parcial", "No se imputó nada (regla cumplida), pero no se hizo un análisis formal del patrón de faltantes"),
    (34, "Control de calidad geográfico (CABA vs. PBA)", "✅ Completo", "Datos descargados"),
    (35, "Control de calidad temporal", "✅ Completo", "Datos descargados"),
    (36, "Conclusiones separadas por categoría", "✅ Completo", "Conclusiones"),
    (37, "25 reglas fundamentales", "✅ Completo", "Aplicadas transversalmente"),
    (38, "Forma de trabajo (ejecutar, comprobar, documentar)", "✅ Completo", "RESUMEN_FUNCIONAMIENTO.md"),
    (39, "Idioma (todo en español)", "✅ Completo", "Todo el proyecto"),
    (40, "Resultado final esperado", "✅ Completo", "Conclusiones"),
]

df = pd.DataFrame(FILAS, columns=["Sección", "Tema", "Estado", "Dónde"])

completos = (df["Estado"] == "✅ Completo").sum()
parciales = (df["Estado"] == "⚠️ Parcial").sum()
pendientes = (df["Estado"] == "✗ Pendiente").sum()

with st.container(horizontal=True, gap="medium"):
    st.metric("Completas", completos, border=True)
    st.metric("Parciales", parciales, border=True, delta_color="off")
    st.metric("Pendientes", pendientes, border=True, delta_color="inverse" if pendientes else "off")

st.dataframe(df, hide_index=True, width="stretch", height=600)

st.caption(
    "La sección 17 (regiones argentinas como NOA/NEA/Cuyo/Pampeana/Patagonia) "
    "es la única marcada pendiente: el proyecto original la pide como "
    "agrupación secundaria opcional, nunca como reemplazo de la provincia — "
    "se puede agregar fácilmente si hace falta, sumando una columna `region` "
    "al dataset provincial."
)
