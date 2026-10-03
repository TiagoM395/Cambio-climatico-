# Ayudamemoria completo del proyecto

**Estado documentado:** 25 de septiembre de 2026, después de revertir la reorganización numerada del menú.
**Para qué sirve este documento:** describir con todo detalle lo que existe hoy (datos, análisis, aplicación, diseño, reglas), de modo que quien lo lea pueda **reconstruir exactamente el mismo trabajo desde cero**, o volver a este punto si un cambio posterior no gusta.
**Respaldo físico:** `_RESPALDO/respaldo_2026-09-25_estado_actual.zip` (incluye este documento; sin `.venv` ni `__pycache__`). Para volver atrás: descomprimir ese archivo sobre esta carpeta.

> **Cómo usar este documento con Claude:** entregarlo completo y pedir "armá exactamente lo que describe este ayudamemoria". Las secciones 15 y 16 dan el orden de reconstrucción y las decisiones abiertas.

---

## 1. Qué es el proyecto

| Dato                      | Valor                                                                                                                                               |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Título                   | Cambio climático en Argentina y su relación con el crecimiento económico (PBI)                                                                   |
| Autor                     | Elías Campos, Tiago Maidana                                                                                                                        |
| Institución              | Instituto 57 · Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial                                                                  |
| Materia                   | Análisis y Exploración de Datos                                                                                                                   |
| Docente                   | Ibarra Martín                                                                                                                                      |
| Comisión                 | 2.º año, grupo 6                                                                                                                                  |
| Fecha de inicio / entrega | 14/09/2026 / 30/11/2026 (11 semanas)                                                                                                                |
| Documentos de la cátedra | `Trabajo_Integrador_Cambio_Climatico_Argentina_CORREGIDO.docx` y `Plan_de_Proyecto_Cambio_Climatico_Argentina_CORREGIDO.docx` (no se modifican) |
| Especificación original  | `proyecto.txt` (40 secciones): **fuente de verdad, nunca se edita**                                                                         |
| Preguntas de origen       | `ver.txt` (10 preguntas y las 3 elegidas como eje)                                                                                                |

**Pregunta central que el usuario debe poder responder siempre:** ¿el cambio climático afecta a la economía argentina? (relación clima ↔ PBI per cápita de Argentina, a nivel país y por provincia).

**Respuesta actual (resumen honesto):**

- Demostrado: Argentina se calienta (+0,13 °C por década; 0,86 °C en 64 años).
- Demostrado (con una salvedad): el calor de la temporada de cultivo reduce el rendimiento: maíz −11,3 %, trigo −13,2 %, soja −8,8 % por cada °C; girasol sin efecto detectable. La soja es menos firme porque falla una prueba placebo.
- Señal moderada: el calor frena el valor de la producción agropecuaria (−5,6 puntos por °C, p = 0,026), que deja de ser significativo al corregir por comparaciones múltiples (Holm, p = 0,16).
- No detectado: efecto sobre la economía total de las provincias ni sobre el PBI per cápita del país (r = −0,12, p = 0,35).

---

## 2. Reglas y condiciones que el usuario impuso (obligatorias)

### 2.1 Reglas de contenido y datos

1. **Solo Argentina** (23 provincias + CABA = 24 jurisdicciones + agregado nacional). Los datos multipaís se filtran a Argentina.
2. **Todos los datos se descargan de fuentes oficiales.** Nunca se construyen, generan, estiman a mano ni rellenan. No se imputan faltantes: la celda queda vacía. Nunca decir "construcción del dataset": decir "datos descargados" que solo se **unen** por año y provincia.
3. Cada fuente se documenta (nombre, URL, institución, variable, unidad, cobertura, metodología, limitaciones). Cada vez que se hable de un dataset debe verse **su cantidad de filas**.
4. **No afirmar causalidad.** Se habla de asociación estadística. Un resultado nulo ("no se detecta") es válido y se informa igual; no se fuerza ninguna conclusión.
5. Se usa la **tasa de crecimiento** del PBI/PBG, no el nivel (evita correlaciones falsas entre series que solo crecen con el tiempo).
6. **Partición cronológica** (nunca aleatoria) en los modelos; provincia codificada con variables dummy; el modelo predice la **economía a partir del clima**, no al revés (decisión explícita del usuario).
7. Todo en **español**. Reproducible: ningún valor, coeficiente o métrica escrito a mano; todo sale de tablas generadas por scripts.
8. Honestidad ante todo: si algo no se demostró, se dice; si una prueba de control falla (placebo de la soja), se dice.

### 2.2 Reglas de redacción (ordenadas por el usuario en esta etapa)

1. El usuario **no es técnico**: todo debe entenderlo cualquiera, pero con nivel profesional.
2. **El término técnico y la fórmula se quedan**, y su significado va **entre paréntesis en el mismo texto** (ejemplo: "+0,13 °C por década ≈ 0,86 °C en 64 años, p < 0,001 (la temperatura sube unos 0,13 grados cada 10 años…; ≈ es aproximadamente; la p es la probabilidad de casualidad…)"). **Nunca** una versión "más fácil" aparte, ni códigos de referencia tipo [G11], ni "Dato técnico:" sueltos.
3. Cada respuesta de resumen empieza con **una respuesta directa en palabras** ("Sí, sube un…", "No, no se ve relación…", "Posiblemente, pero no está confirmado…") y después la cifra con su paréntesis.
4. **Los datos no van dentro de líneas de texto corrido**: van en tarjetas o tablas. Un texto de lectura no lleva cifras salvo lo imprescindible.
5. Formato argentino: **coma decimal** y signo menos verdadero (−). Ejemplo: "−11,3 %".
6. Un solo glosario, al final de Conclusiones (y su PDF). En las páginas, los términos se explican con globo al pasar el mouse (`termino()`) y entre paréntesis.
7. **Cada gráfico** lleva: un título/pregunta clara y una explicación breve de qué muestra y por qué ese tipo de gráfico (dicha en forma natural; nunca "este gráfico responde…"). Las siglas (GEI, MtCO₂eq, PBI) deben tener referencia.
8. **No usar bloques de color para texto explicativo** ni conclusiones: se escriben en cursiva y color (`explicacion()`); `st.info/success/warning/error` quedan reservados para alertas reales.
9. **No repetir contenido** en distintas páginas y **no poner enlaces entre páginas** (`st.page_link`, "ver la página X").
10. **No usar la numeración "5.1, 5.2…"** (fases CRISP-DM numeradas) en ningún lugar de la app: el usuario la rechazó explícitamente.
11. Mantener actualizados README y guías cada vez que cambia algo (el usuario se traba si quedan desactualizados). Comandos de consola siempre en **una sola línea** encadenada con `;` (PowerShell 5.1 no acepta `&&`) y con rutas absolutas.

### 2.3 Reglas de diseño (ver detalle en la sección 9)

- Tarjetas **siempre del mismo tamaño** dentro de una fila (y homogéneas en toda la app); sin texto cortado.
- **Sin scroll** en tablas de pocas filas; **sin scroll horizontal** en pestañas; tablas con texto largo se dibujan con texto que baja de línea.
- Tipografía única, escala corta, sin saltos grandes de tamaño; nada "grande y apretado".
- Portada: 6 tarjetas del alto de la ventana menos 10 px, esquinas redondeadas, **colores lisos (nunca degradados)**, tipografía en `vh` para que entre en una notebook.
- Las tarjetas del estilo "Calentamiento / Rendimiento / Economía total / PBI per cápita" son el estándar visual aprobado por el usuario.

