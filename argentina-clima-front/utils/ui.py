"""
utils/ui.py
=============

Utilidades de interfaz compartidas por todas las páginas:

- `GLOSARIO` + `termino()` / `ayuda()`: definiciones en criollo de los
  términos técnicos (R², MAE, p-valor, etc.), para mostrar como tooltip
  nativo (el "globo" que aparece al pasar el mouse) en métricas, columnas
  de tablas y texto suelto. Nunca como bloque de color.
- `explicacion()`: párrafo explicativo con tipografía en color e itálica,
  sin fondo de color (reemplaza a st.info/success/warning/error, que acá
  no se usan para explicar nada).
- `inyectar_estilos()`: se llama una sola vez, en streamlit_app.py.
"""

import streamlit as st

GLOSARIO = {
    "r2": (
        "R² (coeficiente de determinación): compara el modelo contra "
        "predecir siempre el promedio. 1 = predicción perfecta, 0 = igual "
        "de bueno que el promedio, negativo = peor que el promedio."
    ),
    "mae": (
        "MAE (error absoluto medio): en promedio, cuánto se equivoca el "
        "modelo, en las mismas unidades que la variable predicha. Cuanto "
        "más bajo, mejor."
    ),
    "rmse": (
        "RMSE (raíz del error cuadrático medio): como el MAE, pero "
        "penaliza más fuerte los errores grandes."
    ),
    "p_valor": (
        "p-valor: la probabilidad de ver una relación así de fuerte si en "
        "realidad no hubiera ninguna. Por convención, menor a 0.05 se "
        "considera 'estadísticamente significativo'."
    ),
    "pearson": (
        "Coeficiente de Pearson: qué tan lineal es la relación entre dos "
        "variables, de -1 (relación inversa perfecta) a +1 (relación "
        "directa perfecta). 0 = sin relación lineal."
    ),
    "spearman": (
        "Coeficiente de Spearman: como el de Pearson, pero mide si una "
        "variable sube cuando la otra sube (o baja), sin exigir que la "
        "relación sea una línea recta."
    ),
    "metodo": (
        "Cada prueba se calcula de dos formas: Pearson (¿es una relación "
        "en línea recta?) y Spearman (¿suben o bajan juntas, aunque no "
        "sea en línea recta?). Se muestran las dos por honestidad — una "
        "puede detectar algo que la otra no."
    ),
    "cagr": (
        "Crecimiento anual compuesto (CAGR): la tasa de crecimiento anual "
        "constante que, aplicada todos los años, lleva del valor inicial "
        "al valor final del período."
    ),
    "pbg": "PBG — Producto Bruto Geográfico: el equivalente al PBI, pero medido para una sola provincia.",
    "pbi": "PBI — Producto Bruto Interno: el valor de todo lo que produce la economía de un país en un año.",
    "pbi_per_capita": (
        "PBI per cápita: el PBI total dividido por la población. A "
        "diferencia del PBI total, dice si a CADA PERSONA le va mejor o "
        "peor — el PBI total puede subir solo porque hay más gente, "
        "aunque cada uno tenga lo mismo o menos."
    ),
    "prueba_t": (
        "Prueba t: compara el promedio de dos grupos (acá, años secos vs. "
        "años normales) y dice si la diferencia es más grande de lo que "
        "se podría esperar solo por azar. El p-valor de esta prueba se "
        "interpreta igual que cualquier otro: menor a 0.05 = diferencia "
        "estadísticamente significativa."
    ),
    "año_seco": (
        "Año seco (en este proyecto): un año cuya lluvia quedó entre el "
        "25% más bajo de toda la historia disponible de esa misma zona — "
        "no un número fijo de milímetros, porque lo que es poca lluvia en "
        "Misiones es normal en Santa Cruz."
    ),
    "anomalia": (
        "Anomalía: cuánto se aparta el valor de un año del promedio "
        "histórico de referencia (acá, 1991-2020). Positivo = por encima "
        "de lo normal."
    ),
    "tendencia_decada": (
        "Tendencia por década: cuánto sube o baja, en promedio, esa "
        "variable cada 10 años, calculado con una regresión lineal sobre "
        "toda la serie."
    ),
    "pendiente": "Pendiente de la tendencia: cuánto cambia la variable, en promedio, por cada año que pasa.",
    "dummy": (
        "Variable dummy: una columna de 0 y 1 que le indica al modelo a "
        "qué provincia pertenece cada fila, sin inventarle un orden o un "
        "valor numérico a las provincias."
    ),
    "random_forest": (
        "Random Forest: un modelo que combina muchos árboles de decisión "
        "y promedia sus resultados; suele captar relaciones no lineales "
        "mejor que una recta."
    ),
    "regresion_lineal": "Regresión lineal: el modelo más simple — busca la línea recta que mejor se ajusta a los datos.",
    "z_score": (
        "Valor normalizado (z-score): cuántos desvíos estándar está ese "
        "valor por encima o por debajo del promedio de la serie. Sirve "
        "para comparar variables de escalas distintas en el mismo gráfico."
    ),
    "ic95": (
        "Intervalo de confianza del 95%: el rango donde, si se repitiera "
        "el cálculo muchas veces, caería el resultado real el 95% de las "
        "veces. Cuanto más ancho, menos precisa la estimación."
    ),
    "media_movil": "Media móvil: el promedio de los últimos N años, recalculado año a año — suaviza el ruido para ver la tendencia de fondo.",

    # ---- Variables del dataset (qué es cada cosa) ----
    "v_anomalia_temperatura": (
        "Anomalía de temperatura: cuántos grados centígrados (°C) más cálido "
        "o más frío fue un año en Argentina comparado con lo normal (el "
        "promedio de 1991 a 2020). Ejemplo: +0,8 °C = ese año fue casi un "
        "grado más caliente de lo normal."
    ),
    "v_anomalia_precipitacion_pct": (
        "Anomalía de precipitación: cuánto más o menos llovió un año, en "
        "porcentaje (%), comparado con lo normal. Ejemplo: -15 % = llovió "
        "un 15 % menos de lo habitual (año seco); +20 % = año lluvioso."
    ),
    "v_emisiones_gei_co2eq": (
        "Emisiones de gases de efecto invernadero (GEI): todos los gases que "
        "calientan la atmósfera (dióxido de carbono, metano, etc.), sumados "
        "y expresados como si fueran CO₂. Se mide en MtCO₂eq = millones de "
        "toneladas de CO₂ equivalente. Solo hay datos oficiales 2010-2022."
    ),
    "v_emisiones_co2_fosil": (
        "CO₂ fósil: dióxido de carbono que se libera al quemar petróleo, gas "
        "y carbón (transporte, industria, energía). Se mide en millones de "
        "toneladas (Mt) por año."
    ),
    "v_pbi_crecimiento_pct": (
        "Crecimiento del PBI: cuánto creció (o cayó, si es negativo) la "
        "economía del país respecto del año anterior, en porcentaje (%). "
        "Ejemplo: +3 % = la economía produjo un 3 % más que el año pasado."
    ),
    "v_pib_per_capita_crecimiento_pct": (
        "Crecimiento del PBI per cápita: como el crecimiento del PBI, pero "
        "dividido por la población. Dice si a cada persona, en promedio, le "
        "va mejor (+) o peor (-) que el año anterior."
    ),
    "mtco2eq": (
        "MtCO₂eq = millones de toneladas de dióxido de carbono equivalente. "
        "Es la unidad para sumar gases distintos en una sola cifra: cada "
        "gas se convierte a 'cuánto calentaría si fuera CO₂'."
    ),
    "media": "Media (promedio): el valor típico de la variable, sumando todos los años y dividiendo por la cantidad de años.",
    "desvio": (
        "Desvío estándar: cuánto se alejan, en promedio, los años del "
        "promedio. Si es chico, los valores son parecidos entre sí; si es "
        "grande, cambian mucho de un año a otro."
    ),
    "minimo": "Mínimo: el valor más bajo que tuvo la variable en toda la serie.",
    "maximo": "Máximo: el valor más alto que tuvo la variable en toda la serie.",
    "estadistica_descriptiva": (
        "Estadística descriptiva: un resumen en números de cada variable "
        "(promedio, cuánto varía, mínimo y máximo). Sirve para conocer los "
        "datos antes de compararlos o modelarlos."
    ),
    "tendencias": (
        "Tendencia: hacia dónde va una variable con el paso de los años "
        "(sube, baja o se mantiene) y a qué ritmo. Se calcula trazando la "
        "recta que mejor resume la serie."
    ),
    "serie_temporal": "Serie temporal: los valores de una variable ordenados año por año, para ver cómo evolucionó.",
    "boxplot": (
        "Boxplot (caja y bigotes): la caja contiene la mitad central de los "
        "valores, la línea del medio es la mediana y los puntos sueltos son "
        "años atípicos (muy distintos al resto)."
    ),
    "causalidad": (
        "Causalidad: que una cosa PROVOQUE la otra. Que dos variables se "
        "muevan juntas (correlación) no prueba que una cause la otra."
    ),

    "mapa_calor": (
        "Mapa de calor: una tabla donde cada casilla se pinta de un color "
        "según su valor. Acá, cada fila es una provincia y cada columna un "
        "año: rojo = más cálido de lo normal, azul = más frío."
    ),
    "dispersion": (
        "Gráfico de dispersión: cada punto es una provincia, ubicada según "
        "dos medidas a la vez. Sirve para ver si las dos medidas suben y "
        "bajan juntas."
    ),
    "n_obs": "Años con dato: cuántos años tiene esa provincia con información disponible. Más años = conclusión más confiable.",
    "extrapolacion": (
        "Extrapolación de tendencia: prolongar hacia el futuro la recta que "
        "mejor describe el pasado. Supone que el ritmo de cambio se "
        "mantiene, por eso es una estimación y no una certeza."
    ),
    "escenario_a": "Escenario A (continuidad): supone que el calentamiento sigue al mismo ritmo que en toda la serie 1961-2025.",
    "escenario_c": "Escenario C (aceleración reciente): supone que el calentamiento sigue al ritmo de los últimos años, que fue más rápido.",
    "escenario_b": (
        "Escenario B (IPCC): no lo calculó este proyecto. Es una proyección "
        "publicada por científicos del clima (IPCC) para Argentina a fin de siglo."
    ),
    "ipcc": (
        "IPCC: Panel Intergubernamental sobre Cambio Climático de la ONU. "
        "Reúne a miles de científicos y publica los informes de referencia mundial sobre el clima."
    ),
    "reanalisis": (
        "Reanálisis satelital (NASA POWER): estimación de la temperatura y "
        "la lluvia de cada punto del país, armada combinando satélites y "
        "modelos. No es una estación meteorológica en cada provincia."
    ),

    "v_temperatura_media_c": "Temperatura media: el promedio anual de la temperatura del aire en esa provincia, en grados centígrados (°C).",
    "v_precipitaciones_mm": "Precipitación: la lluvia (y nieve) total caída en un año, medida en milímetros (mm). 1 mm equivale a 1 litro de agua por metro cuadrado.",
    "v_pbg": (
        "PBG (Producto Bruto Geográfico): el valor de todo lo que produce la "
        "economía de una provincia en un año. Se mide en millones de pesos "
        "de 2004, para poder comparar años sin que la inflación distorsione."
    ),
    "v_pbg_preliminar": "Indica si el dato de PBG de ese año es preliminar (todavía puede cambiar) o definitivo.",
    "v_poblacion": "Población: cantidad de habitantes de Argentina en ese año.",
    "v_pib_per_capita": "PBI per cápita: el PBI dividido por la cantidad de habitantes. Dice cuánto produce la economía por persona.",
    "v_tipo_jurisdiccion": "Tipo de jurisdicción: si la fila corresponde al país completo (nacional) o a una provincia.",
    "v_año": "Año al que corresponde el dato.",
    "observaciones": "Observaciones: cuántos datos (por ejemplo, años) tiene disponibles esa variable. Más observaciones = análisis más confiable.",
    "faltantes": "Faltantes: años en los que no hay dato. Se dejan vacíos: no se inventan ni se rellenan.",
    "gei": (
        "GEI (gases de efecto invernadero): gases como el dióxido de carbono "
        "y el metano que atrapan calor en la atmósfera y calientan el planeta."
    ),
    "residuo": (
        "Residuo: la diferencia entre lo que pasó de verdad y lo que el "
        "modelo predijo. Residuos chicos y sin patrón = buen modelo."
    ),
    "predictoras": (
        "Variables predictoras: las 'pistas' que el modelo usa para intentar "
        "adivinar el valor que se quiere predecir (por ejemplo, la lluvia y la temperatura)."
    ),
    "importancia": (
        "Importancia de una variable: qué tanto la usó el modelo para reducir "
        "su error. No es un porcentaje del PBI explicado: solo reparte 100 % "
        "entre las variables."
    ),
    "coeficiente": (
        "Coeficiente: cuánto cambia el valor predicho por cada unidad que "
        "sube esa variable, manteniendo las demás iguales."
    ),
    "asociacion": (
        "Asociación estadística: dos variables tienden a moverse juntas. "
        "No significa que una sea la causa de la otra."
    ),
    "predecir_vs_observado": (
        "Predicción vs. observado: se comparan, año por año, el valor que "
        "el modelo predijo con el valor real. Cuanto más pegados, mejor el modelo."
    ),
    "pp": "Punto porcentual (p.p.): la diferencia entre dos porcentajes. Si un sector crece 5 % en un año y 2 % en otro, la diferencia es de 3 puntos porcentuales.",
    "efectos_fijos": (
        "Efectos fijos: un ajuste estadístico que descuenta lo que es propio de cada provincia (por ejemplo, que unas producen "
        "más que otras) y lo que le pasa a todo el país en un mismo año (una crisis, la pandemia). Así solo queda el efecto del clima."
    ),
    "holm": (
        "Corrección de Holm: cuando se prueban muchas cosas a la vez, alguna sale 'significativa' por pura suerte. "
        "Esta corrección endurece el criterio para compensarlo: un resultado que la supera es mucho más creíble."
    ),
    "placebo": (
        "Prueba placebo: se repite el mismo cálculo sobre algo que no debería verse afectado (por ejemplo, el comercio frente al calor). "
        "Si también diera efecto, el resultado original sería sospechoso."
    ),
    "dosis_respuesta": (
        "Dosis-respuesta: si una causa realmente produce un daño, el daño debería crecer con la 'dosis'. "
        "Acá: el calor debería pegar más donde el campo pesa más en la economía."
    ),
    "permutacion": (
        "Prueba de permutación: se mezclan los datos al azar miles de veces y se cuenta cuántas veces el azar produce un efecto "
        "tan grande como el real. No depende de supuestos estadísticos."
    ),
    "rezago": "Efecto rezagado: cuando el clima de un año afecta a los años siguientes, no solo al mismo año.",
    "coropletico": "Mapa coroplético: cada provincia se pinta con un color según el valor de una variable — más oscuro/intenso, más alto el valor.",
}


