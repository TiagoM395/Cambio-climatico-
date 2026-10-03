# Cómo ejecutar este proyecto

Sin interfaz gráfica: pipeline de scripts de Python por consola.

## 1. Requisitos

Python 3.10+, conexión a internet (paso 3 descarga datos reales).

## 2. Instalar

El backend **no tiene entorno propio**: usa el mismo Python del front, que
está en `C:\Users\tiago\.venvs\clima` (ruta corta, porque la de la carpeta del
proyecto es demasiado larga para las DLL de `geopandas`).

```powershell
C:\Users\tiago\.venvs\clima\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Ejecutar en este orden

| # | Comando | Genera |
|---|---|---|
| 1 | `python -m src.descarga_datos` | `data/raw/*` (13 fuentes documentadas, incluye rendimiento por cultivo del Ministerio de Economía y población provincial del INDEC) |
| 2 | `python -m src.construir_dataset` | `data/processed/dataset_{nacional,provincial}.csv` |
| 3 | `python -m src.analisis_nacional` | `outputs/figures/*_argentina.png` |
| 4 | `python -m src.analisis_provincial` | `outputs/figures/*_provincias.png` |
| 5 | `python -m src.analisis_correlacion` | `outputs/tables/correlaciones_*.csv` |
| 6 | `python -m src.modelo_nacional` | `outputs/models/*_nacional.*` |
| 7 | `python -m src.modelo_provincial` | `outputs/models/modelo_rf_provincial_conjunto.joblib` |
| 8 | `python -m src.escenarios_proyeccion` | `outputs/figures/prediccion_temperatura_escenarios.png` |
| 9 | `python -m src.mapas` | `outputs/figures/mapa_*.png` |
| 10 | `python -m src.analisis_clima_economia_provincial` | `outputs/tables/ranking_precipitacion_crecimiento_pbg_provincial.csv` + gráfico |
| 11 | `python -m src.analisis_sequia_economia` | `outputs/tables/sequia_vs_crecimiento_{nacional,provincial}.csv` + gráficos |
| 12 | `python -m src.conteo_datasets` | `outputs/tables/conteo_datasets.csv` (filas de cada dataset descargado) |
| 13 | `python -m src.analisis_impacto_agropecuario` | `outputs/tables/impacto_*.csv` (efecto del clima sobre el campo y la economía provincial; alimenta la página "Respuesta a la pregunta") |
| 15 | `python -m src.verificar_datasets` | `../VERIFICACION_DE_DATASETS.md` y `outputs/tables/verificacion_datasets.csv` (dirección de cada fuente, filas y huella SHA-256 de cada archivo, para que el docente pueda comprobarlos; ejecutar después del paso 12) |
| 16 | `python -m src.analisis_rendimiento_cultivos` | `outputs/tables/rendimiento_*.csv` (efecto del calor sobre el rendimiento de soja, maíz, trigo y girasol, por provincia y a nivel país; tarda ~2 min; alimenta la pestaña 4 de "Respuesta a la pregunta") |
| 14 | `python -m src.analisis_robustez` | `outputs/tables/robustez_resultados.csv` (pruebas duras sobre la señal del campo: placebo, dosis-respuesta, permutación, corrección de Holm; tarda ~20 s; alimenta la pestaña 5 de "Respuesta a la pregunta") |

Todo junto (bash):
```bash
for m in descarga_datos construir_dataset analisis_nacional analisis_provincial analisis_correlacion modelo_nacional modelo_provincial escenarios_proyeccion mapas analisis_clima_economia_provincial analisis_sequia_economia conteo_datasets analisis_impacto_agropecuario analisis_robustez analisis_rendimiento_cultivos verificar_datasets; do python -m src.$m; done
```

✅ Secuencia verificada de punta a punta, sin errores. Las 2 fuentes nuevas (rendimiento por cultivo y población provincial) se descargaron y se comprobaron en la sesión del 25/09/2026.

## 4. Resultados

- Hallazgos: `CONCLUSIONES.md`
- Gráficos/mapas: `outputs/figures/`
- Tablas: `outputs/tables/`
- Modelos: `outputs/models/`
- Cómo se construyó todo: `RESUMEN_FUNCIONAMIENTO.md`

## 5. Si falla un paso

`descarga_datos` informa qué fuente falló sin detener las demás, nunca
inventa datos. Reintentar función puntual:
```bash
python -c "from src.descarga_datos import descargar_temperatura_nasa_power; descargar_temperatura_nasa_power()"
```

## Portabilidad

No hay rutas fijas en el código (todo relativo a `Path(__file__)`):
mover la carpeta a otra ubicación o PC no rompe nada.