### 2.4 Reglas que entraron en conflicto (decidir antes de seguir)

- Regla antigua: "nunca sacar texto, solo agregar". Regla nueva: "no repetir cosas". Prevalece la nueva cuando el usuario pide quitar algo explícitamente.
- Explicación de cada gráfico "dentro de un recuadro": se aplicó solo en los cuatro gráficos originales de Análisis nacional (título, imagen y explicación dentro del mismo contenedor con borde). En el resto de las páginas la explicación sigue debajo del gráfico, en cursiva. **Pendiente confirmar** si se generaliza.

---

## 3. Estructura de carpetas

```
cambio cllimatico/                       (carpeta de trabajo; ojo: el nombre lleva doble "l")
├── proyecto.txt                         especificación original (NO editar)
├── ver.txt                              preguntas de origen
├── Plan_de_Proyecto_..._CORREGIDO.docx  plan de la cátedra (NO editar)
├── Trabajo_Integrador_..._CORREGIDO.docx
├── _plan_nuevo.txt, _trabajo_nuevo.txt  textos auxiliares
├── COMO_LEVANTAR_EL_PROYECTO.md         guía para abrir la app (usuario no técnico)
├── LA_PREGUNTA_Y_LA_RESPUESTA.md        informe de la respuesta a la pregunta central
├── PENDIENTES_PARA_DEMOSTRAR_MAS.md     preguntas sin responder, objeciones, cómo reforzar
├── VERIFICACION_DE_DATASETS.md          dirección de cada fuente + huella SHA-256 de cada archivo
├── AYUDAMEMORIA_COMPLETO.md             este documento
├── _RESPALDO/                           respaldo comprimido del estado actual
├── argentina-clima-pbi/                 BACKEND: análisis (Python, datos, resultados)
└── argentina-clima-front/               FRONT: app Streamlit (solo lee resultados copiados)
```

**El entorno virtual NO está en esta carpeta** (ver 4.3 y 4.4): vive en
`C:\Users\tiago\.venvs\clima`.

### 3.1 Backend `argentina-clima-pbi/`

```
data/raw/           archivos descargados tal cual (13 fuentes; ver sección 5)
data/processed/     dataset_nacional.csv (65×11), dataset_provincial.csv (1.080×9),
                    provincias_clima_anual.csv, provincias_tendencia.csv
data/sources.csv    documentación de las 13 fuentes (con columnas por_que, para_que, conteo_claves)
src/                21 módulos Python más __init__.py (sección 6)
outputs/figures/    21 PNG
outputs/tables/     34 CSV
outputs/models/     modelo_lineal_nacional_ols.pickle, modelo_rf_nacional.joblib, modelo_rf_provincial_conjunto.joblib
notebooks/          analisis_argentina.ipynb
main.py, requirements.txt
README.md, COMO_EJECUTAR.md, CONCLUSIONES.md, RESUMEN_FUNCIONAMIENTO.md
```

### 3.2 Front `argentina-clima-front/`

```
streamlit_app.py        punto de entrada (configuración, estilos, navegación)
app_pages/              13 páginas (sección 8)
utils/datos.py          carga de datos (todo desde data_front/)
utils/ui.py             glosario, ayudas, componentes de diseño, CSS (sección 9)
utils/pdf.py            Conclusiones → PDF A4 (fpdf2 + fuente DejaVu)
assets/fonts/           DejaVuSans.ttf, -Bold, -Oblique (necesarias para tildes, °, ², ₂ y guion largo en el PDF)
data_front/             COPIA de los resultados del backend (la app nunca recalcula):
                        figures/ (21 PNG), tables/ (32 CSV), processed/ (2 CSV), geo/ (shapefile IGN),
                        sources.csv, CONCLUSIONES.md, RESUMEN_FUNCIONAMIENTO.md
requirements.txt, README.md, COMO_EJECUTAR.md
```

**Regla de sincronización:** al volver a correr un script del backend, copiar sus salidas a `data_front/` (`tables/*.csv`, `figures/*.png`, `processed/*.csv`, `sources.csv`, `CONCLUSIONES.md`). Hoy `data_front/tables` no tiene `rendimiento_panel.csv` ni `sequia_panel_provincial.csv` porque la app no los usa.

---

## 4. Entorno y ejecución

### 4.1 Versiones

Python 3.14.4 · Streamlit 1.57.0 · Plotly 6.7.0 · pandas 2.3.1 · geopandas 1.1.4 · shapely 2.1.2 · Windows 11, PowerShell 5.1 como terminal principal.

> La versión original del proyecto usaba Python 3.13.3. Se migró a 3.14.4 al mudarlo a esta computadora: el `.venv` que venía copiado apuntaba a `C:\Python313` (de la máquina de Elías) y no arrancaba. Todos los paquetes instalan sin compilar en 3.14.

### 4.2 Dependencias

- **Backend** (`argentina-clima-pbi/requirements.txt`): pandas 2.3.1, numpy 2.3.2, matplotlib 3.10.3, seaborn 0.13.2, scipy 1.17.1, scikit-learn 1.8.0, statsmodels 0.15.0, geopandas 1.1.4, pyogrio 0.13.0, pyproj 3.8.0, shapely 2.1.2, plotly 6.7.0, jupyter, openpyxl 3.1.5, requests 2.33.1, joblib, xlrd 2.0.2 (para leer el `.xls` del INDEC).
- **Front** (`argentina-clima-front/requirements.txt`): streamlit 1.57.0, pandas 2.3.1, plotly 6.7.0, geopandas 1.1.4, pyogrio 0.13.0, pyproj 3.8.0, shapely 2.1.2, fpdf2 2.8.8, markdown 3.10.3, scipy 1.18.1 y statsmodels 0.15.0 (estas dos se agregaron el 25/09: la Portada usa scipy y las rectas de tendencia de Plotly usan statsmodels; antes faltaban en el archivo).
- El backend **no tiene entorno propio**: sus scripts se ejecutan con el mismo Python del front (`C:\Users\tiago\.venvs\clima`), que además tiene statsmodels, scikit-learn, scipy, matplotlib, openpyxl y xlrd instalados.

### 4.3 Abrir la aplicación (una sola línea)

```powershell
cd "C:\Trabajo base cambio climatico\argentina-clima-front"; C:\Users\tiago\.venvs\clima\Scripts\python.exe -m streamlit run streamlit_app.py
```

Se abre en `http://localhost:8501`.

### 4.4 Tropiezos conocidos