PAGINAS = {
    "respuesta": (
        "**Qué es:** la página que responde la pregunta central del proyecto: ¿el cambio climático afecta a la economía argentina?\n\n"
        "**Qué vas a ver:** la respuesta resumida arriba y siete pestañas. La primera plantea la pregunta; las cinco siguientes van "
        "paso a paso (el clima cambió, la economía del país, el campo, dónde pega más, si la señal aguanta pruebas duras) y la última es el veredicto.\n\n"
        "**Cómo se lee:** cada gráfico trae debajo una explicación y cada paso termina con una conclusión. El veredicto "
        "distingue lo demostrado, lo que es solo una señal y lo que no se pudo detectar.\n\n"
        "**Ojo:** se muestra lo que dicen los datos reales, aunque no sea lo que se esperaba."
    ),
    "inicio": (
        "**Qué es:** la presentación del proyecto: quién lo hizo, en qué "
        "instituto, y las 5 etapas del trabajo (problema, datos, preparación, "
        "análisis y modelos, conclusiones).\n\n"
        "**Qué vas a ver:** una tarjeta por etapa, con lo más importante de cada una.\n\n"
        "**Para qué sirve:** tener el panorama completo antes de entrar al detalle. "
        "Los números y gráficos están en las demás páginas del menú."
    ),
    "fuentes": (
        "**Qué es:** la lista de todos los datos que usa el proyecto y de dónde salió cada uno.\n\n"
        "**Qué vas a ver:** cuántas filas tiene cada dataset descargado y, por cada fuente, "
        "qué institución la publica, qué mide, en qué unidad, qué años cubre y qué "
        "limitaciones tiene.\n\n"
        "**Para qué sirve:** para poder confiar en los datos (son oficiales y "
        "públicos, ninguno está inventado) o saber por qué desconfiar de alguno."
    ),
    "dataset": (
        "**Qué es:** el detalle de los datos descargados y de cómo se unieron en dos tablas de trabajo.\n\n"
        "**Qué vas a ver:** la cantidad de filas de cada dataset, cuánta información hay de "
        "cada variable (cuántos años y provincias tienen dato) y las tablas finales, una "
        "nacional (una fila por año) y una provincial (una fila por provincia y año).\n\n"
        "**Cómo se lee:** las celdas vacías son años en que la fuente no publicó el dato; "
        "no se rellenan ni se inventan.\n\n"
        "**Para qué sirve:** comprobar que la base sobre la que se hace todo el análisis es "
        "real, completa hasta donde las fuentes lo permiten y sin errores."
    ),
    "nacional": (
        "**Qué es:** el análisis de Argentina como un todo: cómo cambiaron, año por año desde 1961, "
        "la temperatura, la lluvia, las emisiones y el crecimiento de la economía.\n\n"
        "**Qué vas a ver:** una explicación de cada variable, una tabla resumen (promedio, "
        "mínimo, máximo y tendencia) y gráficos de cada una a lo largo del tiempo.\n\n"
        "**Cómo se lee:** en cada gráfico, una línea que sube significa que la variable "
        "aumenta con los años; una que baja, que disminuye.\n\n"
        "**Qué responde:** ¿Argentina se está calentando? ¿llueve más o menos? ¿emite más? "
        "Es la base antes de comparar el clima con la economía o mirar provincia por provincia."
    ),
    "provincial": (
        "**Qué es:** el mismo estudio de temperatura y lluvia, pero separado por provincia. "
        "El promedio del país puede esconder que unas provincias cambian mucho y otras casi nada; "
        "esta página lo muestra.\n\n"
        "**Qué vas a ver:** la evolución de cada provincia, un mapa de colores (provincia por año), "
        "un ranking de las que más se calientan y un comparador donde elegís las que quieras.\n\n"
        "**Cómo se lee:** en el mapa de colores, rojo significa más cálido de lo normal y azul "
        "más frío; cuanto más rojo, más caliente estuvo ese año en esa provincia.\n\n"
        "**Qué responde:** ¿todas las provincias se calientan al mismo ritmo? ¿cuáles cambian "
        "más y cuáles menos? ¿dónde llueve más o menos que antes?"
    ),
    "mapas": (
        "**Qué es:** los mismos datos por provincia, pintados sobre el mapa de Argentina.\n\n"
        "**Qué vas a ver:** mapas donde cada provincia tiene un color según su valor (más "
        "oscuro = más alto) y un mapa interactivo donde elegís qué variable mostrar: cuánto sube "
        "la temperatura, cuánto llueve o cuánto produce la economía.\n\n"
        "**Cómo se lee:** pasá el mouse sobre una provincia y aparece su valor exacto.\n\n"
        "**Para qué sirve:** ver de un vistazo dónde pasa cada cosa (por ejemplo si el "
        "calentamiento se concentra en una región), algo que una tabla no muestra."
    ),
    "correlaciones": (
        "**Qué es:** la página que intenta responder la pregunta central del proyecto: "
        "¿el clima tiene relación con cómo le va a la economía?\n\n"
        "**Qué vas a ver:** primero, si las provincias donde llueve cada vez menos crecieron "
        "menos económicamente. Después, si los años de sequía tuvieron menos crecimiento que "
        "los normales, tanto en el país como en las provincias.\n\n"
        "**Cómo se lee:** cada resultado trae el número y la conclusión en palabras. "
        "Encontrar una relación débil o inexistente también es una respuesta válida.\n\n"
        "**Ojo:** que dos cosas se muevan juntas no prueba que una cause la otra."
    ),
    "modelos": (
        "**Qué es:** una prueba más exigente. En vez de mirar si el clima y la economía se "
        "parecen, se le pide a un modelo (programa que aprende de los datos) que adivine "
        "cuánto crece la economía usando solo el clima.\n\n"
        "**Qué vas a ver:** el resultado para el país y para las 24 provincias, con qué tanto "
        "acierta y cuánto se equivoca, y qué variable usó más.\n\n"
        "**Cómo se lee:** se compara contra la respuesta más simple, adivinar siempre el "
        "promedio. Si el modelo no le gana, el clima solo no alcanza para predecir la economía.\n\n"
        "**Qué responde:** ¿sirve conocer el clima para anticipar la economía?"
    ),
    "escenarios": (
        "**Qué es:** una estimación de cuánto podría subir la temperatura de Argentina en el "
        "futuro, hacia 2050 y a fin de siglo.\n\n"
        "**Qué vas a ver:** tres escenarios. El A sigue el ritmo de toda la historia, el C sigue el "
        "ritmo de los últimos años (más rápido) y el B es una proyección de científicos "
        "internacionales (IPCC), que este proyecto solo cita.\n\n"
        "**Cómo se lee:** la banda sombreada alrededor de cada línea muestra la incertidumbre: "
        "cuanto más lejos en el futuro, más ancha, porque hay menos certeza.\n\n"
        "**Ojo:** son estimaciones, no predicciones seguras."
    ),
    "explorador": (
        "**Qué es:** una página para que hagas tus propias preguntas, sin depender de un análisis ya armado.\n\n"
        "**Qué vas a ver:** elegís una provincia y aparece su ficha (temperatura, lluvia, "
        "emisiones y economía), la comparación contra el país y un ranking.\n\n"
        "**Cómo se usa:** cambiá la provincia o la variable y los gráficos se rehacen al instante.\n\n"
        "**Para qué sirve:** revisar el caso puntual que te interese, por ejemplo tu provincia."
    ),
    "conclusiones": (
        "**Qué es:** el informe final del proyecto, escrito en texto.\n\n"
        "**Qué vas a ver:** los hallazgos principales, las limitaciones y lo que quedó "
        "pendiente, y al final un glosario con todos los términos técnicos explicados.\n\n"
        "**Para qué sirve:** es la respuesta corta si no querés recorrer el resto de las páginas. "
        "Se puede descargar en PDF."
    ),
    "checklist": (
        "**Qué es:** un control del proyecto: compara lo que se pidió al comienzo con lo que se hizo.\n\n"
        "**Qué vas a ver:** cada punto pedido, marcado como completo, parcial o pendiente, y en qué "
        "página del menú se puede ver.\n\n"
        "**Para qué sirve:** que quede claro qué está terminado y qué no, sin esconder nada."
    ),
}


