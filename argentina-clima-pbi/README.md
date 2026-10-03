# Análisis del cambio climático y su relación con el crecimiento económico en Argentina

## Objetivo

Analizar la evolución histórica de la temperatura, precipitaciones y
emisiones de CO₂ en Argentina, su relación con el crecimiento
económico, y las diferencias entre jurisdicciones (23 provincias + CABA
+ agregado nacional), con modelos para estimar la evolución futura de
la temperatura. **Análisis limitado exclusivamente a Argentina.**

## Estado

✅ Completo — 39/40 secciones de `proyecto.txt` cubiertas (pendiente:
sección 17, agrupación secundaria por regiones NOA/NEA/Cuyo/Pampeana/
Patagonia). Ver [`CONCLUSIONES.md`](CONCLUSIONES.md) (hallazgos) y
[`RESUMEN_FUNCIONAMIENTO.md`](RESUMEN_FUNCIONAMIENTO.md) (cómo se
construyó cada parte, checklist completo en el front).

Además de las 40 secciones originales, se sumaron dos análisis pedidos
después: **PBI per cápita** (nacional) y **años de sequía vs. crecimiento
económico** (nacional y provincial) — ver "Relación clima-economía" y
"PBI per cápita y años de sequía" en `CONCLUSIONES.md`.

**Pendiente (documentado, no implementado):** PBI per cápita *por
provincia* (no hay población provincial en ninguna fuente del proyecto)
y clustering de provincias por perfil clima-economía (descartado por
prioridad, no por falta de datos — ver "Pendientes" en `CONCLUSIONES.md`).

## La pregunta central y su respuesta

¿El cambio climático afecta a la economía argentina? Respuesta corta: el
clima cambió con seguridad (+0,13 °C por década) y hay indicios de que le
cuesta al campo, pero con estos datos no se puede demostrar que afecte al
PBI total ni al per cápita. El paso a paso (qué datos tengo, qué demuestro,
cómo lo demuestro) está en [`../LA_PREGUNTA_Y_LA_RESPUESTA.md`](../LA_PREGUNTA_Y_LA_RESPUESTA.md);
los faltantes para demostrar más, en [`../PENDIENTES_PARA_DEMOSTRAR_MAS.md`](../PENDIENTES_PARA_DEMOSTRAR_MAS.md).

## Front-end

Hay una app de Streamlit que presenta todo este proyecto de forma
navegable, en `../argentina-clima-front/` (carpeta separada e
independiente; no la modifica ni depende de ella en tiempo de
ejecución). Ver su `README.md` para ejecutarla.

## Instalación y ejecución

Ver [`COMO_EJECUTAR.md`](COMO_EJECUTAR.md) — guía completa y probada.

```bash
pip install -r requirements.txt
python -m src.descarga_datos
python -m src.construir_dataset
# ...y 12 scripts más (ver COMO_EJECUTAR.md)
```

Sin interfaz gráfica: pipeline de scripts de consola, resultados como
archivos (PNG/CSV/modelos) en `outputs/`.

## Fuentes de datos

13 fuentes reales documentadas en [`data/sources.csv`](data/sources.csv):
CIAM/SMN, Inventario Nacional de GEI, Banco Mundial, OWID/Global Carbon
Project, CEPAL, INDEC (referencia y población provincial), NASA POWER, IGN
(geometría) y Ministerio de Economía (estimaciones agrícolas por cultivo).
Los archivos completos están en `data/raw/`; la dirección exacta de cada
uno, sus filas y su huella SHA-256 para verificarlos están en
[`../VERIFICACION_DE_DATASETS.md`](../VERIFICACION_DE_DATASETS.md).
El rendimiento por cultivo se usa en `src/analisis_rendimiento_cultivos.py` (pestaña 4 de la
respuesta); la población provincial está descargada y verificada pero todavía no se usa en ningún análisis.

## Variables principales

| Variable | Descripción |
|---|---|
| `año` | Año de observación |
| `jurisdiccion` | Provincia, CABA o Argentina |
| `anomalia_temperatura` | Anomalía de temperatura media anual (°C, base 1991-2020) |
| `precipitaciones` | Precipitación anual |
| `emisiones_gei_co2eq` | Emisiones de GEI en CO2 equivalente |
| `pbi_crecimiento_pct` | Crecimiento real anual del PBI (nacional) |
| `pib_per_capita` / `pib_per_capita_crecimiento_pct` | PBI per cápita nacional y su variación anual (Maddison, vía OWID) |
| `pbg` | Producto Bruto Geográfico provincial |

## Estructura

```
argentina-clima-pbi/
├── data/{raw,processed,sources.csv}
├── notebooks/analisis_argentina.ipynb
├── src/            # 16 módulos: descarga, construcción, análisis, modelos, mapas
├── outputs/{figures,tables,models}
├── main.py, requirements.txt
├── README.md, COMO_EJECUTAR.md, CONCLUSIONES.md, RESUMEN_FUNCIONAMIENTO.md
```

Fuera de esta carpeta (en la raíz): `LA_PREGUNTA_Y_LA_RESPUESTA.md`,
`PENDIENTES_PARA_DEMOSTRAR_MAS.md`, `COMO_LEVANTAR_EL_PROYECTO.md`.

## Reproducibilidad

Todo resultado proviene de datos procesados y código versionado. No hay
valores, coeficientes, métricas ni predicciones escritos a mano.