- **El entorno virtual tiene que estar en una ruta CORTA, fuera de la carpeta del proyecto.** Cuando el proyecto estaba en la carpeta larga de OneDrive (~190 caracteres), con el entorno adentro la carpeta `shapely` quedaba en 241 y al cargar la DLL se pasaba del límite de 260 de Windows: `ImportError: DLL load failed while importing lib: El nombre del archivo o la extensión es demasiado largo.` Por eso vive en `C:\Users\tiago\.venvs\clima` (regla invertida respecto de la versión anterior de este documento, que pedía que estuviera dentro de `argentina-clima-front`). La carpeta del proyecto después se mudó a `C:\Trabajo base cambio climatico`, pero el entorno **no** se movió: sigue en `C:\Users\tiago\.venvs\clima` y hay que actualizar el `cd` de los documentos si cambia la ruta otra vez.
- **No hay que usar `activate`**: se llama directo a `C:\Users\tiago\.venvs\clima\Scripts\python.exe`. El `cd` a la carpeta del front sigue siendo obligatorio (Streamlit resuelve `app_pages/` y `data_front/` desde el directorio del script).
- Los archivos `.py` de `app_pages/` y `utils/` están en **CRLF** (Windows). Al editarlos por script, abrir en modo texto de Windows o en binario; un reemplazo mal hecho puede dejar un `SyntaxError`.
- La consola de Windows usa cp1252: al imprimir `→`, `₂`, etc. hay `UnicodeEncodeError`; los scripts nuevos hacen `sys.stdout.reconfigure(encoding="utf-8")`.
- `smn.gob.ar` bloquea descargas automáticas (403): se usa CIAM, que republica lo mismo. El portal de datos abiertos del Ministerio de Economía exige cabecera `User-Agent` de navegador.

### 4.5 Reproducir el backend (desde `argentina-clima-pbi`, con el Python de `C:\Users\tiago\.venvs\clima`)

Orden (`python -m src.<módulo>`):

1. `descarga_datos` · 2. `construir_dataset` · 3. `analisis_nacional` · 4. `analisis_provincial` · 5. `analisis_correlacion` · 6. `modelo_nacional` · 7. `modelo_provincial` · 8. `escenarios_proyeccion` · 9. `mapas` · 10. `analisis_clima_economia_provincial` · 11. `analisis_sequia_economia` · 12. `conteo_datasets` · 13. `analisis_impacto_agropecuario` · 14. `analisis_robustez` (~20 s) · 15. `analisis_rendimiento_cultivos` (~2 min) · 16. `verificar_datasets` (después del 12).
   Luego copiar las salidas a `argentina-clima-front/data_front/`.

---

## 5. Datos: las 13 fuentes

Todas se descargan con `src/descarga_datos.py` y se guardan sin transformar en `data/raw/`. La cantidad de filas sale de `outputs/tables/conteo_datasets.csv`; las direcciones y huellas, de `VERIFICACION_DE_DATASETS.md`.

| #  | Dataset                                                       | Institución                         | Período                                            | Filas                       | Archivo local                                                                          | Para qué se usa                                           |
| -- | ------------------------------------------------------------- | ------------------------------------ | --------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| 1  | Anomalía de temperatura y precipitación nacional            | CIAM / SMN (Secretaría de Ambiente) | 1961-2025                                           | 65 años                    | `ciam_anomalia_temp_precip_nacional.csv`                                             | Clima nacional de todos los análisis                      |
| 2  | Precipitación anual por estación                            | CIAM / SMN                           | 2010-2024                                           | 26 estaciones               | `ciam_precipitacion_estaciones.csv`                                                  | Lluvia provincial medida en tierra                         |
| 3  | Inventario Nacional de GEI, serie por gas y sector            | Secretaría de Ambiente              | 1990-2022                                           | 7.780                       | `inventario-nacional-gei-emisiones_hasta_2022.xlsx`                                  | Emisiones del país (solo 13 años comparables: 2010-2022) |
| 4  | Inventario de GEI desagregado por provincia                   | Secretaría de Ambiente              | 2010-2022                                           | 876 (26 hojas)              | `desagregacion-provincial_hasta_2022.xlsx`                                           | Emisiones por provincia                                    |
| 5  | CO₂, población y PBI (Global Carbon Project vía OWID)      | Our World in Data                    | 1850-2024                                           | 175 (de 50.411 del mundial) | `owid_co2_data_argentina.csv` (+ `owid_co2_data_mundial.csv`)                      | CO₂ fósil en los modelos; población                     |
| 6  | Crecimiento anual del PBI                                     | Banco Mundial                        | 1960-2025                                           | 66                          | `banco_mundial_pbi_crecimiento.csv`                                                  | Variable económica nacional                               |
| 7  | PBG provincial por sector                                     | CEPAL                                | 2004-2024                                           | 1.350 (25 hojas)            | `cepal_pbg_provincial.xlsx`                                                          | Economía provincial y del campo                           |
| 8  | PIB provincial oficial (discontinuado 2017)                   | INDEC                                | —                                                  | no se descargó             | —                                                                                     | Solo se cita como referencia                               |
| 9  | Temperatura y lluvia (NASA POWER)                             | NASA                                 | anual 1981-2025 (1.080); mensual 1981-2023 (12.384) | 1.080 y 12.384              | `nasa_power_temperatura_provincial.csv`, `nasa_power_clima_mensual_provincial.csv` | Clima provincial; punto por provincia = su capital         |
| 10 | Límites de provincias                                        | IGN                                  | —                                                  | 24 polígonos               | `geo_ign_provincias/` (8 archivos)                                                   | Mapas                                                      |
| 11 | Población y PBI (Maddison, mismas columnas del OWID)         | Maddison Project vía OWID           | 1961-2022 (PBI)                                     | (en el archivo 5)           | (en el archivo 5)                                                                      | PBI per cápita nacional                                   |
| 12 | Estimaciones agrícolas por cultivo, provincia y departamento | Ministerio de Economía, Agricultura | 1969-2024 (campañas 1969/70 a 2024/25)             | 160.499                     | `magyp_estimaciones_agricolas.csv` (15,5 MB)                                         | Rendimiento por cultivo                                    |
| 13 | Población por provincia (proyecciones INDEC)                 | INDEC                                | 2010-2040                                           | 744 (24 hojas)              | `indec_poblacion_provincial_2010_2040.xls`                                           | **Descargada y verificada, todavía sin usar**       |

Direcciones exactas (fuente 12: `https://datos.magyp.gob.ar/dataset/9e1e77ba-267e-4eaa-a59f-3296e86b5f36/resource/95d066e6-8a0f-4a80-b59d-6f28f88eacd5/download/estimaciones-agricolas.csv`, estable por identificador de recurso; fuente 13: `https://www.indec.gob.ar/ftp/cuadros/poblacion/c1_proyecciones_prov_2010_2040.xls`; resto en `VERIFICACION_DE_DATASETS.md`).

### 5.1 Tablas de trabajo (solo unión por año/provincia)

- **`dataset_nacional.csv`** (65 filas, 1961-2025): `año, jurisdiccion, tipo_jurisdiccion, anomalia_temperatura, anomalia_precipitacion_pct, emisiones_gei_co2eq, emisiones_co2_fosil, pbi_crecimiento_pct, poblacion, pib_per_capita, pib_per_capita_crecimiento_pct`.
- **`dataset_provincial.csv`** (1.080 filas, 24 jurisdicciones, 1981-2025): `año, jurisdiccion, tipo_jurisdiccion, temperatura_media_c, anomalia_temperatura, precipitaciones_mm, emisiones_gei_co2eq, pbg, pbg_preliminar`.
- Cobertura real (`informe_cobertura.csv`): temperatura y lluvia nacional 65 años; emisiones GEI **13 años (2010-2022)**; CO₂ fósil 64; PBI 65; población 64; PBI per cápita 62 (1961-2022).
- El PBI per cápita solo existe a nivel país: **no hay población provincial usada** (la fuente 13 está descargada pero sin analizar).
- Problemas resueltos al leer archivos: hoja de GEI en otro archivo; años "2023 (2)" y "2024 (2)" de CEPAL venían como texto; NASA usa −999,0 para faltantes (se filtra).