def acordeon_pagina(clave: str) -> None:
    """Acordeón colapsado al tope de cada página: qué es, para qué sirve y
    por qué está — corto y preciso. Se usa una vez, después de st.header()."""
    with st.expander("❓ ¿Qué es esta página?"):
        st.markdown(PAGINAS[clave])


ETIQUETAS_VARIABLES = {
    "año": "Año",
    "tipo_jurisdiccion": "Tipo de jurisdicción",
    "pbg_preliminar": "¿PBG preliminar?",
    "anomalia_temperatura": "Anomalía de temperatura (°C)",
    "anomalia_precipitacion_pct": "Anomalía de precipitación (%)",
    "emisiones_gei_co2eq": "Emisiones de gases de efecto invernadero (MtCO₂eq)",
    "emisiones_co2_fosil": "Emisiones de CO₂ fósil (Mt)",
    "pbi_crecimiento_pct": "Crecimiento del PBI (%)",
    "pib_per_capita_crecimiento_pct": "Crecimiento del PBI per cápita (%)",
    "pib_per_capita": "PBI per cápita",
    "poblacion": "Población",
    "precipitaciones_mm": "Precipitación (mm)",
    "temperatura_media_c": "Temperatura media (°C)",
    "pbg": "Producto bruto geográfico (PBG)",
    "jurisdiccion": "Jurisdicción",
}

