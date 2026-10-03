# Pendientes del proyecto

Este documento lista **solo lo que falta**. Lo que ya está hecho (resultados, pruebas de robustez, rendimiento por cultivo, descarga y verificación de datasets) está explicado en [LA_PREGUNTA_Y_LA_RESPUESTA.md](LA_PREGUNTA_Y_LA_RESPUESTA.md) y descrito en [AYUDAMEMORIA_COMPLETO.md](AYUDAMEMORIA_COMPLETO.md). Cada término técnico lleva su significado entre paréntesis; el glosario completo está en la página Conclusiones de la aplicación.

**Regla del proyecto:** todos los datos se **descargan** de fuentes oficiales. Nunca se crean, se estiman a mano ni se rellenan. Cada dato nuevo debe tener fuente, período, unidad y cantidad de filas documentados en `argentina-clima-pbi/data/sources.csv`.

---

## 1. Agrupar los gráficos y las métricas más cerca del Marco Metodológico — CRISP-DM

**Qué falta:** hoy los gráficos, tablas y métricas están repartidos en las páginas por tema (Análisis nacional, Análisis provincial, Mapas, Clima y economía, Modelos, Escenarios, Respuesta a la pregunta). No siguen el orden del Marco Metodológico del Trabajo Integrador (entendimiento del problema, entendimiento de los datos, preparación de los datos, modelado, evaluación y despliegue). Falta agruparlos para que cada gráfico y cada métrica quede en la fase que le corresponde, sin repetirse.

**Condiciones** (definidas por el usuario): sin numeración en los títulos (no usar "5.1", "5.2"…), sin páginas nuevas cargadas de texto, sin enlaces entre páginas, y cada contenido en un solo lugar.

**Dónde está hoy cada cosa** (para decidir el agrupamiento):

| Fase del Marco Metodológico | Gráficos y métricas que le corresponden | Dónde están hoy |
|---|---|---|
| Entendimiento del problema | Pregunta, objetivos, por qué importa | Portada y pestaña "La pregunta" de Respuesta a la pregunta |
| Entendimiento de los datos | Evolución nacional y provincial, mapas, cobertura por variable, correlaciones, tendencias | Análisis nacional, Análisis provincial, Mapas, Clima y economía, Datos descargados |
| Preparación de los datos | Unión por año y provincia, validaciones, faltantes, problemas resueltos | Datos descargados y Fuentes de datos |
| Modelado | Modelos predictivos (métricas MAE, RMSE, R²), escenarios de temperatura, y los análisis de efectos fijos y de rendimiento por cultivo | Modelos predictivos, Escenarios futuros y las pestañas 3 y 4 de Respuesta a la pregunta |
| Evaluación | Pruebas duras, veredicto, límites, comparación contra el promedio | Pestañas 5 y 6 y Veredicto de Respuesta a la pregunta, y las métricas de Modelos predictivos |
| Despliegue | Conclusiones, PDF, checklist, explorador | Conclusiones, Checklist del proyecto, Explorador interactivo |

**Lo que está separado y conviene acercar:**
- Las **métricas del modelo** (Modelos predictivos) y las **pruebas de evaluación** (Respuesta a la pregunta) son la misma fase de evaluación, pero están en grupos distintos del menú.
- Los **gráficos originales y los interactivos** de una misma variable (por ejemplo en Análisis provincial y Mapas) siguen conviviendo en la misma página.
- Las **tarjetas de cifras** de la Portada y de Respuesta a la pregunta repiten resultados que también aparecen en las páginas de análisis.

**Propuesta a aprobar** (solo renombrar y reordenar los grupos del menú, sin páginas nuevas):

| Grupo del menú | Páginas |
|---|---|
| Resultado | Inicio, Respuesta a la pregunta |
| Datos | Fuentes de datos, Datos descargados |
| Exploración | Análisis nacional, Análisis provincial, Mapas, Clima y economía |
| Modelado | Modelos predictivos, Escenarios futuros |
| Cierre | Conclusiones, Explorador interactivo, Checklist |