### 5.2 Verificación para el docente

`python -m src.verificar_datasets` genera `VERIFICACION_DE_DATASETS.md` y `outputs/tables/verificacion_datasets.csv` con: dataset, institución, dirección exacta, archivo, filas, tamaño, fecha de descarga y huella SHA-256 de cada archivo de `data/raw/`.

---

## 6. Backend: qué hace cada script

| Módulo                                                                           | Qué hace                                                                                                                                                                                                                                                                 | Salidas principales                                                                                                        |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `data_loader`, `preprocessing`, `analysis`, `modeling`, `visualization` | Utilidades: carga sin inventar datos, validación de jurisdicciones, estadística descriptiva y tendencias, división cronológica y modelos, gráficos con título/unidades/fuente                                                                                       | —                                                                                                                         |
| `descarga_datos`                                                                | Descarga las fuentes a`data/raw/`; si una falla, informa y **no inventa reemplazo**                                                                                                                                                                               | `data/raw/*`                                                                                                             |
| `construir_dataset`                                                             | Une por año/provincia, sin imputar                                                                                                                                                                                                                                       | `data/processed/*`                                                                                                       |
| `conteo_datasets`                                                               | Cuenta filas reales de cada archivo                                                                                                                                                                                                                                       | `conteo_datasets.csv`                                                                                                    |
| `analisis_nacional`                                                             | Estadística descriptiva y tendencia (regresión lineal año → variable) nacional                                                                                                                                                                                        | `tendencias_nacional.csv`, `estadistica_descriptiva_nacional.csv`, 5 PNG                                               |
| `analisis_provincial`                                                           | Ídem por provincia + ranking de calentamiento                                                                                                                                                                                                                            | `tendencias_temperatura_provincial.csv`, PNG                                                                             |
| `analisis_correlacion`                                                          | 96 pruebas dentro de cada provincia + 4 nacionales (Pearson y Spearman)                                                                                                                                                                                                   | `correlaciones_*.csv`                                                                                                    |
| `analisis_clima_economia_provincial`                                            | Una sola prueba con n = 24: tendencia de lluvia por década vs. crecimiento del PBG                                                                                                                                                                                       | `ranking_precipitacion_crecimiento_pbg_provincial.csv`, PNG                                                              |
| `analisis_sequia_economia`                                                      | "Año seco" = 25 % con menos lluvia (nacional 1961-2025; provincial contra la propia historia) y prueba t                                                                                                                                                                 | `sequia_vs_crecimiento_*.csv`, PNG                                                                                       |
| `modelo_nacional`                                                               | Predice`pbi_crecimiento_pct` con año, anomalía de lluvia, anomalía de temperatura y CO₂ fósil; regresión lineal (statsmodels OLS) y Random Forest (300 árboles, profundidad 4, semilla 42); corte cronológico en 2009; validación cruzada temporal de 5 cortes | `modelo_nacional_comparacion_metricas.csv`, importancias, coeficientes, modelos, PNG                                     |
| `modelo_provincial`                                                             | Modelo conjunto de las 24 provincias (dummies) que predice`pbg_crecimiento_pct`; Random Forest (300, profundidad 5); corte 2018; sin modelos individuales (máx. 13 años por provincia)                                                                                | `modelo_provincial_metricas.csv`, importancias, predicciones                                                             |
| `escenarios_proyeccion`                                                         | Extrapolación lineal de la temperatura: A (toda la historia), C (últimos 15 años), y B (IPCC AR5, cita externa)                                                                                                                                                        | `escenario_a_...`, `escenario_c_...`, `escenarios_proyeccion_b_ipcc.csv`                                             |
| `mapas`                                                                         | Mapas coropléticos con geometría del IGN                                                                                                                                                                                                                                | 3 PNG                                                                                                                      |
| `analisis_impacto_agropecuario`                                                 | Panel 24 provincias × 19 años (2005-2023, 456 obs): crecimiento agro y total vs. calor/seco/lluvia; regresión con efectos fijos de provincia y año, errores agrupados por provincia                                                                                   | `impacto_agro_*.csv`, `impacto_nacional_percapita.csv`                                                                 |
| `analisis_robustez`                                                             | 12 pruebas duras sobre la señal del calor en el campo (sección 7.6)                                                                                                                                                                                                     | `robustez_resultados.csv`                                                                                                |
| `analisis_rendimiento_cultivos`                                                 | Rendimiento (kg/ha) de soja, maíz, trigo y girasol vs. clima de la temporada de cultivo (sección 7.7)                                                                                                                                                                   | `rendimiento_resultados.csv`, `rendimiento_por_provincia.csv`, `rendimiento_nacional.csv`, `rendimiento_panel.csv` |
| `verificar_datasets`                                                            | Guía de verificación con huellas                                                                                                                                                                                                                                        | `VERIFICACION_DE_DATASETS.md`                                                                                            |

Definiciones fijas: **año base de anomalía** = 1991-2020; "año seco" = 25 % inferior de la propia serie de lluvia; efectos fijos = provincia y año.

---

## 7. Resultados verificados (todos salen de tablas)

### 7.1 Tendencias nacionales (`tendencias_nacional.csv`)

- Temperatura: **+0,0135 °C/año** (R² 0,44; p = 1,5·10⁻⁹); 2023 fue el año más cálido (+0,83 °C sobre 1991-2020).
- Precipitación: sin tendencia (p = 0,91). GEI (13 obs): p = 0,24. PBI: p = 0,41, oscila entre −10,9 % y +10,6 %.

### 7.2 Provincial

- Mayor calentamiento significativo: CABA (+0,032 °C/año), Misiones (+0,019), Corrientes y Chaco (+0,015), Buenos Aires (+0,014). Ranking descriptivo, sin juicio de valor.
- Provincia por provincia (n = 24): correlación lluvia-crecimiento del PBG r = −0,19 (p = 0,37).
- 96 pruebas dentro de cada provincia: solo 1 con p < 0,05 (Formosa), menos de lo esperable por azar.

### 7.3 Años de sequía

- Nacional: 17 años secos y 48 normales; PBI 2,23 % vs 2,35 % (p = 0,94); PBI per cápita 1,31 % vs 1,37 % (p = 0,97).
- Provincial (panel de 24, contra la propia historia): −0,36 puntos (p = 0,60).

### 7.4 Modelos (predicen crecimiento económico)

- Nacional (train 1961-2009, test 2010-2024): regresión lineal MAE 3,80, RMSE 4,66, **R² 0,21**; Random Forest MAE 4,86, RMSE 5,57, **R² −0,13**. Importancia RF: precipitación 58 %, año 16 %, temperatura 16 %, CO₂ 10 %. Ningún coeficiente lineal es significativo.
- Provincial conjunto (corte 2018): MAE 7,39, RMSE 8,66, **R² −0,10** (sin poder predictivo; domina "año").

### 7.5 Escenarios de temperatura

- A (1961-2025, p < 0,001): +0,66 °C en 2050 (IC 95 %: +0,04 a +1,28). C (2011-2025, p = 0,11, no significativa): +1,10 °C (IC 95 %: +0,03 a +2,18). B (IPCC AR5, Barros et al. 2014): +1,0 a +2,0 °C nacional RCP4.5; hasta +3,5 °C en el NOA con RCP8.5, a fin de siglo. Solo se cita.

### 7.6 Impacto en el campo (panel 456 obs.)

