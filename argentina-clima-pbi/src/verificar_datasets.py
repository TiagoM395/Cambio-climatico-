"""
verificar_datasets.py
=====================

Genera la guía para que cualquiera (por ejemplo el docente) pueda comprobar que
los datasets son los originales: para cada archivo descargado en data/raw/ indica
la dirección exacta de la fuente, dónde está guardado, cuántas filas tiene, su
tamaño y su huella SHA-256 (un código único: si el archivo se modificara aunque sea
una coma, la huella cambia).

Salidas:
  outputs/tables/verificacion_datasets.csv
  ../VERIFICACION_DE_DATASETS.md   (documento para leer)

Ejecutar (después de descarga_datos y conteo_datasets):
    python -m src.verificar_datasets
"""

import hashlib
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
TABLES = BASE / "outputs" / "tables"
RAIZ = BASE.parent

# archivo local -> (nombre, institución, dirección exacta, cómo buscar el dato en esa dirección, fila en conteo_datasets)
ARCHIVOS = [
    ("ciam_anomalia_temp_precip_nacional.csv", "Anomalía de temperatura y precipitación nacional", "CIAM / SMN (Secretaría de Ambiente)",
     "https://ciam.ambiente.gob.ar/dt_csv.php?dt_id=467", "Se descarga directo (CSV).", "Anomalía de temperatura y precipitación nacional"),
    ("ciam_precipitacion_estaciones.csv", "Precipitación anual por estación meteorológica", "CIAM / SMN (Secretaría de Ambiente)",
     "https://ciam.ambiente.gob.ar/dt_csv.php?dt_id=623", "Se descarga directo (CSV).", "Precipitación anual por estación meteorológica"),
    ("banco_mundial_pbi_crecimiento.csv", "Crecimiento anual del PBI", "Banco Mundial",
     "https://api.worldbank.org/v2/country/ARG/indicator/NY.GDP.MKTP.KD.ZG?format=json&per_page=200",
     "Respuesta de la API convertida a CSV; también visible en https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=AR.",
     "Crecimiento anual del PBI"),
    ("owid_co2_data_mundial.csv", "Emisiones de CO₂, población y PBI (archivo mundial completo)", "Global Carbon Project / Our World in Data",
     "https://owid-public.owid.io/data/co2/owid-co2-data.csv", "Se descarga directo (CSV).", None),
    ("owid_co2_data_argentina.csv", "Emisiones de CO₂, población y PBI (solo Argentina)", "Global Carbon Project / Our World in Data",
     "https://owid-public.owid.io/data/co2/owid-co2-data.csv", "Es el mismo archivo mundial filtrando la columna iso_code = ARG.",
     "Emisiones de CO₂, población y PBI (solo Argentina)"),
    ("nasa_power_temperatura_provincial.csv", "Temperatura anual por provincia", "NASA POWER",
     "https://power.larc.nasa.gov/api/temporal/monthly/point", "API por coordenadas (latitud y longitud de cada capital provincial, en el código de descarga_datos.py).",
     "Temperatura anual por provincia"),
    ("nasa_power_clima_mensual_provincial.csv", "Clima mensual por provincia (temperatura, lluvia, viento)", "NASA POWER",
     "https://power.larc.nasa.gov/api/temporal/monthly/point", "API por coordenadas (latitud y longitud de cada capital provincial, en el código de descarga_datos.py).",
     "Clima mensual por provincia (temperatura, lluvia, viento)"),
    ("cepal_pbg_provincial.xlsx", "Producto bruto geográfico provincial (por sector)", "CEPAL",
     "https://repositorio.cepal.org/server/api/core/bitstreams/539fcce5-8977-4061-a222-fbfd7358a35f/content", "Se descarga directo (Excel).",
     "Producto bruto geográfico provincial (por sector)"),
    ("inventario-nacional-gei-emisiones_hasta_2022.xlsx", "Inventario Nacional de GEI, serie por gas y sector", "Secretaría de Ambiente",
     "https://inventariogei.ambiente.gob.ar/files/inventario-nacional-gei-emisiones_hasta_2022.xlsx", "Se descarga directo (Excel). Portal: https://inventariogei.ambiente.gob.ar/resultados.",
     "Inventario Nacional de GEI, serie por gas y sector"),
    ("desagregacion-provincial_hasta_2022.xlsx", "Inventario de GEI desagregado por provincia", "Secretaría de Ambiente",
     "https://inventariogei.ambiente.gob.ar/files/desagregacion-provincial_hasta_2022.xlsx", "Se descarga directo (Excel). Portal: https://inventariogei.ambiente.gob.ar/resultados.",
     "Inventario de GEI desagregado por provincia"),
    ("magyp_estimaciones_agricolas.csv", "Estimaciones agrícolas por cultivo, provincia y departamento", "Ministerio de Economía - Secretaría de Agricultura, Ganadería y Pesca",
     "https://datos.magyp.gob.ar/dataset/estimaciones-agricolas",
     "En esa página, el recurso \"Estimaciones agrícolas\" (CSV). Descarga directa por identificador: "
     "https://datos.magyp.gob.ar/dataset/9e1e77ba-267e-4eaa-a59f-3296e86b5f36/resource/95d066e6-8a0f-4a80-b59d-6f28f88eacd5/download/estimaciones-agricolas.csv. "
     "El Ministerio lo actualiza dos veces por año, por lo que una descarga posterior puede tener más campañas que este archivo.",
     "Estimaciones agrícolas por cultivo, provincia y departamento"),
    ("indec_poblacion_provincial_2010_2040.xls", "Población por provincia (proyecciones 2010-2040)", "INDEC",
     "https://www.indec.gob.ar/ftp/cuadros/poblacion/c1_proyecciones_prov_2010_2040.xls", "Se descarga directo (Excel, una hoja por provincia).",
     "Población por provincia (proyecciones)"),
]