**Decisiones que hay que tomar antes:**
- Si "Respuesta a la pregunta" queda arriba (como resultado) o pasa a la fase de evaluación.
- Cuál modelo rige en el Trabajo Integrador: el de la app (predice el crecimiento económico) o el del documento (predice la temperatura). Hoy no coinciden y las secciones de modelado, evaluación y conclusiones del documento no reflejan lo que muestra la app.
- Si la explicación de cada gráfico va siempre dentro del mismo recuadro (hoy solo en los cuatro gráficos originales de Análisis nacional).

---

## 2. Revisiones de la aplicación que faltan

1. Aplicar el mismo criterio visual (tarjetas del mismo tamaño, tablas sin scroll, texto sin cortar) en las páginas Análisis provincial, Modelos, Escenarios y Explorador, donde todavía hay texto largo y tablas de `st.dataframe`.
2. Verificar en toda la app que **cada mención de un dataset muestre su cantidad de filas** (hoy está en Fuentes de datos y en las pestañas de análisis de Respuesta).
3. Confirmar que cada gráfico tenga su explicación breve y la referencia de sus siglas (hoy hecho en los cuatro gráficos originales de Análisis nacional).
4. La pregunta central de la Portada sigue siendo la del Trabajo Integrador original (predecir la temperatura); alinearla cuando se decida el modelo rector.
5. Regla de sincronización: cuando se vuelve a correr un análisis, copiar sus salidas a `argentina-clima-front/data_front/`.
6. ~~Tarea de orden: borrar el entorno virtual `.venv` que quedó por error en la carpeta principal.~~ **Hecho el 27/09/2026:** el entorno no puede vivir dentro de la carpeta del proyecto (la ruta supera el límite de 260 caracteres de Windows al cargar las DLL de `geopandas`/`shapely`). Ahora está en `C:\Users\tiago\.venvs\clima` y se llama directo, sin `activate`. Ver `COMO_LEVANTAR_EL_PROYECTO.md`.

---

## 3. Preguntas originales que todavía no se responden

Las preguntas salen de `ver.txt` y de la sección 2 de `proyecto.txt`.

| Pregunta original | Estado | Qué falta |
|---|---|---|
| ¿Los años de más crecimiento coinciden con más presión ambiental (CO₂)? | Respondida en parte: se comparó el CO₂ con el crecimiento del PBI per cápita (sin relación) | Un gráfico específico por períodos de alto y bajo crecimiento |
| ¿Los años con temperatura o lluvia anómalas tienen otro desempeño económico? | Respondida para lluvia (años secos) y para temperatura en el campo | Comparar también "años muy cálidos" a nivel país |
| ¿Hay relación con sequías, inundaciones y otros eventos extremos? | No respondida: solo existe "año seco", una definición propia | Registro de emergencias agropecuarias e inundaciones (punto 6.3) |
| ¿Qué relación hay entre sequías y la economía (campo, exportaciones, empleo)? | Respondida en parte: solo producción del campo | Empleo y exportaciones (punto 6.2) |
| ¿Las provincias tienen distinta relación clima ↔ PBI **per cápita**? | No respondida: se usó el PBG total, no per cápita | Usar la población por provincia (punto 6.1) |
| ¿Qué variables climáticas explican mejor las diferencias de PBI per cápita entre provincias? | No respondida | Lo mismo: población provincial |
| ¿Las provincias más expuestas a eventos extremos tienen menor PBI per cápita? (índice de exposición) | No respondida | Población + eventos extremos |
| ¿Se puede predecir el PBI per cápita provincial con clima y economía? | No respondida: el modelo provincial predice el crecimiento del PBG (R² = −0,10) | Población + más variables |
| ¿La relación cambia entre provincias? | Respondida en parte | Agrupar por región (sección 17 de `proyecto.txt`: NOA, NEA, Cuyo, Pampeana, Patagonia) y agrupar provincias por perfil (clustering) |

