# Resumen de funcionamiento del proyecto

Registro cronológico de qué se construyó, qué decisiones se tomaron (y
por qué), y qué problemas reales aparecieron y cómo se resolvieron.

**Nota sobre esta versión:** el proyecto se reconstruyó completo en una
segunda pasada (misma metodología y fuentes ya validadas en la primera
construcción). Los resultados numéricos coinciden exactamente con la
primera corrida (verificado), lo cual confirma que el pipeline es
reproducible de punta a punta.

## Etapas 1-2 — Inspección y estructura

Entorno revisado (Python 3.13, dependencias del stack recomendado).
Estructura creada según `proyecto.txt` sección 11: `data/`, `notebooks/`,
`src/` (13 módulos), `outputs/`, `main.py`, `requirements.txt`.

## Etapa 3 — Fuentes de datos

13 fuentes reales, verificadas por acceso directo (no solo enlaces de
búsqueda), documentadas en `data/sources.csv` con todos los campos de
la sección 4. Problemas reales resueltos en el camino:
- `smn.gob.ar` bloquea accesos automatizados (403) → se usó CIAM
  (`ciam.ambiente.gob.ar`), que republica los mismos datos del SMN.
- OWID no tiene a Argentina en su grapher de temperatura por país → se
  adoptó NASA POWER (reanálisis, documentado como tal).
- INDEC discontinuó el PBG provincial en 2017 (motivo real investigado:
  falta de Censo Económico actualizado + decisiones provinciales
  independientes) → se adoptó la actualización de CEPAL (2004-2024).
- Inventario de GEI: 2022 es el último año publicado, rezago
  estructural de 2-3 años en este tipo de reportes a nivel mundial.

Decisiones del usuario: temperatura provincial = NASA POWER (documentada
la limitación metodológica); emisiones_co2 principal = GEI oficial
(CO2 equivalente), con OWID como serie alternativa para el modelo.

## Etapa 4 — Construcción del dataset

`src/descarga_datos.py` + `src/construir_dataset.py`. Datasets:
`dataset_nacional.csv` (65 filas, 1961-2025), `dataset_provincial.csv`
(1080 filas, 24 jurisdicciones, 1981-2025). Validado: 0 jurisdicciones
inválidas, 0 duplicados, CABA diferenciada de Pcia. Buenos Aires, sin
multiplicación de filas en merges.

Bugs reales corregidos: hoja incorrecta del Excel de GEI (el archivo
"emisiones" es nacional 1990-2022, no tiene desagregación provincial;
esa está en "desagregacion-provincial", 2010-2022); años "2023 (2)" /
"2024 (2)" de CEPAL venían como texto y se perdían silenciosamente;
NASA POWER usa -999.0 como código de dato faltante.

## Etapas 5-6 — Análisis exploratorio

Nacional: 5 gráficos (sección 15) + estadística descriptiva + tendencias.
Tendencia de temperatura: +0.0135°C/año (p<0.001). Provincial: evolución
por provincia + ranking de tendencias. CABA con mayor calentamiento
(+0.032°C/año, p<0.001) — consistente con efecto de isla de calor urbana.

## Etapa 7 — Relación clima-economía

Correlaciones Pearson/Spearman, nacional y provincial (24 pruebas
independientes, nunca mezcladas). Ninguna correlación nacional
significativa. De 96 pruebas provinciales, solo 1 con p<0.05 — menos
de lo esperable por azar, no se interpreta como hallazgo real.

## Etapa 8 — Modelos predictivos

Regresión lineal (statsmodels OLS, con IC/p-valores) + Random Forest,
nacional (división 1961-2009/2010-2024) y provincial conjunto (pooled,
dummies por provincia, división 2010-2018/2019-2022).

Decisión de datos: CO2 para el modelo nacional = serie OWID (64 años),
no la oficial de GEI (13 años, insuficiente para dividir train/test).

Resultado honesto: R² negativo en los tres modelos (LR nacional: -0.75;
RF nacional: -1.59; RF provincial: -0.01) — ninguno predice mejor que
el promedio histórico. No se construyeron modelos individuales por
provincia (máximo 13 años de datos superpuestos).

## Etapa 9 — Escenarios de proyección futura

No se usaron los modelos multivariados (ya probados poco confiables)
para proyectar, evitando además inventar valores futuros de
precipitación/CO2/PBI. Se usó extrapolación de tendencia simple:
- Escenario A (tendencia histórica completa): +0.66°C en 2050 (p<0.001).
- Escenario C (últimos 15 años): +1.10°C en 2050 (pendiente NO
  significativa, p=0.11 — reportado igual, con esa advertencia).
