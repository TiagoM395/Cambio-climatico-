# Verificación de los datasets

Todos los datos de este proyecto se **descargaron** de fuentes oficiales; ninguno se creó ni se completó a mano. Esta guía permite comprobarlo: para cada archivo figura **la dirección exacta de donde se descargó**, **dónde está guardado en el proyecto**, **cuántas filas tiene** y su **huella SHA-256** (un código único que cambia si el archivo se modifica, aunque sea una coma).

## Cómo verificarlo (3 pasos)

1. Entrar a la **dirección** del dataset que se quiere comprobar (columna 4) y descargar el archivo.
2. Comparar con el archivo guardado en el proyecto (columna 2): mismas columnas, misma cantidad de filas y mismos valores. Los datos históricos no cambian; en las fuentes que se actualizan (ver "Nota" al final) pueden aparecer años nuevos al final.
3. Para comprobar que el archivo del proyecto **no fue alterado**, calcular su huella y compararla con la de la última columna. En Windows (PowerShell): `Get-FileHash "ruta\del\archivo" -Algorithm SHA256`.

## Datasets

| # | Dataset | Institución | Dirección de la fuente | Archivo en el proyecto | Filas | Tamaño | Descargado | Huella SHA-256 |
|---|---|---|---|---|---|---|---|---|
| 1 | Anomalía de temperatura y precipitación nacional | CIAM / SMN (Secretaría de Ambiente) | https://ciam.ambiente.gob.ar/dt_csv.php?dt_id=467 | `argentina-clima-pbi/data/raw/ciam_anomalia_temp_precip_nacional.csv` | 65 (años) | 2 KB | 2026-09-23 | `19e788766a88334d4e074f51e0bf014dbec2d398263b840baaf30e132901d08c` |
| 2 | Precipitación anual por estación meteorológica | CIAM / SMN (Secretaría de Ambiente) | https://ciam.ambiente.gob.ar/dt_csv.php?dt_id=623 | `argentina-clima-pbi/data/raw/ciam_precipitacion_estaciones.csv` | 26 (estaciones) | 3 KB | 2026-09-23 | `c9ddf4ed035baa2be9d960fd968bf5399b171cc7df24b06baec620436bcd8d80` |
| 3 | Crecimiento anual del PBI | Banco Mundial | https://api.worldbank.org/v2/country/ARG/indicator/NY.GDP.MKTP.KD.ZG?format=json&per_page=200 | `argentina-clima-pbi/data/raw/banco_mundial_pbi_crecimiento.csv` | 66 (años) | 2 KB | 2026-09-23 | `8d9fbbf834740b06b7d5f1b790f873afb2a0ae6703dc127cd574d4b1ebac44ba` |
| 4 | Emisiones de CO₂, población y PBI (archivo mundial completo) | Global Carbon Project / Our World in Data | https://owid-public.owid.io/data/co2/owid-co2-data.csv | `argentina-clima-pbi/data/raw/owid_co2_data_mundial.csv` | 50.411 (país-año, archivo mundial completo) | 31.7 MB | 2026-09-23 | `7ec10de1e9502c20c70bfff54476d7893922f7594aa299d9291d87fe49f3e342` |
| 5 | Emisiones de CO₂, población y PBI (solo Argentina) | Global Carbon Project / Our World in Data | https://owid-public.owid.io/data/co2/owid-co2-data.csv | `argentina-clima-pbi/data/raw/owid_co2_data_argentina.csv` | 175 (años; filtrados de 50.411 filas del archivo mundial) | 176 KB | 2026-09-23 | `5f0d45bd5aef79869e6126305086567c3bab40f68e77856a7cb74b18ba10fcad` |
| 6 | Temperatura anual por provincia | NASA POWER | https://power.larc.nasa.gov/api/temporal/monthly/point | `argentina-clima-pbi/data/raw/nasa_power_temperatura_provincial.csv` | 1.080 (provincia-año) | 43 KB | 2026-09-23 | `bb9bd9fb10fe4dfcc86def816ddfed6bd7233777ee916c60d537b4a7eb32d5aa` |
| 7 | Clima mensual por provincia (temperatura, lluvia, viento) | NASA POWER | https://power.larc.nasa.gov/api/temporal/monthly/point | `argentina-clima-pbi/data/raw/nasa_power_clima_mensual_provincial.csv` | 12.384 (provincia-mes) | 640 KB | 2026-09-23 | `fe7f3d3ffd1c21be0204e933e00af01b5f8b0dffd5f764db71cea47d3673b659` |
| 8 | Producto bruto geográfico provincial (por sector) | CEPAL | https://repositorio.cepal.org/server/api/core/bitstreams/539fcce5-8977-4061-a222-fbfd7358a35f/content | `argentina-clima-pbi/data/raw/cepal_pbg_provincial.xlsx` | 1.350 (filas en 25 hojas) | 448 KB | 2026-09-23 | `3b00aca6d8d1dcb9437f76d7bab1651ba5699c3cd02b7eeffc1103f752c92af0` |
| 9 | Inventario Nacional de GEI, serie por gas y sector | Secretaría de Ambiente | https://inventariogei.ambiente.gob.ar/files/inventario-nacional-gei-emisiones_hasta_2022.xlsx | `argentina-clima-pbi/data/raw/inventario-nacional-gei-emisiones_hasta_2022.xlsx` | 7.780 (filas, hoja de la serie) | 578 KB | 2026-09-23 | `e645bde0f04d801fc7fddcfab520a38126052219e72808c1e4bbef748399c686` |
| 10 | Inventario de GEI desagregado por provincia | Secretaría de Ambiente | https://inventariogei.ambiente.gob.ar/files/desagregacion-provincial_hasta_2022.xlsx | `argentina-clima-pbi/data/raw/desagregacion-provincial_hasta_2022.xlsx` | 876 (filas en 26 hojas) | 1.3 MB | 2026-09-23 | `c60cc1c4fae9175afded6fc8fa9df435ff086cf0ac418be4289ff6961013518b` |
| 11 | Estimaciones agrícolas por cultivo, provincia y departamento | Ministerio de Economía - Secretaría de Agricultura, Ganadería y Pesca | https://datos.magyp.gob.ar/dataset/estimaciones-agricolas | `argentina-clima-pbi/data/raw/magyp_estimaciones_agricolas.csv` | 160.499 (cultivo-departamento-año) | 14.8 MB | 2026-09-25 | `7a47a6d356258a69ce0010031f9b2f45ea4c873901d8f812c7c394d9946f9395` |
| 12 | Población por provincia (proyecciones 2010-2040) | INDEC | https://www.indec.gob.ar/ftp/cuadros/poblacion/c1_proyecciones_prov_2010_2040.xls | `argentina-clima-pbi/data/raw/indec_poblacion_provincial_2010_2040.xls` | 744 (provincia-año) | 202 KB | 2026-09-25 | `c651e0f0b237abaf8709dd20e2c8bb62caa3f6ebbd6b77a2b5349a5f81287a5b` |