| Resultado                       | Calor (+1 °C)                               | Año seco         |
| ------------------------------- | -------------------------------------------- | ----------------- |
| Producción agropecuaria        | −5,64 puntos, p = 0,026 (IC −10,6 a −0,7) | −2,98, p = 0,125 |
| Economía total de la provincia | −0,99, p = 0,174                            | −0,18, p = 0,767 |

- PBI per cápita nacional (62 años): temperatura r = −0,12 (p = 0,35), lluvia r = −0,14 (p = 0,27), CO₂ r = 0,02 (p = 0,86).
- Por provincia, en años secos el campo creció menos en 18 de 24 provincias (San Luis −26,6; San Juan −23,5; Córdoba −23,0 puntos). En el campo el peso medio en las 8 provincias más agropecuarias va del 4 % al 11 %.
- **Pruebas duras (`robustez_resultados.csv`) — pasa 8 de 12:** sacar una provincia (22 de 24 siguen significativas; peor caso sin Santiago del Estero p = 0,057); sin extremos −3,96 (p = 0,045); permutación (2.000 mezclas) el azar iguala 6 veces (p = 0,0035); placebo en construcción (p = 0,11), comercio (0,25), transporte (0,69) y finanzas (0,39) sin efecto; alimentos y bebidas −1,10 (p = 0,031); dosis-respuesta en la economía total −0,43 puntos por °C por cada punto de peso del campo (p < 0,001); año muy cálido −2,97 (p = 0,064); Spearman del ranking −0,35 (p = 0,093); efecto rezagado sin efecto (p = 0,79); **Corrección de Holm por las 6 pruebas originales: p = 0,155 (no pasa)**.

### 7.7 Rendimiento por cultivo (`rendimiento_resultados.csv`, 1.987 observaciones)

| Cultivo | Obs.  | Provincias         | % por °C                  | p       | Placebo (clima siguiente)      |
| ------- | ----- | ------------------ | -------------------------- | ------- | ------------------------------ |
| Maíz   | 625   | 15                 | −11,3 (IC −16,0 a −6,6) | < 0,001 | p = 0,24 (pasa)                |
| Soja    | 551   | 15                 | −8,8                      | 0,0002  | **p = 0,0047 (no pasa)** |
| Trigo   | 475   | 12                 | −13,2                     | 0,0006  | p = 0,14 (pasa)                |
| Girasol | 336   | 8                  | −1,3                      | 0,59    | p = 0,75                       |
| Todos   | 1.987 | (50 combinaciones) | −7,3 (IC −10,1 a −4,6)  | < 0,001 | p = 0,014                      |

- Método: clima de la **temporada de cultivo** (soja: nov-mar; maíz y girasol: oct-mar; trigo: jul-nov) de NASA POWER; rendimiento = producción / superficie cosechada (provincias con ≥ 2.000 ha y ≥ 15 años); logaritmo del rendimiento con efectos fijos de provincia y campaña; errores agrupados por provincia.
- Robustez: permutación (1.000 mezclas) p = 0,001; sacando de a una provincia sigue significativo (15/15 maíz, 15/15 soja, 12/12 trigo); con tendencia propia por provincia sigue significativo; el signo es negativo en 15/15 provincias de maíz, 14/15 de soja, 11/12 de trigo, 8/8 de girasol.
- **Nivel país** (42 campañas, con tendencia lineal, errores robustos HAC): trigo −7,3 % (p = 0,023) y girasol −10,1 % (p = 0,003) significativos; soja −7,1 % (p = 0,069) y maíz −8,5 % (p = 0,085) al borde. En orden de magnitud, sobre la producción reciente (promedio de las últimas 5 campañas): 1 °C más equivale a ~4,6 millones de t de maíz y ~3,1 de soja (producción reciente: maíz 54, soja 43, trigo 17, girasol 4 millones de t).
- Las temporadas se calentaron ~0,08 °C por década, por lo que el efecto acumulado ya medido ronda −0,6 % por década; el riesgo está en los años calurosos.

---

## 8. Aplicación Streamlit: navegación y páginas

### 8.1 `streamlit_app.py`

- `st.set_page_config(page_title="Clima y economía — Argentina", page_icon=":material/thermostat:", layout="wide")`, `inyectar_estilos()` y `st.navigation(..., position="sidebar")` con estos grupos (título de grupo → páginas):
  - *(sin título)*: **Inicio** (default, `:material/home:`), **Respuesta a la pregunta** (`:material/question_answer:`)
  - **El proyecto**: Fuentes de datos (`database`), Datos descargados (`table_chart`)
  - **Análisis**: Análisis nacional (`public`), Análisis provincial (`map`), Mapas (`travel_explore`), Clima y economía (`insights`)
  - **Modelos y proyecciones**: Modelos predictivos (`model_training`), Escenarios futuros (`timeline`)
  - **Explorar**: Explorador interactivo (`tune`)
  - **Cierre**: Conclusiones (`fact_check`), Checklist del proyecto (`checklist`)
- Barra lateral: leyenda "Datos reales, de fuentes oficiales, documentados en **Fuentes de datos**. Ningún valor es inventado."
- No hay `.streamlit/config.toml`: se usa el tema por defecto (claro/oscuro según el navegador). Todo el color propio funciona en ambos.
- Cada página (salvo Inicio) muestra arriba el acordeón "¿Qué es esta página?" (`acordeon_pagina(clave)`, textos en `PAGINAS` de `utils/ui.py`).

### 8.2 Páginas (contenido actual)