**Resumen:** lo que no se pudo responder depende de **usar la población de cada provincia** (ya descargada) y de un **registro de eventos extremos**.

---

## 4. Objeciones que todavía no tienen respuesta completa

| Objeción | Qué falta |
|---|---|
| "Es casualidad." (respuesta parcial: el resultado del valor de la producción del campo no sobrevive a la corrección de Holm, p = 0,16) | Corregir el p-valor por **todas** las pruebas del proyecto, no solo por las 6 originales |
| "Cada provincia tiene su propia tendencia." (ya se descuenta en el rendimiento por cultivo, no en el valor agregado) | Agregar una tendencia propia por provincia al análisis del valor de la producción del campo |
| "Con 24 provincias los p-valores no son confiables." | Prueba de *bootstrap* por provincia (repetir el cálculo sacando provincias enteras al azar, miles de veces, y ver cuánto varía el resultado) |
| "NASA POWER es un satélite, no una estación." | Validar contra estaciones meteorológicas en tierra del SMN (fuente candidata, sin verificar) |
| "19 años son pocos." | Sigue vigente para el valor agregado por sector (CEPAL 2005-2023); el rendimiento por cultivo ya usa 42 campañas |
| "La soja falla el placebo." | Investigar por qué el clima de la campaña siguiente aparece asociado al rendimiento de la soja (posible efecto de fondo que hay que separar) |
| "¿Cuánto es eso en plata?" | Traducir el efecto a dinero |

---

## 5. Cómo reforzar la respuesta (sin buscar datos nuevos)

1. **Traducir el efecto a dinero.** Multiplicar el efecto por el valor de la producción de cada cultivo o provincia para decir *cuántos millones de pesos se pierden por cada grado*. Hoy el efecto se expresa en porcentaje y en toneladas (orden de magnitud). Es el cambio que más "punzante" hace al resultado.
2. **Bootstrap por provincia** (ver punto 4).
3. **Tendencia propia de cada provincia** en el valor agregado (ver punto 4).
4. **Índice de sequía (SPI)** calculado con la lluvia mensual de NASA POWER (ya descargada, 12.384 filas): mide cuán seco fue un período comparado con lo normal y es más fino que "25 % con menos lluvia en el año".
5. **Sequías generalizadas:** marcar los años en que muchas provincias estuvieron secas a la vez y ver si el país entero lo sintió (estudio de eventos).
6. **Efecto no lineal y por umbral:** ver si el daño aparece recién a partir de cierto calor.
7. **Clima de la temporada de cultivo también para el valor agregado del campo** (hoy solo se usa para el rendimiento).
8. **Agrupar provincias** por región y por perfil clima-economía (clustering), para poder decir *"el daño se concentra en tal región"*.
9. **Redactar la conclusión final con cuatro partes:** qué, cuánto, dónde y con qué certeza (ejemplo objetivo: *"cada grado de más le cuesta al campo X millones de pesos por año, concentrados en tal región y tal cultivo"*).

---

## 6. Datos nuevos a conseguir

Las fuentes de esta sección son **candidatas**: todavía no se accedió a ninguna para comprobar que el dato exista con el formato y la cobertura necesarios. Antes de usarlas hay que verificarlas, como se hizo con las fuentes actuales.

### 6.1 Población por provincia: ya descargada, falta usarla
- **Estado:** el archivo de proyecciones del INDEC (2010-2040, 744 filas provincia-año) ya está descargado y verificado en `argentina-clima-pbi/data/raw/indec_poblacion_provincial_2010_2040.xls`. Todavía no se usa en ningún análisis.
- **Qué falta:** sumar la población al dataset provincial y calcular el PBG per cápita (`pbg / población`).
- **Qué permitiría responder:** ¿las provincias más expuestas al clima tienen menor PBI per cápita?, ¿qué variables climáticas explican mejor esas diferencias?, y un modelo del PBI per cápita provincial.
- **Límite:** son proyecciones sobre el Censo 2010 y no hay dato anual anterior a 2010; la serie de PBG provincial disponible con población alcanza unos 14 años.
- **Dificultad:** baja. Es el faltante más importante y el más fácil de cubrir.