## Cómo encontrar el dato en cada dirección

1. **Anomalía de temperatura y precipitación nacional**: Se descarga directo (CSV).
2. **Precipitación anual por estación meteorológica**: Se descarga directo (CSV).
3. **Crecimiento anual del PBI**: Respuesta de la API convertida a CSV; también visible en https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=AR.
4. **Emisiones de CO₂, población y PBI (archivo mundial completo)**: Se descarga directo (CSV).
5. **Emisiones de CO₂, población y PBI (solo Argentina)**: Es el mismo archivo mundial filtrando la columna iso_code = ARG.
6. **Temperatura anual por provincia**: API por coordenadas (latitud y longitud de cada capital provincial, en el código de descarga_datos.py).
7. **Clima mensual por provincia (temperatura, lluvia, viento)**: API por coordenadas (latitud y longitud de cada capital provincial, en el código de descarga_datos.py).
8. **Producto bruto geográfico provincial (por sector)**: Se descarga directo (Excel).
9. **Inventario Nacional de GEI, serie por gas y sector**: Se descarga directo (Excel). Portal: https://inventariogei.ambiente.gob.ar/resultados.
10. **Inventario de GEI desagregado por provincia**: Se descarga directo (Excel). Portal: https://inventariogei.ambiente.gob.ar/resultados.
11. **Estimaciones agrícolas por cultivo, provincia y departamento**: En esa página, el recurso "Estimaciones agrícolas" (CSV). Descarga directa por identificador: https://datos.magyp.gob.ar/dataset/9e1e77ba-267e-4eaa-a59f-3296e86b5f36/resource/95d066e6-8a0f-4a80-b59d-6f28f88eacd5/download/estimaciones-agricolas.csv. El Ministerio lo actualiza dos veces por año, por lo que una descarga posterior puede tener más campañas que este archivo.
12. **Población por provincia (proyecciones 2010-2040)**: Se descarga directo (Excel, una hoja por provincia).

## Mapa de límites provinciales

El archivo geográfico de provincias (IGN) está en `argentina-clima-pbi/data/raw/geo_ign_provincias/` (8 archivos que forman un mismo mapa). Dirección: http://www.ign.gob.ar/descargas/geodatos/SHAPES/ign_provincia.zip (también en https://datos.gob.ar, "Unidades Territoriales - Provincias").

## Nota sobre fuentes que se actualizan

Algunas fuentes publican datos nuevos periódicamente (por ejemplo, las estimaciones agrícolas se actualizan dos veces por año). Si una descarga nueva trae más años que el archivo del proyecto, lo que hay que comparar son los años en común: deben ser idénticos. Cada archivo guardado corresponde a la fecha de la columna "Descargado".

## Cómo se calculó esta guía

Se genera con `python -m src.verificar_datasets` (lee los archivos de `data/raw/`, no los modifica). Las fuentes con su metodología y limitaciones están en `argentina-clima-pbi/data/sources.csv` y en la página **Fuentes de datos** de la aplicación.
