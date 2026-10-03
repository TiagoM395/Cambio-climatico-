"""
descarga_datos.py
===================

Descarga las fuentes documentadas en `data/sources.csv` y las guarda tal
cual en `data/raw/`, sin transformarlas. Si una fuente no puede
descargarse, se informa explícitamente, nunca se inventa un reemplazo.

Ejecutar:
    python -m src.descarga_datos
"""

from pathlib import Path
import io
import time
import zipfile
import requests
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

CAPITALES_PROVINCIALES = {
    "CABA": (-34.6037, -58.3816),
    "Buenos Aires": (-34.9215, -57.9545),
    "Catamarca": (-28.4696, -65.7852),
    "Chaco": (-27.4513, -58.9866),
    "Chubut": (-43.3002, -65.1023),
    "Córdoba": (-31.4201, -64.1888),
    "Corrientes": (-27.4692, -58.8306),
    "Entre Ríos": (-31.7333, -60.5297),
    "Formosa": (-26.1775, -58.1781),
    "Jujuy": (-24.1858, -65.2995),
    "La Pampa": (-36.6167, -64.2833),
    "La Rioja": (-29.4131, -66.8558),
    "Mendoza": (-32.8908, -68.8272),
    "Misiones": (-27.3671, -55.8961),
    "Neuquén": (-38.9516, -68.0591),
    "Río Negro": (-40.8135, -62.9967),
    "Salta": (-24.7859, -65.4117),
    "San Juan": (-31.5375, -68.5364),
    "San Luis": (-33.2950, -66.3356),
    "Santa Cruz": (-51.6230, -69.2168),
    "Santa Fe": (-31.6333, -60.7000),
    "Santiago del Estero": (-27.7834, -64.2642),
    "Tierra del Fuego, Antártida e Islas del Atlántico Sur": (-54.8019, -68.3030),
    "Tucumán": (-26.8241, -65.2226),
}