# Columnas de tablas de estadística: nombre visible y clave del glosario.
COLUMNAS_ESTADISTICAS = {
    "variable": ("Variable", None),
    "media": ("Promedio", "media"),
    "desvio_estandar": ("Variación típica (desvío)", "desvio"),
    "minimo": ("Mínimo", "minimo"),
    "maximo": ("Máximo", "maximo"),
    "pendiente": ("Tendencia por año", "pendiente"),
    "p_valor": ("p-valor", "p_valor"),
    "n_observaciones": ("Años con dato", "n_obs"),
    "observaciones": ("Observaciones", "observaciones"),
    "faltantes": ("Faltantes", "faltantes"),
    "primer_año": ("Primer año", None),
    "ultimo_año": ("Último año", None),
    "coeficiente": ("Coeficiente", "coeficiente"),
    "jurisdiccion": ("Provincia", None),
}


def tabla_legible(df):
    """Copia de `df` con los nombres de variable (en la columna 'variable')
    reemplazados por su etiqueta legible."""
    out = df.copy()
    if "variable" in out.columns:
        out["variable"] = out["variable"].map(lambda v: ETIQUETAS_VARIABLES.get(v, v))
    return out


def config_columnas(df) -> dict:
    """column_config con nombre en criollo y globo de ayuda para cada
    columna conocida de `df` (estadísticas y variables del dataset)."""
    cfg = {}
    for col in df.columns:
        if col in COLUMNAS_ESTADISTICAS:
            nombre, clave = COLUMNAS_ESTADISTICAS[col]
            cfg[col] = st.column_config.Column(nombre, help=GLOSARIO.get(clave) if clave else None)
        elif col in ETIQUETAS_VARIABLES:
            clave = f"v_{col}"
            cfg[col] = st.column_config.Column(
                ETIQUETAS_VARIABLES[col], help=GLOSARIO.get(clave)
            )
    return cfg


