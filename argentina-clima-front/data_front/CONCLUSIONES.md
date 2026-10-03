# Conclusiones

Responde exclusivamente las preguntas de investigación de `proyecto.txt`
(sección 2). Cada afirmación está trazada a una tabla o gráfico concreto
en `outputs/`. Para verlo navegable, con gráficos interactivos, ver el
front-end en `../argentina-clima-front/`.

## Hallazgos nacionales

- **Temperatura:** tendencia de calentamiento de **+0.0135 °C/año**
  (1961-2025), significativa (p<0.001, R²=0.44). 2023 fue el año con
  mayor anomalía (+0.83 °C sobre base 1991-2020).
- **Precipitaciones:** sin tendencia significativa (p=0.91).
- **Emisiones de GEI (2010-2022):** pendiente negativa no significativa (p=0.24).
- **PBI:** sin tendencia significativa (p=0.41), alta volatilidad (-10.9% a +10.6%).

## Hallazgos provinciales

- Tendencias de calentamiento significativas más altas: **CABA**
  (+0.032°C/año, p<0.001), **Misiones** (+0.019, p=0.004), **Corrientes**
  y **Chaco** (+0.015, p=0.031), **Buenos Aires** (+0.014, p=0.002).
- Las 5 tendencias más bajas (Santiago del Estero, Catamarca, La Rioja,
  Tucumán, Río Negro) no son estadísticamente significativas.
- Ranking descriptivo, no implica juicio de valor sobre las provincias.
- Precipitación: evolución 2010-2024 documentada por provincia, sin
  tendencia formal calculada (serie corta).

## Relación clima-economía

- **Nacional (año a año):** ninguna asociación significativa (clima vs.
  PBI, p>0.05 en todos los casos).
- **Provincial (dentro de cada provincia, 96 pruebas = 24 provincias × 2
  variables × 2 métodos):** solo 1 dio p<0.05 (Formosa, precipitación-PBG,
  Spearman, p=0.041) — **menos** de lo esperable por azar (~5 de 96). No
  se interpreta como hallazgo real. Con solo 13-15 años de datos por
  provincia, estas pruebas tienen muy poco poder estadístico.
- **Provincial (comparando las 24 provincias entre sí):** cruzando la
  tendencia de precipitación por década de cada provincia (2010-2024)
  contra el crecimiento de su PBG (CAGR 2004-2024) se obtiene una única
  prueba con n=24, más potente que las 96 anteriores: r=-0.19 (p=0.37,
  no significativa). Las provincias donde más bajó la lluvia (Misiones,
  Chaco, Corrientes) crecieron en línea con el promedio nacional o por
  encima; las de peor desempeño económico (Catamarca, Santa Cruz) no son
  las más secas — en Catamarca la lluvia incluso aumentó. Conclusión:
  con los datos disponibles, la diferencia de crecimiento económico entre
  provincias no se explica por cuánto les llueve. Detalle en
  `outputs/tables/ranking_precipitacion_crecimiento_pbg_provincial.csv`.

## PBI per cápita y años de sequía

- **PBI per cápita nacional:** variable nueva, derivada de población y PBI
  (Maddison Project Database, vía OWID; 1961-2022, 62 años). Ni con
  temperatura ni con precipitación se encontró asociación significativa
  (p>0.05 en los cuatro casos) — mismo resultado que con el PBI total.
- **Años de sequía vs. años normales (nacional):** se definió año seco
  como el 25% con menor anomalía de precipitación de la serie 1961-2025
  (17 años secos, 48 normales). El PBI creció en promedio 2.23% en años
  secos vs. 2.35% en normales (prueba t, p=0.94); el PBI per cápita 1.31%
  vs. 1.37% (p=0.97). Ninguna diferencia significativa.
- **Años de sequía vs. normales (provincial, panel de 24 provincias):**
  con años secos definidos por la propia historia de lluvia de cada
  provincia (no un umbral fijo en mm) y el crecimiento del PBG comparado
  contra el promedio histórico de esa misma provincia (para no confundir
  "provincia seca" con "provincia pobre"), la diferencia fue de -0.36
  puntos (p=0.60) — tampoco significativa.