1. **Inicio (`inicio.py`)**: 6 tarjetas a pantalla completa (sección 9.6). Tarjeta 1 institucional (Instituto 57, Tecnicatura, TP Integrador, título, ficha con materia, autor, docente, comisión, entrega 30 de noviembre de 2026; sin chips de tecnologías). Tarjetas 2 a 6: fases con títulos formales ("Planteo del problema y objetivos", "Datasets descargados de fuentes oficiales" con tabla de cada dataset y total de registros, "Preparación de los datos descargados", "Análisis exploratorio y modelado", "Resultados y conclusiones"). Sus cifras y afirmaciones se **calculan solas** de los datos (tendencia, anomalía máxima, correlaciones de Pearson entre las cuatro variables con su significancia, años del período, partición temporal, cantidad de años de emisiones GEI). Solo quedan fijos: los datos institucionales, el contexto, la pregunta central del Trabajo Integrador original (predecir la temperatura) y el corte 2009 del modelo (`AÑO_CORTE` de `modelo_nacional.py`). Se corrigieron tres frases que no describían el trabajo real ("comparación entre dos mitades", "baseline ingenuo", "sin faltantes").
2. **Respuesta a la pregunta (`respuesta.py`)**: detalle en 8.3.
3. **Fuentes de datos (`fuentes.py`)**: aviso de 13 fuentes; tabla "Cantidad de filas de cada dataset descargado" sin scroll; ficha (contenedor con borde) por cada una de las 13 fuentes con cantidad de datos, período, alcance, frecuencia, por qué se usa, para qué sirve, qué mide y unidad, limitaciones y dirección; lista "Problemas reales resueltos durante la búsqueda".
4. **Datos descargados (`dataset.py`)**: explicación de la unión; tabla de filas por dataset; 3 tarjetas (nacional 65 filas, provincial 1.080, validaciones); pestañas Cobertura por variable (tabla + barras agrupadas), Vista previa nacional, Vista previa provincial (filtro de jurisdicción); problemas encontrados al leer archivos.
5. **Análisis nacional (`nacional.py`)**: 4 tarjetas de variables (con sigla y años con dato); tabla "Estadística descriptiva y tendencias"; "Gráficos originales del proyecto": cuatro PNG (temperatura, precipitación, emisiones GEI, PBI), cada uno con su explicación, fuente y cantidad de años dentro del mismo recuadro; PNG de tendencias normalizadas (z-score); "Gráficos adicionales interactivos": selector de variable (6), barras + media móvil de 5 años, boxplot por década, líneas z-score.
6. **Análisis provincial (`provincial.py`)**: PNG de temperatura y precipitación por provincia y del ranking; mapa de calor provincia × año de anomalía (escala RdBu_r centrada en 0); boxplot por provincia; dispersión precipitación media vs. tendencia; comparador (multiselect + control de variable) y tabla de ranking de calentamiento.
7. **Mapas (`mapas.py`)**: 3 PNG (tendencia de temperatura, anomalía media 2016-2025, precipitación media) y mapa coroplético interactivo con selector (tendencia de temperatura / precipitación media / PBG más reciente) sobre la geometría IGN.
8. **Clima y economía (`correlaciones.py`)**: barra horizontal lluvia vs. crecimiento del PBG (escala PuOr), 2 tarjetas (donde más baja la lluvia: Misiones; peor desempeño: Catamarca), explicación, PNG de dispersión, tabla del ranking; sección de sequía compacta (dos PNG lado a lado con leyenda y conclusión); expander con las 96 + 4 pruebas.
9. **Modelos predictivos (`modelos.py`)**: aclaración de que se predice una sola variable (crecimiento económico) y las demás son "pistas"; modelo nacional (explicación según R², barras de MAE/RMSE/R², PNG predicción vs. observado —el archivo se llama `prediccion_temperatura.png` pero muestra el PBI—, PNG de residuos, expanders con coeficientes e importancia); modelo provincial (3 tarjetas MAE/RMSE/R², PNG y expander de importancias) y nota de que no hay modelos individuales.
10. **Escenarios futuros (`escenarios.py`)**: PNG "original" y gráfico interactivo 2026-2050 con bandas de confianza; 3 tarjetas (A +0,66 °C, C +1,10 °C, B +1,0 a +3,5 °C); tabla del escenario B; leyenda que aclara que observado, A/C y B no se mezclan.
11. **Explorador interactivo (`explorador.py`)**: selector de provincia, ficha con 3 tarjetas (anomalía media, precipitación media, PBG más reciente), comparación contra el nacional y ranking interactivo.
12. **Conclusiones (`conclusiones.py`)**: hoja A4 (clase `.hoja-informe`, serif) con `CONCLUSIONES.md` + glosario único, y botón "Descargar como PDF" (`utils/pdf.py`).
13. **Checklist (`checklist.py`)**: tabla de las 40 secciones de `proyecto.txt` con estado y dónde se ve: **38 completas, 1 parcial (sección 33, faltantes) y 1 pendiente (sección 17, regiones NOA/NEA/Cuyo/Pampeana/Patagonia)**.

### 8.3 Respuesta a la pregunta (`respuesta.py`) en detalle

- **Encabezado:** etiqueta "RESPUESTA A LA PREGUNTA CENTRAL", título "¿El cambio climático afecta a la economía argentina?" y una oración sin cifras: "El clima de Argentina cambió con seguridad y el calor reduce el rendimiento de los cultivos. Ese efecto se diluye en el resto de la economía y no es detectable en el PBI total ni en el PBI per cápita del país."
- **4 tarjetas de indicador:** Calentamiento (+0,13 °C por década, con curva de la anomalía suavizada, "Demostrado"); Rendimiento (−7,3 % por °C, promedio de los cuatro cultivos, con rango probable, "Demostrado"); Economía total (−1,0 puntos por °C, rango cruza el cero, "No detectado"); PBI per cápita (r = −0,12, rango por transformación de Fisher, "No detectado").
- **"Detalle de cada resultado":** 7 desplegables (calentamiento, cultivos, valor del campo, años secos, economía total, PBI per cápita, pruebas duras) con el nivel de evidencia en color y el texto completo con paréntesis explicativos. Debajo, una línea en cursiva "Cómo leerlo". **Dentro del desplegable de años secos** (el 4.º) está el bloque "¿Y si lloviera más en una provincia concreta?": un `st.selectbox` con las 24 jurisdicciones (por defecto Córdoba) y 4 tarjetas calculadas —campo en años secos (puntos, con el estado según el signo: "Señal débil" si la pérdida va en el sentido esperado, "No detectado" si va al revés), economía total (puntos), correlación lluvia ↔ PBG dentro de la provincia (r, n y p, con el estado según p) y tendencia de la lluvia (**mm por década**, no %, período 2010-2024 que es la cobertura real de `precipitaciones_mm` en `dataset_provincial`, 360 provincia-años)—, más una `explicacion()` con dos salvedades: el dato es lluvia acumulada y no frecuencia, y las cifras por provincia son orientativas (2 a 8 años secos; panel de 24 provincias: −0,36 puntos, p = 0,60). Lee `impacto_agro_por_provincia.csv`, `correlaciones_provincial.csv`, `ranking_precipitacion_crecimiento_pbg_provincial.csv` y `sequia_vs_crecimiento_provincial.csv`; no recalcula nada.
- **8 pestañas** (sin íconos, para que entren en una fila): *La pregunta* · *1 · El clima* · *2 · La economía* · *3 · El campo* · *4 · Cultivos* · *5 · Dónde pega* · *6 · Pruebas* · *Veredicto*.
  - *La pregunta:* "¿El cambio climático le pega a la economía de los argentinos?", 3 paneles iguales (El trabajo, El interior productivo —cifras de las 8 provincias más agropecuarias—, La justicia entre regiones) y "Cómo se responde, en 6 pasos".
  - *1 · El clima:* tres tarjetas (por década, acumulado, ¿es casualidad?), barras anuales rojas/azules con línea de tendencia negra, barras horizontales por provincia (OrRd), conclusión.
  - *2 · La economía:* dispersión anomalía vs. crecimiento del PBI per cápita con recta, barras años secos vs. normales (naranja `#c8842b` y verde `#4a7c59`), tabla de correlaciones, párrafo del panel de 24 provincias, conclusión.
  - *3 · El campo:* 3 tarjetas "qué tengo / qué demuestro / cómo", gráfico de puntos con rangos de los 6 efectos (rojo = significativo, gris = no), 4 tarjetas, dispersión ajustada por efectos fijos, conclusión.
  - *4 · Cultivos:* 4 tarjetas (una por cultivo, con rango), gráfico de puntos por cultivo, gráfico por provincia en paneles (rojo `#c0392b` / gris `#b0b0b0`), gráfico nacional (rojo / naranja), 4 tarjetas de millones de toneladas, tabla de pruebas de control, conclusión.
  - *5 · Dónde pega:* barras por provincia de la diferencia de crecimiento del campo en años secos (color = peso del campo, YlOrBr), dispersión del efecto en la economía total vs. peso del campo, tabla.
  - *6 · Pruebas:* 3 tarjetas de resumen, tabla de las 13 pruebas (nombre, qué se hizo, efecto, p, Pasa/Justo/No pasa/Informativo), gráfico de p en escala logarítmica con línea en 0,05, viñetas de lo que se aprende, conclusión.
  - *Veredicto:* tabla con las mismas 7 respuestas del resumen, "La respuesta", "Por qué importa socialmente", "Límites de este análisis", "Qué haría falta para demostrar más".