def para_que(texto: str) -> None:
    """Línea corta 'Para qué sirve' bajo el título de una sección."""
    st.markdown(f'<p class="explicacion-clima"><b>¿Para qué sirve?</b> {texto}</p>', unsafe_allow_html=True)


def etiqueta_variable(nombre: str) -> str:
    """Nombre legible para una variable técnica del dataset. Las variables
    dummy de provincia ('prov_X') se muestran como 'Provincia: X'."""
    if nombre.startswith("prov_"):
        return f"Provincia: {nombre[len('prov_'):]}"
    return ETIQUETAS_VARIABLES.get(nombre, nombre)


def ayuda(clave: str) -> str:
    """Devuelve la definición de GLOSARIO[clave], para usar en el parámetro
    `help=` nativo de Streamlit (st.metric, column_config, etc.) — ahí
    Streamlit ya dibuja el ícono con el globo de ayuda solo."""
    return GLOSARIO[clave]


def termino(texto_visible: str, clave: str) -> str:
    """Envuelve `texto_visible` en un tooltip nativo del navegador (aparece
    al pasar el mouse) con la definición de GLOSARIO[clave]. Para insertar
    DENTRO de un st.markdown(..., unsafe_allow_html=True)."""
    definicion = GLOSARIO[clave].replace('"', "&quot;")
    return (
        f'<abbr title="{definicion}" class="termino-clima">{texto_visible}</abbr>'
    )