### 6.2 Empleo y exportaciones agropecuarias
- **Qué es:** cuántas personas trabajan en el sector agropecuario en cada provincia y cuánto se exporta.
- **Por qué hace falta:** hoy se mide la **producción**. El impacto social se ve en el **trabajo** y en el **ingreso de divisas**.
- **Dónde buscarlo (candidatas):** empleo registrado por sector y provincia (Secretaría de Trabajo, SIPA); exportaciones por provincia de origen (INDEC).
- **Cómo se conecta:** dos columnas nuevas en el dataset provincial y un análisis igual al que ya existe para la producción.
- **Dificultad:** media. El empleo informal no queda registrado; hay que aclararlo como límite.

### 6.3 Eventos extremos en lugar de solo la lluvia anual
- **Qué es:** registro de cuándo hubo sequías o inundaciones graves, en qué provincia y de qué magnitud.
- **Por qué hace falta:** hoy "año seco" es solo el 25 % de años con menos lluvia, no una emergencia declarada.
- **Dónde buscarlo (candidatas):** Comisión Nacional de Emergencias y Desastres Agropecuarios (no hay un dataset abierto consolidado; cada provincia publica las suyas), Servicio Meteorológico Nacional, EM-DAT (CRED).
- **Cómo se conecta:** una variable de 0 y 1 por provincia y año (`evento_extremo`) en lugar de `seco`.
- **Dificultad:** media a alta.

### 6.4 Otras fuentes candidatas
- **Índice El Niño / La Niña (ENSO), NOAA:** explica buena parte de las sequías argentinas y permite separar sequía por clima natural de calentamiento de fondo.
- **Estaciones meteorológicas del SMN:** para validar la temperatura de NASA POWER.

### Orden recomendado
| Prioridad | Tarea | Motivo |
|---|---|---|
| 0 | Agrupar gráficos y métricas según el Marco Metodológico (punto 1) | Es lo que más afecta la presentación final |
| 1 | Usar la población provincial (6.1) | Habilita el PBI per cápita provincial, la pregunta original |
| 2 | Puntos 5.1 a 5.5: dinero, bootstrap, tendencia por provincia, SPI, sequías generalizadas | Refuerzan la respuesta sin esperar ninguna fuente |
| 3 | Eventos extremos (6.3) | Cambia "año seco" por emergencias reales |
| 4 | Empleo y exportaciones (6.2) | Suma la dimensión social del trabajo |

## Qué no va a cambiar

Aunque se consigan todos los datos, el resultado puede seguir siendo débil. En ese caso, esa también es una respuesta válida y se informa igual. Lo que no se hace es forzar una conclusión: que dos cosas se muevan juntas no prueba que una cause la otra.

## Pasos para sumar un dato nuevo

1. Verificar la fuente: entrar y confirmar que el dato existe, su período, unidad y licencia.
2. Agregar la descarga a `argentina-clima-pbi/src/descarga_datos.py` para que sea reproducible.
3. Documentarlo en `argentina-clima-pbi/data/sources.csv` (con `por_que`, `para_que` y `conteo_claves`) y en `conteo_datasets.py`.
4. Sumarlo al dataset (`src/construir_dataset.py`) sin imputar ni rellenar faltantes.
5. Correr un análisis nuevo y copiar los resultados a `argentina-clima-front/data_front/tables/`.
6. Actualizar la página **Respuesta a la pregunta**, el conteo de filas (`python -m src.conteo_datasets`) y la guía de verificación (`python -m src.verificar_datasets`).