- Escenario B (IPCC AR5, Barros et al. 2014, cita externa): +1.0 a
  +3.5°C hacia fin de siglo XXI, según escenario de emisiones.

Problemas reales de acceso a fuentes: IPCC/CCKP devolvieron 403; un PDF
de la Tercera Comunicación Nacional superó el límite de tamaño; otro
PDF (CONICET) no tenía texto extraíble y no había poppler para
renderizarlo. Se resolvió con una fuente secundaria confiable
(Wikipedia, citando textualmente a Barros et al. 2014).

## Etapa 10 — Conclusiones

`CONCLUSIONES.md`, separado en las 6 categorías de la sección 36, cada
afirmación trazable a un archivo concreto de `outputs/`.

## Etapa 11 — Mapas coropléticos

`geopandas` instalado sin problemas (wheels de `pyogrio`, sin compilar
GDAL). Geometría: shapefile oficial del IGN, encontrado tras varios
callejones sin salida (búsquedas genéricas sin resultado, un endpoint
con 404, un `package_show` de datos.gob.ar con error 502) hasta dar con
la URL real vía `package_search` y la documentación de `georef-ar-api`.

Bug de diseño corregido: el polígono de Tierra del Fuego incluye el
sector antártico reclamado por Argentina, que dominaba el mapa; se
recortó el encuadre visual (no el dato) al territorio continental +
Tierra del Fuego. 3 mapas generados, geográficamente coherentes con el
clima real de Argentina (Misiones la más lluviosa, Cuyo la más seca).

Se agregó `descargar_geometria_ign()` a `src/descarga_datos.py` para que
la descarga de la geometría también sea reproducible desde cero (antes
se había bajado manualmente).

## Reconstrucción completa (esta versión)

El usuario movió la carpeta original a otra ubicación como resguardo y
pidió reconstruir el proyecto completo desde `proyecto.txt` en esta
ubicación, sin quitar nada, como base para un front-end nuevo (Streamlit,
carpeta separada, sin tocar este proyecto). Se recrearon los 13 módulos
de `src/`, `data/sources.csv`, y se corrió el pipeline completo de
punta a punta: los 9 pasos terminaron sin errores y los resultados
numéricos coinciden exactamente con la corrida original.

## Etapa 12 — Front-end en Streamlit (proyecto separado)

**Qué se hizo:** se construyó `argentina-clima-front/`, carpeta hermana
e independiente (no depende de este proyecto en tiempo de ejecución:
lee una copia propia de los resultados en su carpeta `data_front/`).
No se modificó ni un archivo de `argentina-clima-pbi/` para esto.

**Contenido:** app multipágina (`st.navigation`) con 12 páginas —
Inicio (dashboard con KPIs), Fuentes de datos, Construcción del
dataset, Análisis nacional, Análisis provincial, Mapas, Clima y
economía, Modelos predictivos, Escenarios futuros, Explorador
interactivo, Conclusiones, y un Checklist de las 40 secciones de
`proyecto.txt` (honesto: marca la sección 17 —regiones NOA/NEA/Cuyo—
como pendiente, no implementada en ningún momento del proyecto).

Cada página muestra los gráficos PNG originales de `outputs/figures/`
**más** gráficos interactivos nuevos (Plotly), generados en vivo a
partir de los mismos CSV ya validados: mapa de calor provincia×año,
boxplots por década, comparador multi-provincia, mapa coroplético
interactivo, ficha por provincia, ranking interactivo, medias móviles.

**Guía de referencia usada:** se cargó la skill `developing-with-streamlit`;
como el script `discover.py` fallaba (buscaba el intérprete `python3`,
inexistente en esta máquina Windows, solo `python`), se localizó
manualmente el `SKILL.md` versionado dentro del propio paquete instalado
(`site-packages/streamlit/.agents/skills/...`) y se leyeron las
referencias de `multipage-apps`, `dashboards`, `design` y
`code-organization` antes de escribir código.

**Verificación real:** las 12 páginas + el punto de entrada se corrieron
con `streamlit.testing.v1.AppTest` (testing headless oficial de
Streamlit, sin necesitar navegador) — cero excepciones. Además se
levantó el servidor real (`python -m streamlit run streamlit_app.py`)
y se confirmó HTTP 200 y `/_stcore/health` = `ok` antes de darlo por
terminado.