- Conclusión: con los datos disponibles, no se encontró que los años de
  sequía tengan un desempeño económico distinto de los años normales, ni
  a nivel país ni comparando las provincias contra sí mismas. Detalle en
  `outputs/tables/sequia_vs_crecimiento_nacional.csv` y
  `outputs/tables/sequia_vs_crecimiento_provincial.csv`.

## Territorial (mapas)

Los mapas (`outputs/figures/mapa_*.png`, geometría oficial IGN) confirman
visualmente los patrones: mayor calentamiento en CABA/noreste, mayor
precipitación en Misiones, menor en Cuyo — coherente con el clima
conocido de Argentina.

## Resultados del modelo predictivo

Variable elegida a predecir: **el crecimiento económico** (PBI nacional,
PBG provincial) a partir del clima — no al revés, porque la pregunta del
proyecto es si el clima explica a la economía.

- **Nacional** (regresión lineal + Random Forest; año, anomalía de
  precipitación, anomalía de temperatura, CO₂ [OWID] → crecimiento del
  PBI): la **regresión lineal predice mejor que el promedio histórico**
  sobre datos de prueba nunca vistos (R²=0.21, modesto pero real); el
  **Random Forest no** (R²=-0.13). La variable climática con más peso es
  la anomalía de precipitación.
- **Provincial conjunto** (pooled, dummies por provincia; año,
  precipitación, temperatura, emisiones → variación anual del PBG):
  R²=-0.10, sin poder predictivo útil. Variable más importante: "año"
  (probable shock común a todas las provincias, ej. 2020, más que clima).
- No se construyeron modelos individuales por provincia (máx. 13 obs. por provincia).
- Conclusión: a nivel país hay una señal débil pero real de que el clima
  ayuda a explicar el crecimiento del PBI; a nivel provincial, con los
  datos disponibles, el clima solo no alcanza para predecir cómo le va a
  la economía de cada provincia.

## Proyecciones (hasta 2050 / fin de siglo)

| Escenario | Método | Resultado |
|---|---|---|
| A — Continuidad histórica | OLS 1961-2025 (p<0.001) | **+0.66°C** en 2050 (IC95%: +0.04 a +1.28°C) |
| C — Aceleración reciente | OLS 2011-2025 (**p=0.11, no sig.**) | +1.10°C en 2050 (IC95%: +0.03 a +2.18°C) |
| B — IPCC AR5 (externo) | Barros et al. 2014, RCP4.5/8.5 | +1.0 a +3.5°C fin de siglo XXI (no comparable directamente) |

## Limitaciones

- Temperatura provincial: NASA POWER (reanálisis, no estación en tierra).
- Precipitación provincial: 1 estación por provincia, 2010-2024.
- GEI: CO₂ equivalente total, no CO₂ puro; 2010-2022 provincial.
- PBG: estimación CEPAL (2023-2024 preliminares); serie INDEC discontinuada desde 2017.
- 96 correlaciones provinciales sin corrección por comparaciones múltiples.
- PBI per cápita: PBI en dólares internacionales PPA 2011 (Maddison), no
  comparable en nivel con el PBI en pesos constantes de 2004 (Banco
  Mundial/CEPAL) usado en el resto del proyecto — solo se usa su tasa de
  crecimiento, no el nivel. Serie hasta 2022, no 2025 como el resto.
- "Año seco" es una definición estadística de este proyecto (percentil 25
  de la propia serie histórica), no una clasificación oficial de sequía
  del SMN ni de organismos agropecuarios.
- Ningún resultado implica causalidad.

## Pendientes (no implementado)

- **PBI per cápita por provincia:** no existe en ningún archivo del
  proyecto un dato de población por provincia (se buscó explícitamente).
  El PBI per cápita solo se pudo construir a nivel país (ver arriba).
  Para hacerlo por provincia hace falta salir a buscar población
  provincial (INDEC/Censo) — no está.
- **Clustering de provincias** (agrupar las 24 por parecido de perfil
  clima-economía, ej. k-means): no se hizo. Quedó descartado a pedido
  del usuario por ser secundario frente a lo anterior, no por
  imposibilidad de datos — es la pieza más fácil de agregar después si
  hace falta, ya que no requiere ningún dato nuevo.