- **Niveles de evidencia:** Demostrado (verde `#3fa66b`), Señal moderada / Señal débil (naranja `#d98b1f`), No detectado (gris `#8a8f98`). Se calculan en el código a partir de las tablas.

---

## 9. Sistema de diseño

### 9.1 Tipografía

Familia **Inter** (importada de Google Fonts) con respaldo Segoe UI / system-ui. Escala: `h2` 1,6 rem/700 · `h3` 1,2 rem/600 · `h4` 1,02 rem/600 · párrafo 0,95 rem con interlineado 1,65 · leyendas 0,82 rem · etiquetas en mayúsculas 0,70-0,74 rem con 0,05-0,09 em de espaciado · cifras de tarjeta 2,05 rem/600 con números tabulares · texto de explicación en cursiva 0,9 rem. La hoja de Conclusiones en pantalla usa Georgia (serif); el PDF descargable usa DejaVu Sans (fuentes incluidas en `assets/fonts/`).

### 9.2 Colores

- Estado: `#3fa66b` demostrado/pasa · `#d98b1f` señal/justo · `#8a8f98` no detectado/informativo · `#d0533f` no pasa.
- Datos en gráficos: rojo `#c0392b` (significativo, año cálido), azul `#2e6fa3` (año frío), gris `#8a8a8a` / `#b0b0b0` (no significativo), verde `#2e7d4f`, naranja `#d98b1f`, `#c8842b`, `#4a7c59`, `#b8961e`, `#6b6b6b`, sparklines `#5b8def` por defecto. Escalas Plotly: OrRd, RdBu_r, PuOr, YlOrBr, Blues, Reds, Greens.
- Texto explicativo: `#2f6690` (claro) y `#7fb2dd` (oscuro), cursiva.
- Bordes y fondos de tarjeta: `rgba(128,128,128,0.25)` y fondo `rgba(128,128,128,0.045)` (funciona en ambos temas).
- Portada (colores lisos, sin degradados): institucional fondo `#0d1b2a`, acento `#c9a24b`; etapas: `#1b3f8b`/`#9cc0ff`, `#0b5d57`/`#8be8d8`, `#9a4210`/`#ffc590`, `#5a2a83`/`#dcb8ff`, `#8f1d33`/`#ffb8c6`.

### 9.3 Componentes (en `utils/ui.py`)

| Función                                                                                     | Qué dibuja                                                                                                                                                                       | Regla                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tarjetas([...], minimo=230)`                                                              | Fila de tarjetas de indicador en grilla CSS (`auto-fit`, igual altura). Campos: `etiqueta, valor, u (unidad en la línea), unidad (subtítulo), grafico, desc, ayuda, estado` | Cifra en una sola línea; el estado va arriba a la derecha con punto de color y borde izquierdo de 3 px del mismo color; ayuda al pasar el mouse por toda la tarjeta; no usar`st.metric` para textos largos |
| `svg_linea(valores, color)`                                                                | Curva chica (sparkline) con área suave y último punto                                                                                                                           | Dentro de una tarjeta                                                                                                                                                                                         |
| `svg_rango(estimado, inf, sup, color)`                                                     | Punto + barra de rango probable + línea de cero punteada, con los extremos debajo                                                                                                | Si la barra toca el cero, el efecto no es firme                                                                                                                                                               |
| `claves(tengo, demuestro, como)`                                                           | Tres tarjetas de igual tamaño "Qué tengo / Qué demuestro / Cómo lo demuestro"                                                                                                 | Una por pestaña de análisis                                                                                                                                                                                 |
| `paneles([(titulo, texto)])`                                                               | Tarjetas de texto de igual altura                                                                                                                                                 | Sin íconos                                                                                                                                                                                                   |
| `tabla_html(encabezados, filas, anchos, col_estado, col_num)`                              | Tabla con texto que baja de línea, sin scroll, con columna de estado coloreada                                                                                                   | Para tablas con texto largo; para tablas de pocas filas con`st.dataframe` usar `height="content"`                                                                                                         |
| `explicacion(texto)`                                                                       | Párrafo en cursiva y color, sin fondo                                                                                                                                            | Reemplaza cajas de color                                                                                                                                                                                      |
| `termino(texto, clave)`                                                                    | Texto con subrayado punteado y globo (definición del`GLOSARIO`)                                                                                                                | Para siglas y términos técnicos                                                                                                                                                                             |
| `ayuda(clave)`, `para_que(texto)`, `acordeon_pagina(clave)`, `num(valor, decimales)` | Ayudas, línea "¿Para qué sirve?", acordeón "¿Qué es esta página?", formato con coma                                                                                        | —                                                                                                                                                                                                            |
| `tabla_legible`, `config_columnas`, `ETIQUETAS_VARIABLES`                              | Nombres de columnas en criollo con globo                                                                                                                                          | —                                                                                                                                                                                                            |
| `inyectar_estilos()`                                                                       | Inyecta todo el CSS (una sola vez, desde`streamlit_app.py`)                                                                                                                     | —                                                                                                                                                                                                            |
| `GLOSARIO`, `GLOSARIO_FINAL`, `glosario_markdown()`                                    | 72 definiciones (61 entran al glosario único del final)                                                                                                                          | Todo término nuevo se agrega a ambos                                                                                                                                                                         |

Clases CSS: `.kpi-grid/.kpi/.kpi-top/.kpi-etiqueta/.kpi-estado/.kpi-valor/.kpi-num/.kpi-u/.kpi-sub/.kpi-graf/.kpi-svg/.kpi-pie/.kpi-desc`, `.claves-grid/.clave`, `.paneles-grid/.panel-texto`, `.tabla-clima`, `.resp-eyebrow/.resp-titulo/.resp-lead`, `.explicacion-clima`, `.termino-clima`, `.hoja-informe`. Pestañas: `flex-wrap: wrap`, separación 0,2 × 1,4 rem, texto 0,92 rem sin saltos.

### 9.4 Patrones de página

- Título de sección → gráfico o tarjetas → explicación en cursiva (por qué ese tipo de gráfico y cómo leerlo). Un gráfico por pregunta.
- Cada gráfico lleva `st.plotly_chart(..., width="stretch")` o `st.image(..., width="stretch")` con título, ejes con unidades y fuente.
- Texto de resultado: respuesta directa + cifra + paréntesis; "chances en 100" para expresar p-valores (función `chances(p)`: 0,026 → "2,6 chances en 100"; menos de 0,001 → "menos de 1 chance en 1.000").

### 9.5 Cómo verificar el aspecto (sin abrir el navegador a mano)

Edge sin ventana: `msedge.exe --headless=new --hide-scrollbars --window-size=1500,1250 --virtual-time-budget=90000 --screenshot=<ruta>.png http://localhost:<puerto>/<pagina>`. Con ventanas muy altas la captura queda cargando; usar 1.250 px de alto. Las pestañas no se pueden abrir en captura: se prueban con una página de prueba o con `streamlit.testing.v1.AppTest`.

### 9.6 Portada (medidas)

Cada tarjeta: `height: calc(100vh - 20px)`, margen inferior 10 px, radio 24 px, texto en `vh`/`clamp()`; contenedor con `padding: 10px` y ancho máximo 100 %; las tarjetas de etapa son una grilla 36 % / 64 % (izquierda: número enorme + fase + título; derecha: bloques con borde superior del color de acento); la tarjeta de datasets muestra una tabla con total de registros.