**Nota:** este resumen (`RESUMEN_FUNCIONAMIENTO.md`) y `CONCLUSIONES.md`
de este proyecto se copiaron tal cual a `argentina-clima-front/data_front/`
y se muestran íntegros en la página "Conclusiones" del front — cualquier
actualización futura de estos documentos requiere copiarlos de nuevo
(ver `argentina-clima-front/README.md`, sección "Actualizar los datos").

## Etapa 13 — Rehacer "Clima y economía", per cápita y sequía

**Motivo:** la página "Clima y economía" original solo mostraba tablas de
correlación crudas (96 pruebas con muy poca potencia estadística cada
una) sin traducirlas a una historia; el modelo predictivo predecía
temperatura usando la economía como insumo, al revés de la pregunta del
proyecto; y faltaban dos variables centrales pedidas por el usuario: PBI
**per cápita** y años de **sequía** como categoría (no como mm continuos).

**Clima-economía (nuevo enfoque):** `src/analisis_clima_economia_provincial.py`
cruza la tendencia de precipitación de cada provincia (2010-2024) contra
el crecimiento de su PBG (CAGR 2004-2024) — una sola prueba con n=24
provincias, mucho más potente que las 96 pruebas dentro de cada
provincia. Resultado honesto: r=-0.19, p=0.37, no significativa.

**Modelos predictivos (variable objetivo invertida):** `modelo_nacional.py`
y `modelo_provincial.py` pasaron a predecir crecimiento económico (PBI /
variación del PBG) a partir del clima, no al revés. Hallazgo real: a
nivel nacional la regresión lineal predice mejor que el promedio
histórico (R²=0.21, la anomalía de precipitación es la variable más
importante); a nivel provincial sigue sin haber poder predictivo (R²=-0.10).

**PBI per cápita nacional:** el dataset `owid_co2_data_argentina.csv`
(ya descargado para CO2) trae columnas `population` y `gdp` (Maddison
Project Database) sin usar. Se agregó `cargar_poblacion_pbi_percapita_nacional()`
a `construir_dataset.py`: PBI per cápita = gdp / population, 1961-2022 (62
años). No hay población provincial en ninguna fuente, así que per cápita
queda solo a nivel nacional.

**Indicador de sequía:** `src/analisis_sequia_economia.py`, nuevo. "Año
seco" = percentil 25 más bajo de precipitación de la propia serie
histórica (nacional: toda la serie 1961-2025; provincial: la propia
historia de cada provincia 1981-2025, no un umbral fijo en mm, porque lo
seco en Misiones es normal en Santa Cruz). Prueba t comparando el
crecimiento económico entre años secos y normales. A nivel provincial,
como cada provincia por separado tiene muy pocos años de PBG, se agrupan
las 24 en un panel comparando cada año contra el promedio histórico de
esa misma provincia (para no confundir "provincia seca" con "provincia
pobre"). Resultado honesto: ninguna diferencia significativa, ni nacional
(p=0.94 PBI, p=0.97 PBI per cápita) ni provincial (p=0.60).

**Front-end:** además de las páginas actualizadas, se agregó:
- Un glosario (`utils/ui.py`) con tooltips nativos de Streamlit
  (parámetro `help=`) y `<abbr title="...">` para términos técnicos
  (R², MAE, p-valor, Pearson/Spearman, PBI per cápita, año seco, etc.).
- Un acordeón "¿Qué es esta página?" al tope de las 12 páginas.
- Reemplazo de los bloques de color (`st.info`/`success`/`warning`/`error`)
  usados como explicación por texto en cursiva y color, sin fondo — los
  bloques de color quedaron reservados para alertas reales.
- Explicación ("por qué este gráfico y no otro") debajo de cada gráfico.
- La página "Fuentes de datos" pasó de una tabla que truncaba texto
  largo con "..." a una ficha desplegable por fuente.
- Conclusiones: hoja tipo A4 (estilo informe) + botón de descarga en PDF
  (`utils/pdf.py`, con `fpdf2` + `markdown`, fuente DejaVu Sans embebida
  en `assets/fonts/` para tildes/°/²/₂/em-dash — las fuentes core de PDF
  no las soportan). Bug real de fpdf2 2.8.x encontrado y evitado: llamar
  `multi_cell`/`write_html` dos veces seguidas con texto acentuado tira
  `FPDFException: Not enough horizontal space` — se resolvió armando
  todo el HTML del informe y renderizándolo en un solo `write_html()`.

**Verificación:** las 12 páginas se corrieron con `AppTest` después de
cada cambio (cero excepciones) y el servidor real se levantó varias
veces (`HTTP 200`, `/_stcore/health` = `ok`).
