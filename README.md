# 🌡️ Clima y economía — Argentina

Análisis del cambio climático y su relación con el crecimiento económico en Argentina

Python Streamlit pandas Plotly GeoPandas Jupyter Fuentes oficiales

Una respuesta verificable a la pregunta "¿el cambio climático afecta a la economía argentina?", construida sobre 14 datasets de organismos oficiales y con cada número trazable hasta el archivo de origen.

## 📋 Tabla de contenidos

- [🧐 ¿Qué es?](#-qué-es)
- [🔬 La pregunta y la respuesta](#-la-pregunta-y-la-respuesta)
- [⚙️ ¿Cómo funciona?](#-cómo-funciona)
- [✨ Características](#-características)
- [🛠️ Tecnologías](#️-tecnologías)
- [🚀 Instalación y uso](#-instalación-y-uso)
- [⚠️ Configuración y tropiezos](#️-configuración-y-tropiezos)
- [📁 Estructura del proyecto](#-estructura-del-proyecto)
- [🏗️ Arquitectura](#️-arquitectura)
- [🔌 Datos y trazabilidad](#-datos-y-trazabilidad)
- [👥 Autores](#-autores)
- [📄 Licencia](#-licencia)

## 🧐 ¿Qué es?

Este proyecto responde con datos reales una pregunta que suele quedar en la opinión: si el clima de Argentina se está calentando, ¿eso se nota en la economía?

La respuesta corta, en una línea: el país se calienta de forma comprobable y el calor reduce el rendimiento de los cultivos, pero ese golpe no se detecta en el PBI total ni en el PBI per cápita.

No es un ejercicio de opiniones. Cada afirmación del proyecto sale de una tabla calculada, cada tabla de un script con nombre, y cada script de un dataset con fuente, fecha de descarga y huella SHA-256. No hay ni un número escrito a mano.

La aplicación es una app web navegable en 13 páginas que muestra los resultados ya calculados, con la explicación al costado de cada cifra: para quien no es técnico, el término técnico se mantiene y su significado va entre paréntesis en el mismo texto.

## 🔬 La pregunta y la respuesta

Pregunta central: **¿el cambio climático afecta a la economía argentina?**

| Evidencia | Resultado | Nivel |
|---|---|---|
| ¿Argentina se está calentando? | +0,13 °C por década (≈ 0,86 °C en 64 años), p < 0,001 | **Demostrado** |
| ¿El calor reduce el rendimiento de los cultivos? | maíz −11,3 %, trigo −13,2 %, soja −8,8 % por cada °C, p < 0,001 | **Demostrado** |
| ¿El calor frena la producción del campo? | −5,6 puntos de crecimiento por °C, p = 0,026 | Señal moderada |
| ¿Los años secos frenan al campo? | −3,0 puntos, p = 0,12 | Señal débil |
| ¿Se nota en la economía total de las provincias? | calor −1,0 puntos por °C (p = 0,17); año seco −0,2 (p = 0,77) | No detectado |
| ¿Se nota en el PBI per cápita del país? | correlación −0,12, p = 0,35 | No detectado |
| ¿La señal del campo aguanta pruebas duras? | pasa 8 de 12 pruebas; con corrección de Holm, p = 0,16 | Señal moderada |

Los tres niveles significan cosas distintas. **Demostrado** es comprobado con solidez. **Señal** es que los datos apuntan en una dirección pero con incertidumbre. **No detectado** es que con estos datos no se distingue de la casualidad, lo cual no implica que el efecto no exista.

Un efecto chico en el promedio del país puede ser grande para las familias que viven de una cosecha. Que no se vea en el PBI total no alcanza para descartar el problema: hay que mirar el sector y la región.

El desarrollo completo de los 6 pasos está en [LA_PREGUNTA_Y_LA_RESPUESTA.md](LA_PREGUNTA_Y_LA_RESPUESTA.md).

## ⚙️ ¿Cómo funciona?

El proyecto separa el cálculo de la presentación. Una cosa es analizar, otra es mostrar: el front nunca recalcula ni inventa nada, solo lee tablas ya generadas.

Secuencia:

1. **Descarga.** `src/descarga_datos.py` baja 12 fuentes oficiales (CIAM/SMN, NASA POWER, Banco Mundial, CEPAL, IGN, Secretaría de Ambiente, Ministerio de Economía, INDEC, Our World in Data). Informa qué fuente falló sin detener las demás y nunca rellena un dato que no pudo bajar.
2. **Integración.** `src/construir_dataset.py` une las series por año en dos datasets: uno nacional (1961-2025) y uno provincial (1981-2025, 24 jurisdicciones).
3. **Análisis.** 21 scripts calculan tendencias, estadística descriptiva, correlaciones clima-economía, regresiones OLS con efectos fijos, random forest, escenarios de proyección y mapas.
4. **Verificación.** `src/verificar_datasets.py` anota la URL, la cantidad de filas y el SHA-256 de cada archivo en [VERIFICACION_DE_DATASETS.md](VERIFICACION_DE_DATASETS.md).
5. **Copia.** Los resultados que el front necesita (CSV y PNG) se copian a `argentina-clima-front/data_front/`.
6. **Presentación.** `streamlit_app.py` navega 13 páginas leyendo únicamente `data_front/`.

Si una tabla falta, la página avisa que falta en vez de mostrar un número inventado.

## ✨ Características

- 🌡️ **Calentamiento nacional y provincial:** tendencia de temperatura y precipitación 1961-2025, con mapa por provincia.
- 🌾 **Rendimiento de cultivos:** efecto del calor de temporada sobre soja, maíz, trigo y girasol, por provincia y a nivel país, con efectos fijos de provincia y año.
- 📉 **Efecto del clima sobre el campo:** PBG agropecuario por provincia, con crecimiento y valor agregado por sector.
- 🗺️ **Mapas oficiales:** 24 polígonos del IGN, sin Bugs de geometría ni generalizaciones.
- 🧪 **Pruebas duras:** 12 tests de robusteza (placebo, dosis-respuesta, permutación, corrección de Holm) contra la señal del campo.
- 🔮 **Escenarios 2030-2050:** continuidad de tendencia, aceleración reciente y comparación con IPCC AR5.
- 📊 **Modelos predictivos:** regresión lineal y random forest, nacional y provincial conjunto, con corte cronológico.
- 🧾 **Trazabilidad completa:** cada dato con su fuente oficial, su fecha y su SHA-256 verificable por el docente.
- 🧭 **Explicaciones al costado de cada cifra:** glosario con globo de ayuda al pasar el mouse y un único glosario al final del informe.
- 📄 **Exportación a PDF:** informe completo generado con fpdf2.
- 📱 **Modo celular:** funciona en el teléfono con la Network URL que muestra Streamlit al arrancar.

## 🛠️ Tecnologías

| Tecnología | Versión | Rol |
|---|---|---|
| Python | 3.10+ (probado en 3.14.4) | Lenguaje único del proyecto |
| Streamlit | 1.57.0 | Interfaz web de las 13 páginas |
| pandas | 2.3.1 | Unión de series, joins por año, agregaciones |
| Plotly | 6.7.0 | Gráficos interactivos y rectas de tendencia |
| GeoPandas | 1.1.4 | Lectura del shapefile del IGN y mapas por provincia |
| pyogrio / pyproj / Shapely | 0.13.0 / 3.8.0 / 2.1.2 | Motor de geometría y sistemas de coordenadas |
| scipy / statsmodels | 1.18.1 / 0.15.0 | Regresiones, p-valores, correlación de Pearson y Spearman |
| scikit-learn | 1.8.0 | Random forest y corte cronológico train/test |
| fpdf2 / markdown | 2.8.8 / 3.10.3 | Generación del informe PDF |
| openpyxl / xlrd | 3.1.5 / 2.0.2 | Lectura de .xlsx y .xls (INDEC, MAQyP) |
| requests | 2.33.1 | Descarga de datos (API y CKAN) |
| matplotlib / seaborn | 3.10.3 / 0.13.2 | Gráficos estáticos para el informe |
| Jupyter | - | Notebook exploratorio |

Los dos `requirements.txt` pinan versiones distintas de scipy y numpy. Si instalás ambos en un mismo entorno, `pip` te va a pedir que elijas una versión.

## 🚀 Instalación y uso

Requisitos:

- Python 3.10 o superior.
- Windows 10/11 (probado en Windows 11 con PowerShell). En Linux y macOS corre todo salvo la nota de rutas largas de abajo.

Clonar, instalar y levantar la app:

```powershell
# 1. Clonar
git clone https://github.com/TiagoM395/Cambio-climatico-.git
cd Cambio-climatico-

# 2. Crear el entorno virtual en una ruta CORTA (ver "Tropiezos")
python -m venv C:\Users\TU_USUARIO\.venvs\clima

# 3. Instalar las dependencias del front
C:\Users\TU_USUARIO\.venvs\clima\Scripts\python.exe -m pip install -r argentina-clima-front\requirements.txt

# 4. Levantar la app
cd argentina-clima-front
C:\Users\TU_USUARIO\.venvs\clima\Scripts\python.exe -m streamlit run streamlit_app.py
```

Se abre solo en `http://localhost:8501`. Para cerrarlo: `Ctrl+C`.

No hace falta activar el entorno con `activate`: se llama directo al intérprete con su ruta completa.

Para levantar solo la app **no hace falta descargar nada**: `argentina-clima-front/data_front/` ya viene con los 32 CSV de resultados, las 21 figuras y el shapefile.

Para reproducir los análisis del backend:

```powershell
pip install -r argentina-clima-pbi\requirements.txt
cd argentina-clima-pbi
python -m src.descarga_datos      # baja las 12 fuentes (tarda bastante)
```

El pipeline completo son 16 pasos, en orden, y están en [argentina-clima-pbi/COMO_EJECUTAR.md](argentina-clima-pbi/COMO_EJECUTAR.md).

## ⚠️ Configuración y tropiezos

La app no necesita variables de entorno ni archivo de configuración. Los únicos puntos de fricción reales:

| Problema | Causa | Solución |
|---|---|---|
| `ImportError: DLL load failed while importing lib: El nombre del archivo o la extensión es demasiado largo` | El entorno quedó en una ruta larga y Windows no carga las DLL de `shapely` y `geopandas` (límite de 260 caracteres) | Crear el venv en `C:\ruta\corta\clima`, nunca dentro del repo |
| El puerto 8501 está ocupado | Hay otra instancia corriendo | Cerrar la terminal anterior, o usar `--server.port 8502` |
| `streamlit` no se reconoce como comando | El script corto a veces no queda en el PATH de Windows | Usar siempre `python -m streamlit run streamlit_app.py` |
| Faltan matplotlib, sklearn, openpyxl al correr un script del backend | El entorno del front no las trae | `pip install -r argentina-clima-pbi\requirements.txt` |

## 📁 Estructura del proyecto

```text
Cambio-climatico-/
├── 📂 argentina-clima-front/         # App web (Streamlit)
│   ├── 📂 app_pages/                 # 13 páginas: inicio, respuesta, fuentes, dataset,
│   │                                 #   nacional, provincial, mapas, correlaciones, modelos,
│   │                                 #   escenarios, explorador, conclusiones, checklist
│   ├── 📂 utils/                     # ui.py (tarjetas, tablas, glosario),
│   │                                 #   datos.py (lectura de data_front), pdf.py (informe)
│   ├── 📂 assets/fonts/              # Tipografías para el PDF
│   ├── 📂 data_front/                # Copia exacta de lo que muestra la app
│   │   ├── 📂 processed/             #   dataset_nacional.csv, dataset_provincial.csv
│   │   ├── 📂 tables/                #   32 tablas de resultados
│   │   ├── 📂 figures/               #   21 figuras
│   │   ├── 📂 geo/                   #   Shapefile del IGN (24 polígonos)
│   │   └── 📄 sources.csv            #   Fuente, período y filas de cada dataset
│   ├── 📄 streamlit_app.py           # Punto de entrada y navegación
│   ├── 📄 requirements.txt
│   ├── 📄 README.md
│   └── 📄 COMO_EJECUTAR.md
│
├── 📂 argentina-clima-pbi/            # Backend de análisis (scripts de Python)
│   ├── 📂 src/                       # 21 scripts + __init__.py
│   │   ├── 📄 descarga_datos.py      #   Las 12 fuentes oficiales
│   │   ├── 📄 construir_dataset.py   #   Unión por año (nacional + provincial)
│   │   ├── 📄 data_loader.py         #   Carga de fuentes documentadas
│   │   ├── 📄 analisis_*.py          #   Nacional, provincial, correlaciones, sequía,
│   │   │                             #   impacto agropecuario, robustez, rendimiento
│   │   ├── 📄 modelo_*.py            #   Regresión lineal + random forest
│   │   ├── 📄 escenarios_proyeccion.py
│   │   ├── 📄 mapas.py
│   │   ├── 📄 conteo_datasets.py     #   Inventario de datasets con su cantidad de filas
│   │   ├── 📄 verificar_datasets.py  #   URL + SHA-256 de cada archivo
│   │   └── 📄 analysis.py, modeling.py, preprocessing.py, visualization.py
│   ├── 📂 data/
│   │   ├── 📂 raw/                   #   Datos originales (12 fuentes, 81 MB)
│   │   ├── 📂 processed/             #   Datasets integrados
│   │   └── 📄 sources.csv            #   Documentación de cada fuente
│   ├── 📂 outputs/
│   │   ├── 📂 figures/               #   Gráficos y mapas
│   │   ├── 📂 tables/                #   Tablas de resultados
│   │   └── 📂 models/                #   Modelos serializados (.joblib)
│   ├── 📂 notebooks/                 # Exploración en Jupyter
│   ├── 📄 main.py                    # Punto de entrada informativo
│   ├── 📄 requirements.txt
│   ├── 📄 README.md
│   ├── 📄 CONCLUSIONES.md
│   └── 📄 COMO_EJECUTAR.md           # El pipeline, en orden
│
├── 📄 LA_PREGUNTA_Y_LA_RESPUESTA.md      # La respuesta explicada paso a paso
├── 📄 EXPLICACION_ORAL_GENERAL.md        # Guion para la defensa oral
├── 📄 AYUDAMEMORIA_COMPLETO.md            # Memoria técnica: entorno, dependencias, tropiezos
├── 📄 VERIFICACION_DE_DATASETS.md        # URL, fecha y SHA-256 de cada dataset
├── 📄 COMO_LEVANTAR_EL_PROYECTO.md       # Instrucciones de arranque
├── 📄 PENDIENTES_PARA_DEMOSTRAR_MAS.md   # Análisis futuros alcanzables
├── 📄 Plan_de_Proyecto_Cambio_Climatico_Argentina_CORREGIDO.docx
├── 📄 Trabajo_Integrador_Cambio_Climatico_Argentina_CORREGIDO.docx
├── 📄 .gitignore
└── 📄 README.md
```

## 🏗️ Arquitectura

El proyecto tiene dos capas con una única frontera: los archivos de `data_front/`. El front no importa código del backend, solo lee tablas y figuras.

```text
CAPA 1 — BACKEND (argentina-clima-pbi)

  Fuentes oficiales
        ↓
  data/raw/  ──→  construir_dataset.py  ──→  data/processed/*.csv
        ↓
  análisis · modelos · mapas · escenarios
        ↓
  outputs/tables/ · outputs/figures/ · outputs/models/
        ↓
  verificar_datasets.py  ──→  ../VERIFICACION_DE_DATASETS.md
        ↓
  copia de los .csv y .png que el front necesita


CAPA 2 — FRONT (argentina-clima-front)

  data_front/  ──→  utils/datos.py  ──→  app_pages/*.py  ──→  streamlit_app.py
        ↓
  13 páginas con tablas, mapas, gráficos interactivos y glosario
```

El front nunca recalcula. Si hace falta un número nuevo, se agrega un script al backend, se corre, se copia el resultado a `data_front/` y la página lo lee.

## 🔌 Datos y trazabilidad

14 datasets, 12 fuentes oficiales distintas, todos con fuente, período y cantidad de filas documentados:

| Dataset | Fuente | Período | Filas |
|---|---|---|---|
| Anomalía de temperatura y precipitación nacional | CIAM / SMN | 1961-2025 | 65 años |
| Precipitación anual por estación meteorológica | CIAM / SMN | 2010-2024 | 26 estaciones |
| Crecimiento anual del PBI | Banco Mundial | 1960-2025 | 66 años |
| Emisiones de CO₂, población y PBI (solo Argentina) | Global Carbon Project / OWID | 1850-2024 | 175 años |
| Temperatura anual por provincia | NASA POWER | 1981-2025 | 1.080 provincia-año |
| Clima mensual por provincia | NASA POWER | 1981-2023 | 12.384 provincia-mes |
| Producto bruto geográfico provincial (por sector) | CEPAL | 2004-2024 | 1.350 filas |
| Inventario Nacional de GEI (serie nacional) | Secretaría de Ambiente | 1990-2022 | 7.780 filas |
| Inventario de GEI desagregado por provincia | Secretaría de Ambiente | 2010-2022 | 876 filas |
| Estimaciones agrícolas por cultivo | Ministerio de Economía (Agricultura) | 1969-2024 | 160.499 filas |
| Población por provincia (proyecciones) | INDEC | 2010-2040 | 744 provincia-año |
| Límites de provincias (mapa) | IGN | — | 24 polígonos |

La dirección exacta de cada archivo, su fecha de descarga y su huella SHA-256 están en [VERIFICACION_DE_DATASETS.md](VERIFICACION_DE_DATASETS.md). Un docente puede comprobar que los datos son reales y que no fueron alterados.

## 👥 Autores

- Elias Campos, Romina Guzman, Rodrigo Bulggiani, Tiago Maidana
<!-- Agregar al resto de los integrantes del grupo -->

