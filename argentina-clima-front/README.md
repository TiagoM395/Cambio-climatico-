# Cómo levantar el proyecto

## 1. Dónde está el entorno virtual

El entorno virtual **no** está dentro de esta carpeta, sino en
`C:\Users\tiago\.venvs\clima`.

**¿Por qué?** Cuando el proyecto estaba en una carpeta muy larga, Windows no
lograba cargar las DLL de `shapely` y `geopandas` (error: `ImportError: DLL load
failed while importing lib: El nombre del archivo o la extensión es demasiado
largo.`). El entorno quedó en una ruta corta y no se movió cuando la carpeta
del proyecto se mudó. Todo lo demás (código, datos, resultados) sí está en esta
carpeta.

## 2. Levantar la aplicación (todo en una línea)

```powershell
cd "C:\Trabajo base cambio climatico\argentina-clima-front"; C:\Users\tiago\.venvs\clima\Scripts\python.exe -m streamlit run streamlit_app.py
```

## 3. Abrir en el navegador

Se abre solo en `http://localhost:8501`. Si no se abre solo, pegar esa
dirección en el navegador.

## 4. Para cerrarlo

Volver a la terminal y presionar `Ctrl+C`.

---

**Las veces siguientes, solo repetir el paso 2.**

## Instalar todo desde cero (otra computadora)

```powershell
python -m venv "C:\Users\tu_usuario\.venvs\clima"; C:\Users\tu_usuario\.venvs\clima\Scripts\python.exe -m pip install -r requirements.txt
```

La ruta del entorno tiene que ser corta, nunca dentro de la carpeta del
proyecto.

## Explicaciones para lectores sin conocimientos técnicos

- Cada término técnico explica qué es **al pasar el mouse** (globo de ayuda). Todas las definiciones viven en `GLOSARIO` de `utils/ui.py`; para agregar una, se suma allí y se usa `termino()` (texto) o `ayuda()` (métricas y columnas).
- Los nombres de columnas y variables se muestran en criollo con `ETIQUETAS_VARIABLES` / `config_columnas()` / `tabla_legible()`.
- Cada sección tiene una línea "¿Para qué sirve?" (`para_que()`).
- Hay **un solo glosario, al final del informe** (página Conclusiones y su PDF), armado desde `GLOSARIO_FINAL`. Si se agrega un término, sumarlo también a esa lista.

## Página "Respuesta a la pregunta"

`app_pages/respuesta.py`: 8 pestañas (pregunta, 6 pasos de evidencia, veredicto). La pestaña 4 ("Los cultivos") lee `rendimiento_*.csv` (generados por `python -m src.analisis_rendimiento_cultivos`; copiarlos a `data_front/tables/` si se vuelve a correr). Lee `impacto_*.csv` de `data_front/tables/`, generados por `python -m src.analisis_impacto_agropecuario` en `argentina-clima-pbi`. Si se vuelve a correr ese script, copiar los `impacto_*.csv` a `data_front/tables/`. El veredicto distingue "demostrado / señal / no detectado" y se recalcula solo desde esas tablas (salvo dos frases sobre provincias concretas en la pestaña 4).

Estructura de la página: 8 pestañas (la 6, "¿Aguanta las pruebas?", lee `robustez_resultados.csv`, generado por `python -m src.analisis_robustez`; copiarlo a `data_front/tables/` si se vuelve a correr). Arriba, **"La respuesta"**: titular, 4 tarjetas con la cifra clave y un desplegable por cada una de las 6 preguntas con su detalle;  y al inicio de cada pestaña 1 a 5, tres cuadros **Qué tengo / Qué demuestro / Cómo lo demuestro** (función `tres_claves()`) y el detalle de cada resultado en desplegables. No hay glosario propio: los términos se definen entre paréntesis en el texto, con globo al pasar el mouse (`termino()`), y en el glosario único de Conclusiones (`GLOSARIO` / `GLOSARIO_FINAL` en `utils/ui.py`). Regla de redacción: el término técnico o la fórmula se mantiene y su significado va entre paréntesis en el mismo texto (nunca una versión "más fácil" aparte ni códigos de referencia); las conclusiones van como texto en cursiva y color (`explicacion()`), no en bloques de color. Si se agrega un término, sumarlo a `GLOSARIO` y `GLOSARIO_FINAL`. El mismo contenido, explicado paso a paso para no técnicos, está en `../LA_PREGUNTA_Y_LA_RESPUESTA.md`: si cambian los resultados, actualizar ambos.

## Componentes de diseño (utils/ui.py)

- `tarjetas([...])`: fila de tarjetas de indicador (etiqueta, cifra, unidad, mini gráfico opcional, descripción y estado). Todas de la misma altura, sin texto cortado. No usar `st.metric` para textos largos.
- `claves(tengo, demuestro, como)`: las tres tarjetas "Qué tengo / Qué demuestro / Cómo lo demuestro", siempre del mismo tamaño.
- `tabla_html(encabezados, filas)`: tabla que ajusta el texto al ancho, sin scroll ni datos cortados (para tablas con texto largo). Para tablas de pocas filas con `st.dataframe` usar `height="content"`.
- `data_front/sources.csv` tiene, por cada fuente, `por_que`, `para_que` y `conteo_claves` (qué filas de `conteo_datasets.csv` le corresponden): la página Fuentes de datos arma con eso la ficha de cada dataset, siempre con su cantidad de filas.