def _descargar_archivo(url: str, destino: Path, headers: dict | None = None) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, headers=headers or {"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    destino.write_bytes(resp.content)
    print(f"OK  {destino.name}  ({len(resp.content)} bytes)")


def descargar_anomalia_nacional():
    url = "https://ciam.ambiente.gob.ar/dt_csv.php?dt_id=467"
    _descargar_archivo(url, RAW_DIR / "ciam_anomalia_temp_precip_nacional.csv")


def descargar_precipitacion_estaciones():
    url = "https://ciam.ambiente.gob.ar/dt_csv.php?dt_id=623"
    _descargar_archivo(url, RAW_DIR / "ciam_precipitacion_estaciones.csv")


def descargar_inventario_gei():
    base = "https://inventariogei.ambiente.gob.ar/files/"
    for nombre in [
        "inventario-nacional-gei-emisiones_hasta_2022.xlsx",
        "desagregacion-provincial_hasta_2022.xlsx",
    ]:
        _descargar_archivo(base + nombre, RAW_DIR / nombre)


def descargar_pbg_cepal():
    url = "https://repositorio.cepal.org/server/api/core/bitstreams/539fcce5-8977-4061-a222-fbfd7358a35f/content"
    _descargar_archivo(url, RAW_DIR / "cepal_pbg_provincial.xlsx")


def descargar_pbi_crecimiento_banco_mundial():
    url = (
        "https://api.worldbank.org/v2/country/ARG/indicator/NY.GDP.MKTP.KD.ZG"
        "?format=json&per_page=200"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    datos = resp.json()[1]
    df = pd.DataFrame(
        [{"año": int(d["date"]), "pbi_crecimiento_pct": d["value"]} for d in datos]
    ).sort_values("año")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destino = RAW_DIR / "banco_mundial_pbi_crecimiento.csv"
    df.to_csv(destino, index=False)
    print(f"OK  {destino.name}  ({len(df)} filas, {df['año'].min()}-{df['año'].max()})")


def descargar_co2_owid():
    url = "https://owid-public.owid.io/data/co2/owid-co2-data.csv"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destino = RAW_DIR / "owid_co2_data_mundial.csv"
    destino.write_bytes(resp.content)
    df = pd.read_csv(destino)
    df_arg = df[df["iso_code"] == "ARG"].copy()
    destino_arg = RAW_DIR / "owid_co2_data_argentina.csv"
    df_arg.to_csv(destino_arg, index=False)
    print(f"OK  {destino.name}  ({len(df)} filas mundiales)")
    print(f"OK  {destino_arg.name}  ({len(df_arg)} filas filtradas a Argentina)")


def descargar_temperatura_nasa_power(anio_inicio: int = 1981, anio_fin: int = 2025):
    filas = []
    for jurisdiccion, (lat, lon) in CAPITALES_PROVINCIALES.items():
        url = (
            "https://power.larc.nasa.gov/api/temporal/monthly/point"
            f"?parameters=T2M&community=RE&longitude={lon}&latitude={lat}"
            f"&start={anio_inicio}&end={anio_fin}&format=JSON"
        )
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            datos = resp.json()["properties"]["parameter"]["T2M"]
        except Exception as e:
            print(f"AVISO: no se pudo descargar NASA POWER para {jurisdiccion}: {e}")
            continue
        for clave, valor in datos.items():
            mes = clave[-2:]
            anio = int(clave[:4])
            if mes == "13":
                filas.append({
                    "jurisdiccion": jurisdiccion, "año": anio,
                    "temperatura_media_c": valor, "latitud": lat, "longitud": lon,
                })
        time.sleep(0.3)
        print(f"OK  NASA POWER: {jurisdiccion}")

    df = pd.DataFrame(filas)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destino = RAW_DIR / "nasa_power_temperatura_provincial.csv"
    df.to_csv(destino, index=False)
    print(f"OK  {destino.name}  ({len(df)} filas)")


def descargar_clima_mensual_provincial(anio_inicio: int = 1981, anio_fin: int = 2023):
    """
    Ampliación (no reemplaza descargar_temperatura_nasa_power): temperatura
    (T2M), precipitación (PRECTOTCORR) y viento (WS2M) MENSUALES por
    provincia, no solo el promedio anual. Da ~24 provincias × ~43 años ×
    12 meses ≈ 12.000+ filas reales (no infladas), y agrega la variable
    de viento que antes no estaba.
    """
    parametros = "T2M,PRECTOTCORR,WS2M"
    filas = []
    for jurisdiccion, (lat, lon) in CAPITALES_PROVINCIALES.items():
        url = (
            "https://power.larc.nasa.gov/api/temporal/monthly/point"
            f"?parameters={parametros}&community=RE&longitude={lon}&latitude={lat}"
            f"&start={anio_inicio}&end={anio_fin}&format=JSON"
        )
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            datos = resp.json()["properties"]["parameter"]
        except Exception as e:
            print(f"AVISO: no se pudo descargar clima mensual NASA POWER para {jurisdiccion}: {e}")
            continue

        for clave in datos["T2M"].keys():
            mes = clave[-2:]
            if mes == "13":  # promedio anual calculado por la API, no es un mes real
                continue
            anio = int(clave[:4])
            fila = {
                "jurisdiccion": jurisdiccion, "año": anio, "mes": int(mes),
                "temperatura_c": datos["T2M"].get(clave),
                "precipitacion_mm": datos["PRECTOTCORR"].get(clave),
                "viento_ms": datos["WS2M"].get(clave),
                "latitud": lat, "longitud": lon,
            }
            filas.append(fila)
        time.sleep(0.3)
        print(f"OK  clima mensual NASA POWER: {jurisdiccion}")

    df = pd.DataFrame(filas)
    for col in ["temperatura_c", "precipitacion_mm", "viento_ms"]:
        df.loc[df[col] <= -900, col] = pd.NA  # -999.0 = código de dato faltante
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destino = RAW_DIR / "nasa_power_clima_mensual_provincial.csv"
    df.to_csv(destino, index=False)
    print(f"OK  {destino.name}  ({len(df)} filas)")


def descargar_estimaciones_agricolas():
    """Superficie sembrada/cosechada, produccion y rendimiento por cultivo, provincia y departamento, 1969-2025
    (Ministerio de Economia, Secretaria de Agricultura, Ganaderia y Pesca). Se usa el identificador del recurso
    (estable) y no el nombre del archivo, que cambia con cada actualizacion semestral."""
    url = ("https://datos.magyp.gob.ar/dataset/9e1e77ba-267e-4eaa-a59f-3296e86b5f36/resource/"
           "95d066e6-8a0f-4a80-b59d-6f28f88eacd5/download/estimaciones-agricolas.csv")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120)
    resp.raise_for_status()
    (RAW_DIR / "magyp_estimaciones_agricolas.csv").write_bytes(resp.content)
    print(f"OK  magyp_estimaciones_agricolas.csv  ({len(resp.content)} bytes)")


def descargar_poblacion_provincial_indec():
    """Poblacion estimada al 1 de julio de cada anio 2010-2040, por provincia (INDEC, proyecciones sobre Censo 2010)."""
    url = "https://www.indec.gob.ar/ftp/cuadros/poblacion/c1_proyecciones_prov_2010_2040.xls"
    _descargar_archivo(url, RAW_DIR / "indec_poblacion_provincial_2010_2040.xls")


def descargar_geometria_ign():
    """IGN: shapefile oficial de provincias, usado por src/mapas.py."""
    url = "http://www.ign.gob.ar/descargas/geodatos/SHAPES/ign_provincia.zip"
    destino = RAW_DIR / "geo_ign_provincias"
    destino.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for nombre_interno in zf.namelist():
            nombre_archivo = Path(nombre_interno).name
            if not nombre_archivo:
                continue
            with zf.open(nombre_interno) as origen:
                (destino / nombre_archivo).write_bytes(origen.read())
    print(f"OK  geo_ign_provincias/ ({len(list(destino.iterdir()))} archivos)")


def descargar_todo():
    tareas = [
        descargar_anomalia_nacional,
        descargar_precipitacion_estaciones,
        descargar_inventario_gei,
        descargar_pbg_cepal,
        descargar_pbi_crecimiento_banco_mundial,
        descargar_co2_owid,
        descargar_temperatura_nasa_power,
        descargar_clima_mensual_provincial,
        descargar_geometria_ign,
        descargar_estimaciones_agricolas,
        descargar_poblacion_provincial_indec,
    ]
    for tarea in tareas:
        print(f"\n--- {tarea.__name__} ---")
        try:
            tarea()
        except Exception as e:
            print(f"ERROR en {tarea.__name__}: {e}")
            print("No se inventan datos para reemplazar esta fuente.")


if __name__ == "__main__":
    descargar_todo()