def explicacion(texto: str) -> None:
    """Párrafo explicativo: tipografía en color e itálica, sin bloque de
    fondo de color. Reemplaza a st.info/success/warning/error para texto
    que explica (no alerta)."""
    st.markdown(f'<p class="explicacion-clima">{texto}</p>', unsafe_allow_html=True)


def num(valor: float, decimales: int = 1, signo: bool = False) -> str:
    """Número con coma decimal (formato argentino): num(-11.34) -> '\u221211,3'."""
    txt = f"{valor:+.{decimales}f}" if signo else f"{valor:.{decimales}f}"
    return txt.replace(".", ",").replace("-", "\u2212")


COLOR_ESTADO = {
    "Demostrado": "#3fa66b", "Señal moderada": "#d98b1f", "Señal débil": "#d98b1f", "No detectado": "#8a8f98",
}


def svg_linea(valores, color: str = "#5b8def") -> str:
    """Mini gráfico de línea (sparkline) con área suave y el último valor marcado."""
    v = [float(x) for x in valores]
    lo, hi = min(v), max(v)
    rango = (hi - lo) or 1.0
    ancho, alto, margen = 200.0, 44.0, 4.0
    pts = [
        (margen + i * (ancho - 2 * margen) / (len(v) - 1), alto - margen - (x - lo) / rango * (alto - 2 * margen))
        for i, x in enumerate(v)
    ]
    linea = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{pts[0][0]:.1f},{alto - margen:.1f} {linea} {pts[-1][0]:.1f},{alto - margen:.1f}"
    return (
        f'<svg class="kpi-svg" viewBox="0 0 {ancho:.0f} {alto:.0f}" preserveAspectRatio="none" role="img">'
        f'<polygon points="{area}" fill="{color}" fill-opacity="0.14"/>'
        f'<polyline points="{linea}" fill="none" stroke="{color}" stroke-width="1.8" vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="2.6" fill="{color}"/></svg>'
    )


def svg_rango(estimado: float, inf: float, sup: float, color: str = "#8a8f98", etiqueta: str = "rango probable") -> str:
    """Mini gráfico del efecto estimado (punto) con su rango probable (barra) respecto del cero (línea punteada)."""
    lim = max(abs(inf), abs(sup), abs(estimado)) * 1.2 or 1.0
    ancho, alto = 200.0, 30.0
    x = lambda val: (val + lim) / (2 * lim) * ancho  # noqa: E731
    cero = x(0.0)
    return (
        f'<svg class="kpi-svg kpi-svg-rango" viewBox="0 0 {ancho:.0f} {alto:.0f}" preserveAspectRatio="none" role="img">'
        f'<line x1="{cero:.1f}" x2="{cero:.1f}" y1="2" y2="{alto - 2:.0f}" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="2 2" vector-effect="non-scaling-stroke"/>'
        f'<line x1="{x(inf):.1f}" x2="{x(sup):.1f}" y1="{alto / 2:.0f}" y2="{alto / 2:.0f}" stroke="{color}" stroke-width="6" stroke-linecap="round" stroke-opacity="0.5" vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{x(estimado):.1f}" cy="{alto / 2:.0f}" r="4" fill="{color}"/></svg>'
        f'<div class="kpi-pie"><span>{num(inf, 1)}</span><span>{etiqueta}</span><span>{num(sup, 1)}</span></div>'
    )


COLOR_RESULTADO = {"Pasa": "#3fa66b", "Justo": "#d98b1f", "No pasa": "#d0533f", "Informativo": "#8a8f98", **COLOR_ESTADO}


def tabla_html(encabezados: list[str], filas: list[list], anchos: list[int] | None = None, col_estado: int | None = None,
               col_num: tuple = ()) -> None:
    """Tabla que ajusta el texto al ancho de la pantalla: sin scroll y sin datos cortados.
    `anchos` son proporciones por columna; `col_estado` pinta esa columna con el color del estado ("Pasa", "No pasa"...);
    `col_num` alinea columnas de cifras."""
    import html as _html

    cg = "".join(f'<col style="width:{a}%">' for a in anchos) if anchos else ""
    th = "".join(f"<th>{_html.escape(str(h))}</th>" for h in encabezados)
    cuerpo = []
    for fila in filas:
        celdas = []
        for i, v in enumerate(fila):
            txt = _html.escape(str(v))
            if col_estado is not None and i == col_estado:
                color = COLOR_RESULTADO.get(str(v), "")
                celdas.append(f'<td class="tabla-estado" style="color:{color}">{txt}</td>')
            elif i in col_num:
                celdas.append(f'<td class="tabla-num">{txt}</td>')
            else:
                celdas.append(f"<td>{txt}</td>")
        cuerpo.append("<tr>" + "".join(celdas) + "</tr>")
    st.markdown(
        f'<table class="tabla-clima"><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{"".join(cuerpo)}</tbody></table>',
        unsafe_allow_html=True,
    )


def claves(tengo: str, demuestro: str, como: str) -> None:
    """Tres tarjetas de igual tamaño: qué datos hay, qué se demuestra y cómo se demuestra."""
    import html as _html

    partes = "".join(
        f'<div class="clave"><div class="clave-titulo">{t}</div><div class="clave-texto">{_html.escape(x)}</div></div>'
        for t, x in [("Qué tengo", tengo), ("Qué demuestro", demuestro), ("Cómo lo demuestro", como)]
    )
    st.markdown(f'<div class="claves-grid">{partes}</div>', unsafe_allow_html=True)