---

## 10. Informes y guías (qué dice cada uno)

| Archivo                                                                                                     | Contenido                                                                                                                                                                                                                                                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LA_PREGUNTA_Y_LA_RESPUESTA.md`                                                                           | Respuesta en un minuto (7 respuestas con nivel), datos, los 6 pasos (clima, economía país, campo, cultivos, dónde pega, pruebas duras), límites, qué falta, cómo reproducir y glosario de referencia                                                                                                                                                                                               |
| `PENDIENTES_PARA_DEMOSTRAR_MAS.md`                                                                        | **Solo lo que falta** (actualizado el 25/09): agrupar gráficos y métricas según el Marco Metodológico CRISP-DM (sin numeración), revisiones visuales pendientes, preguntas originales sin responder, objeciones sin respuesta completa, refuerzos sin datos nuevos y datos nuevos a conseguir (uso de la población provincial, empleo/exportaciones, eventos extremos, ENSO, estaciones SMN) |
| `VERIFICACION_DE_DATASETS.md`                                                                             | Para el docente: dirección, archivo, filas, tamaño, fecha y SHA-256 de cada dataset                                                                                                                                                                                                                                                                                                                    |
| `COMO_LEVANTAR_EL_PROYECTO.md`                                                                            | Guía de una línea para abrir la app                                                                                                                                                                                                                                                                                                                                                                    |
| `argentina-clima-pbi/README.md`, `COMO_EJECUTAR.md`, `CONCLUSIONES.md`, `RESUMEN_FUNCIONAMIENTO.md` | Objetivo y estructura del backend, pasos numerados de ejecución, conclusiones completas (fuente del PDF) y cómo se construyó cada parte                                                                                                                                                                                                                                                               |
| `argentina-clima-front/README.md`, `COMO_EJECUTAR.md`                                                   | Cómo levantar el front, cómo se explican los términos, estructura de Respuesta, componentes de diseño                                                                                                                                                                                                                                                                                                |

---

## 11. Decisiones tomadas y cosas descartadas

- **El modelo predice el crecimiento económico a partir del clima** (no la temperatura). Fue un cambio pedido por el usuario ("¿por qué predecís temperatura si la pregunta es sobre la economía?").
- **Regresión con efectos fijos** en lugar de las 96 correlaciones individuales como método central.
- **Placebo, permutación, dosis-respuesta y corrección de Holm** como pruebas duras; se reportan aunque debiliten el resultado.
- **Rendimiento por cultivo** como medida principal del efecto en el campo (sin distorsión de precios).
- **Reorganización numerada del menú** (grupos "1 a 3 · Introducción", "4 · Datos", "5 · Metodología CRISP-DM", "6 y 7", "8", "11", "10", con páginas nuevas Objetivos y pregunta, Descripción de los datos y Plan de trabajo): **construida y luego descartada** por el usuario. Las páginas descartadas se guardaron fuera del proyecto (carpeta temporal `reorganizacion_descartada` de la sesión).
- **Guía de lectura con códigos G1-G23 y bloques de color para conclusiones**: descartadas.
- **Cobertura temporal por fuente** (badges): eliminada; el período está en la ficha de cada dataset.
- **Glosario dentro de la página de respuesta**: eliminado; queda el único glosario final.

---

## 12. Estado de la comparación con el Trabajo Integrador (pendiente de decidir)

El documento del Trabajo Integrador (secciones de modelado, evaluación y conclusiones) describe un modelo que **predice la anomalía de temperatura** a partir de PBI, CO₂ y precipitación (RMSE lineal 0,382 y Random Forest 0,429 contra una línea base de 0,268; hipótesis de desacople). La aplicación, en cambio, modela el **crecimiento económico** desde el clima. Hay que elegir cuál versión rige y actualizar la otra antes de entregar. **No se modificó el documento.**

---

## 13. Límites del trabajo (mantener a la vista)

Solo 19 años de PBG por sector y provincia (2005-2023); temperatura y lluvia provinciales de un punto (la capital) y satelitales (NASA POWER); "año seco" es una definición propia; GEI con solo 13 años comparables; PBI per cápita solo nacional (falta usar la población provincial); se probaron muchas combinaciones y el resultado del valor de la producción del campo no sobrevive a Holm; ningún resultado prueba causalidad; la soja falla un placebo.

## 14. Pendientes conocidos

1. Elegir modelo rector (temperatura o economía) y alinear el documento del TI con la app.
2. Usar la población provincial (ya descargada) para el PBI per cápita provincial.
3. Sección 17 de `proyecto.txt` (regiones) y agrupación de provincias (clustering), no hechas.
4. Confirmar si la explicación de cada gráfico va siempre dentro de un recuadro (hoy solo en Análisis nacional).
5. La pregunta central de la Portada sigue siendo la del Trabajo Integrador original (temperatura); alinearla cuando se decida el modelo rector (punto 1).
6. Revisar textos largos y tarjetas en el resto de las pestañas de Respuesta y en Provincial/Modelos con la misma regla visual.
7. Mejoras de la respuesta sin datos nuevos: traducir el efecto a pesos, bootstrap por provincia, tendencia propia por provincia, índice de sequía (SPI) con la lluvia mensual, clima de la temporada de cultivo para el valor agregado.

---

## 15. Cómo reconstruir todo desde cero (orden)

1. Crear la carpeta de trabajo con `proyecto.txt`, `ver.txt` y los dos `.docx` (no se editan).
2. Crear el entorno virtual en una **ruta corta fuera de la carpeta del proyecto** (`python -m venv C:\Users\tu_usuario\.venvs\clima`), instalar `requirements.txt` del front y sumar `statsmodels`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `openpyxl`, `xlrd`, `requests`, `joblib`. Recién después crear `argentina-clima-front/`.
3. Crear `argentina-clima-pbi/` con `src/`, `data/`, `outputs/` y escribir los módulos de la sección 6 en el orden 1-16, cumpliendo las reglas de la sección 2.1 (nada inventado, sin imputar, solo Argentina).
4. Descargar las 13 fuentes (`descarga_datos`), documentarlas en `data/sources.csv` (con `por_que`, `para_que`, `conteo_claves`), contar filas, generar la guía de verificación.
5. Ejecutar todos los análisis y verificar que las cifras de la sección 7 coincidan.
6. Copiar salidas a `argentina-clima-front/data_front/` (regla de la sección 3.2).
7. Construir el front: `utils/datos.py`, `utils/ui.py` (glosario, componentes y CSS de la sección 9), `utils/pdf.py` + fuentes DejaVu, las 13 páginas de la sección 8 y `streamlit_app.py` con la navegación de 8.1.
8. Escribir los informes y guías de la sección 10, y aplicar las reglas de redacción de 2.2.
9. Probar: `AppTest` de las 13 páginas sin excepciones; capturas de pantalla de Respuesta, Fuentes y Análisis nacional; verificar tarjetas iguales, sin scroll horizontal ni en tablas, sin texto cortado.

## 16. Cómo volver atrás

- Descomprimir `_RESPALDO/respaldo_2026-09-25_estado_actual.zip` sobre esta carpeta (reemplaza los archivos por los de este estado).
- Este documento describe ese mismo estado; si algo no coincide con lo que se ve, manda el documento.