def sha256(archivo: Path) -> str:
    h = hashlib.sha256()
    with archivo.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def tamaño(nbytes: int) -> str:
    return f"{nbytes / 1_048_576:.1f} MB" if nbytes >= 1_048_576 else f"{nbytes / 1024:.0f} KB"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    conteo = pd.read_csv(TABLES / "conteo_datasets.csv").set_index("dataset")
    filas = []
    for archivo, nombre, institucion, url, como, clave in ARCHIVOS:
        ruta = RAW / archivo
        if not ruta.exists():
            print("FALTA", archivo)
            continue
        if clave and clave in conteo.index:
            n = f"{int(conteo.loc[clave, 'filas']):,}".replace(",", ".") + f" ({conteo.loc[clave, 'unidad']})"
        elif archivo == "owid_co2_data_mundial.csv":
            n = f"{int(conteo.loc['Emisiones de CO₂, población y PBI (solo Argentina)', 'unidad'].split('de ')[1].split(' ')[0].replace('.', '')):,}".replace(",", ".") + " (país-año, archivo mundial completo)"
        else:
            n = "—"
        filas.append({
            "archivo": f"argentina-clima-pbi/data/raw/{archivo}", "dataset": nombre, "institucion": institucion, "direccion": url,
            "como_encontrarlo": como, "filas": n, "tamaño": tamaño(ruta.stat().st_size), "bytes": ruta.stat().st_size,
            "descargado": datetime.fromtimestamp(ruta.stat().st_mtime).strftime("%Y-%m-%d"), "sha256": sha256(ruta),
        })
    out = pd.DataFrame(filas)
    TABLES.mkdir(parents=True, exist_ok=True)
    out.to_csv(TABLES / "verificacion_datasets.csv", index=False)

    md = ["# Verificación de los datasets", "",
          "Todos los datos de este proyecto se **descargaron** de fuentes oficiales; ninguno se creó ni se completó a mano. "
          "Esta guía permite comprobarlo: para cada archivo figura **la dirección exacta de donde se descargó**, "
          "**dónde está guardado en el proyecto**, **cuántas filas tiene** y su **huella SHA-256** (un código único que "
          "cambia si el archivo se modifica, aunque sea una coma).", "",
          "## Cómo verificarlo (3 pasos)", "",
          "1. Entrar a la **dirección** del dataset que se quiere comprobar (columna 4) y descargar el archivo.",
          "2. Comparar con el archivo guardado en el proyecto (columna 2): mismas columnas, misma cantidad de filas y mismos valores. "
          "Los datos históricos no cambian; en las fuentes que se actualizan (ver \"Nota\" al final) pueden aparecer años nuevos al final.",
          "3. Para comprobar que el archivo del proyecto **no fue alterado**, calcular su huella y compararla con la de la última columna. "
          "En Windows (PowerShell): `Get-FileHash \"ruta\\del\\archivo\" -Algorithm SHA256`.", "",
          "## Datasets", "",
          "| # | Dataset | Institución | Dirección de la fuente | Archivo en el proyecto | Filas | Tamaño | Descargado | Huella SHA-256 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(filas, 1):
        md.append(f"| {i} | {r['dataset']} | {r['institucion']} | {r['direccion']} | `{r['archivo']}` | {r['filas']} | {r['tamaño']} | {r['descargado']} | `{r['sha256']}` |")
    md += ["", "## Cómo encontrar el dato en cada dirección", ""]
    for i, r in enumerate(filas, 1):
        md.append(f"{i}. **{r['dataset']}**: {r['como_encontrarlo']}")
    md += ["", "## Mapa de límites provinciales", "",
           "El archivo geográfico de provincias (IGN) está en `argentina-clima-pbi/data/raw/geo_ign_provincias/` (8 archivos que forman un mismo mapa). "
           "Dirección: http://www.ign.gob.ar/descargas/geodatos/SHAPES/ign_provincia.zip (también en https://datos.gob.ar, \"Unidades Territoriales - Provincias\").", "",
           "## Nota sobre fuentes que se actualizan", "",
           "Algunas fuentes publican datos nuevos periódicamente (por ejemplo, las estimaciones agrícolas se actualizan dos veces por año). "
           "Si una descarga nueva trae más años que el archivo del proyecto, lo que hay que comparar son los años en común: "
           "deben ser idénticos. Cada archivo guardado corresponde a la fecha de la columna \"Descargado\".", "",
           "## Cómo se calculó esta guía", "",
           "Se genera con `python -m src.verificar_datasets` (lee los archivos de `data/raw/`, no los modifica). "
           "Las fuentes con su metodología y limitaciones están en `argentina-clima-pbi/data/sources.csv` y en la página **Fuentes de datos** de la aplicación."]
    (RAIZ / "VERIFICACION_DE_DATASETS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"OK {len(filas)} datasets verificados -> VERIFICACION_DE_DATASETS.md")


if __name__ == "__main__":
    main()