def paneles(items: list[tuple[str, str]], minimo: int = 280) -> None:
    """Tarjetas de texto (título y párrafo) de igual tamaño, en una grilla."""
    import html as _html

    partes = "".join(
        f'<div class="panel-texto"><div class="panel-titulo">{_html.escape(t)}</div><div class="panel-cuerpo">{_html.escape(x)}</div></div>'
        for t, x in items
    )
    st.markdown(
        f'<div class="paneles-grid" style="grid-template-columns: repeat(auto-fit, minmax({minimo}px, 1fr));">{partes}</div>',
        unsafe_allow_html=True,
    )


def tarjetas(items: list[dict], minimo: int = 230) -> None:
    """Fila de tarjetas de indicador en una grilla: todas de la misma altura y sin texto cortado.
    Cada item: etiqueta, valor (corto), u (unidad en la misma línea, opcional), unidad (subtítulo), grafico (svg, opcional),
    desc (opcional), ayuda (opcional, se ve al pasar el mouse) y estado (opcional)."""
    import html as _html

    partes = []
    for it in items:
        estado = it.get("estado", "")
        color = COLOR_ESTADO.get(estado, "")
        acento = f"border-left: 3px solid {color};" if color else ""
        estado_html = f'<span class="kpi-estado" style="color:{color}"><i></i>{_html.escape(estado)}</span>' if estado and color else (
            f'<span class="kpi-estado">{_html.escape(estado)}</span>' if estado else "")
        ayuda_txt = _html.escape(it.get("ayuda", ""), quote=True)
        tip = f' title="{ayuda_txt}"' if ayuda_txt else ""
        u_html = f'<span class="kpi-u">{it["u"]}</span>' if it.get("u") else ""
        sub = f'<div class="kpi-sub">{it["unidad"]}</div>' if it.get("unidad") else ""
        graf = f'<div class="kpi-graf">{it["grafico"]}</div>' if it.get("grafico") else ""
        desc = f'<div class="kpi-desc">{it["desc"]}</div>' if it.get("desc") else ""
        partes.append(
            f'<div class="kpi"{tip} style="{acento}"><div class="kpi-top"><span class="kpi-etiqueta">{_html.escape(it["etiqueta"])}</span>{estado_html}</div>'
            f'<div class="kpi-valor"><span class="kpi-num">{it["valor"]}</span>{u_html}</div>{sub}{graf}{desc}</div>'
        )
    st.markdown(
        f'<div class="kpi-grid" style="grid-template-columns: repeat(auto-fit, minmax({minimo}px, 1fr));">{"".join(partes)}</div>',
        unsafe_allow_html=True,
    )


def inyectar_estilos() -> None:
    """Llamar una sola vez, en streamlit_app.py, antes de mostrar cualquier página."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ---------- Tipografía: una sola familia y una escala corta ---------- */
        .stApp { font-family: "Inter", "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif; }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
            font-family: inherit; letter-spacing: -0.012em; line-height: 1.25;
        }
        .stApp h2 { font-size: 1.6rem; font-weight: 700; }
        .stApp h3 { font-size: 1.2rem; font-weight: 600; }
        .stApp h4 { font-size: 1.02rem; font-weight: 600; }
        .stApp .stMarkdown p, .stApp .stMarkdown li { font-size: 0.95rem; line-height: 1.65; }
        .stApp [data-testid="stCaptionContainer"] { font-size: 0.82rem; line-height: 1.5; }

        /* ---------- Pestañas: nunca scroll horizontal ---------- */
        .stApp [data-baseweb="tab-list"] { flex-wrap: wrap; gap: 0.2rem 1.4rem; overflow: visible; }
        .stApp [data-baseweb="tab-list"] button { padding-left: 0; padding-right: 0; }
        .stApp [data-baseweb="tab-list"] button p { font-size: 0.92rem; font-weight: 500; white-space: nowrap; }

        /* ---------- Tarjetas de indicador ---------- */
        .kpi-grid { display: grid; gap: 1rem; margin: 0.6rem 0 1.4rem 0; align-items: stretch; }
        .kpi {
            border: 1px solid rgba(128, 128, 128, 0.25); border-radius: 12px; padding: 1.1rem 1.25rem 1.05rem 1.25rem;
            display: flex; flex-direction: column; min-width: 0; background: rgba(128, 128, 128, 0.045);
        }
        .kpi-top { display: flex; justify-content: space-between; align-items: baseline; gap: 0.75rem; min-height: 1.3rem; }
        .kpi-etiqueta { font-size: 0.74rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; opacity: 0.7; line-height: 1.3; }
        .kpi-estado { font-size: 0.72rem; font-weight: 600; white-space: nowrap; display: inline-flex; align-items: center; gap: 0.35rem; opacity: 0.95; }
        .kpi-estado i { width: 0.45rem; height: 0.45rem; border-radius: 50%; background: currentColor; display: inline-block; }
        .kpi-valor { margin-top: 0.7rem; display: flex; align-items: baseline; flex-wrap: wrap; gap: 0.4rem; }
        .kpi-num { font-size: 2.05rem; font-weight: 600; letter-spacing: -0.025em; line-height: 1.1; font-variant-numeric: tabular-nums; white-space: nowrap; }
        .kpi-u { font-size: 0.95rem; font-weight: 500; opacity: 0.7; }
        .kpi-sub { font-size: 0.84rem; opacity: 0.75; margin-top: 0.3rem; line-height: 1.4; }
        .kpi-graf { margin-top: 0.9rem; }
        .kpi-svg { width: 100%; height: 44px; display: block; color: inherit; }
        .kpi-svg-rango { height: 30px; }
        .kpi-pie { display: flex; justify-content: space-between; font-size: 0.68rem; opacity: 0.6; margin-top: 0.15rem; font-variant-numeric: tabular-nums; }
        .kpi-desc { font-size: 0.8rem; line-height: 1.5; opacity: 0.72; margin-top: auto; padding-top: 0.85rem; }

        /* ---------- Tablas que se ajustan al ancho ---------- */
        .tabla-clima { width: 100%; border-collapse: collapse; margin: 0.6rem 0 1.2rem 0; table-layout: fixed; }
        .tabla-clima th { text-align: left; font-size: 0.7rem; letter-spacing: 0.06em; text-transform: uppercase; opacity: 0.7; font-weight: 600;
                          padding: 0.55rem 0.8rem; border-bottom: 1px solid rgba(128, 128, 128, 0.45); }
        .tabla-clima td { padding: 0.75rem 0.8rem; vertical-align: top; font-size: 0.86rem; line-height: 1.55;
                          border-bottom: 1px solid rgba(128, 128, 128, 0.2); overflow-wrap: anywhere; }
        .tabla-clima td.tabla-num { font-variant-numeric: tabular-nums; }
        .tabla-clima td.tabla-estado { font-weight: 600; }

        /* ---------- Qué tengo / Qué demuestro / Cómo lo demuestro ---------- */
        .claves-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 0.6rem 0 1.3rem 0; align-items: stretch; }
        .clave { border: 1px solid rgba(128, 128, 128, 0.25); border-radius: 12px; padding: 1rem 1.15rem; background: rgba(128, 128, 128, 0.045); }
        .clave-titulo { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; opacity: 0.7; margin-bottom: 0.5rem; }
        .clave-texto { font-size: 0.88rem; line-height: 1.6; }

        /* ---------- Paneles de texto de igual tamaño ---------- */
        .paneles-grid { display: grid; gap: 1rem; margin: 0.6rem 0 1.3rem 0; align-items: stretch; }
        .panel-texto { border: 1px solid rgba(128, 128, 128, 0.25); border-radius: 12px; padding: 1.1rem 1.25rem; background: rgba(128, 128, 128, 0.045); }
        .panel-titulo { font-size: 1rem; font-weight: 600; letter-spacing: -0.01em; margin-bottom: 0.5rem; }
        .panel-cuerpo { font-size: 0.9rem; line-height: 1.6; opacity: 0.9; }

        /* ---------- Encabezado de la respuesta ---------- */
        .resp-eyebrow { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.09em; text-transform: uppercase; opacity: 0.65; margin: 0 0 0.4rem 0; }
        .resp-titulo { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.015em; line-height: 1.25; margin: 0 0 0.7rem 0; }
        .resp-lead { font-size: 1rem; line-height: 1.65; max-width: 62rem; margin: 0 0 1.3rem 0; opacity: 0.92; }
        .explicacion-clima {
            font-style: italic;
            font-size: 0.9rem;
            color: #2f6690;
            margin-top: 0.2rem;
            margin-bottom: 0.9rem;
            line-height: 1.5;
        }
        @media (prefers-color-scheme: dark) {
            .explicacion-clima { color: #7fb2dd; }
        }
        .termino-clima {
            text-decoration: underline dotted;
            text-underline-offset: 3px;
            cursor: help;
        }
        .hoja-informe {
            background: #ffffff;
            color: #1a1a1a;
            max-width: 210mm;
            margin: 1.5rem auto;
            padding: 18mm;
            border-radius: 4px;
            box-shadow: 0 2px 16px rgba(0, 0, 0, 0.22);
            border: 1px solid rgba(0, 0, 0, 0.08);
            font-family: Georgia, "Times New Roman", serif;
            line-height: 1.6;
        }
        .hoja-informe h1, .hoja-informe h2, .hoja-informe h3 {
            font-family: Georgia, "Times New Roman", serif;
            color: #1a1a1a;
        }
        .hoja-informe table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.75rem 0;
        }
        .hoja-informe th, .hoja-informe td {
            border: 1px solid #ccc;
            padding: 6px 10px;
            text-align: left;
        }
        @media (max-width: 900px) {
            .hoja-informe { padding: 6mm 5mm; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


GLOSARIO_FINAL = [
    "v_anomalia_temperatura", "v_anomalia_precipitacion_pct", "v_emisiones_gei_co2eq",
    "mtco2eq", "v_emisiones_co2_fosil", "v_pbi_crecimiento_pct", "pbi", "pbi_per_capita",
    "v_pib_per_capita_crecimiento_pct", "pbg", "anomalia", "estadistica_descriptiva",
    "media", "desvio", "minimo", "maximo", "serie_temporal", "media_movil", "z_score",
    "boxplot", "tendencias", "pendiente", "tendencia_decada", "pearson", "spearman",
    "p_valor", "ic95", "causalidad", "año_seco", "prueba_t", "regresion_lineal",
    "mapa_calor", "dispersion", "n_obs", "extrapolacion", "escenario_a", "escenario_c",
    "escenario_b", "ipcc", "reanalisis", "pp", "efectos_fijos", "gei", "residuo", "predictoras", "importancia",
    "coeficiente", "asociacion", "predecir_vs_observado",
    "random_forest", "dummy", "r2", "mae", "rmse", "cagr", "coropletico",
    "holm", "placebo", "dosis_respuesta", "permutacion", "rezago",
]


def glosario_markdown() -> str:
    """Glosario único para el final del informe: cada definición del
    GLOSARIO, en el orden de GLOSARIO_FINAL, como lista con el término en negrita."""
    lineas = ["## Glosario", "", "Definiciones en lenguaje simple de los términos usados en este informe.", ""]
    for clave in GLOSARIO_FINAL:
        termino_, _, resto = GLOSARIO[clave].partition(": ")
        lineas.append(f"- **{termino_}**: {resto}")
    return "\n".join(lineas)
