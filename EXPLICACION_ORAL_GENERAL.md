# Explicación oral general del trabajo

**Finalidad de este documento:** formaliza el guion de exposición oral del trabajo y el preparo de respuestas ante preguntas. Está redactado en registro académico: el texto en cursiva corresponde a lo que se enuncia durante la exposición, y lo que figura entre corchetes es una indicación de acción o de navegación en la aplicación.

**Datos del trabajo:** Cambio climático en Argentina y su relación con el crecimiento económico (PBI) · Matías Elías Campos y Tiago Maidana · Instituto 57, Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial, 2.º año, grupo 6 · Materia: Análisis y Exploración de Datos · Docente: Ibarra Martín · Fecha de entrega: 30/11/2026.

**Criterio de redacción:** los términos técnicos se enuncian con su significado inmediato, entre paréntesis, conforme al criterio empleado en el resto del trabajo. Toda cifra que se mencione durante la exposición debe figurar en el **cuadro de cifras clave** (sección 8); en caso de duda, se recurre a la tabla correspondiente y se lee el valor, sin enunciar cifras memorizadas.

---

## 1. Cómo utilizar este documento

| Tiempo disponible | Contenido a desarrollar |
|---|---|
| 5 minutos | Secciones 2, 3 y 4, con apoyo del cuadro de cifras (sección 8) |
| 10 minutos | Secciones 2 a 7 |
| 15 minutos, o con instancia de preguntas | Secciones 2 a 7 y luego la sección 9 |
| Con evaluador exigente | Secciones 2 a 7, más las secciones 9, 10 y 11 |

Estructura argumental del trabajo, expresada en una línea: **la pregunta formulada, la respuesta breve, el origen de los datos, la estrategia de análisis, los resultados obtenidos, los resultados no obtenidos y por qué la ausencia de un resultado también es un resultado.**

---

## 2. Apertura y presentación (30 segundos)

> *Buenos días. Nuestro trabajo se titula "Cambio climático en Argentina y su relación con el crecimiento económico". Se trata de un trabajo integrador de la materia de Análisis y Exploración de Datos, elaborado sobre datos reales provenientes de fuentes oficiales.*
>
> *La pregunta que orientó el trabajo es una: **¿el cambio climático afecta a la economía argentina?***
>
> *La respuesta breve, que sostiene la totalidad de la exposición, es la siguiente: **el clima de Argentina cambió de manera verificable y el calor reduce el rendimiento de los cultivos; ese efecto se diluye y no resulta detectable en el PBI total ni en el PBI per cápita del país.** Es decir, el efecto existe, puede medirse en el sector agropecuario y se pierde al observar la economía en su conjunto. Explicaré a qué se debe ello.*

[Abrir la página **Inicio** de la aplicación, que contiene el título, la ficha del trabajo y las seis etapas.]

---

## 3. La respuesta breve: siete resultados y su nivel de evidencia (1 minuto)

> *Expongo a continuación los siete resultados, cada uno asignado a un nivel de evidencia. Los desarrollo después.*
>
> **1. ¿Argentina se está calentando? Demostrado.** Así es: la temperatura aumenta 0,13 °C cada diez años, aproximadamente 0,86 °C en 64 años, con p menor a 0,001 (la p expresa la probabilidad de que el resultado sea producto del azar; un valor inferior a 0,001 equivale a menos de 1 posibilidad en 1.000).
>
> **2. ¿El calor reduce el rendimiento de los cultivos? Demostrado.** Reduce, y de magnitud considerable: maíz −11 %, trigo −13 % y soja −9 % de rendimiento por cada grado adicional de calor durante la temporada de cultivo. El girasol no registra efecto.
>
> **3. ¿El calor frena la producción del campo? Señal moderada.** El sector agropecuario crece 5,6 puntos porcentuales menos por cada grado adicional, con p = 0,026: 2,6 posibilidades en 100 de que el resultado sea casual. Constituye un indicio con respaldo, no una demostración.
>
> **4. ¿Los años secos frenan al campo? Señal débil.** Apuntan en el mismo sentido, con 3 puntos porcentuales menos de crecimiento, pero el valor p = 0,12 no permite afirmarlo.
>
> **5. ¿Se observa en la economía total de las provincias? No detectado.** No se distingue del azar: p = 0,17 para el calor y p = 0,77 para el año seco.
>
> **6. ¿Se observa en el PBI per cápita del país? No detectado.** La correlación entre temperatura y crecimiento por habitante es de −0,12, con p = 0,35; es decir, resulta prácticamente nula.
>
> **7. ¿La señal referida al campo resiste las pruebas de robustez? Señal moderada.** Superó 8 de 12 pruebas, si bien al aplicar la corrección de Holm el valor asciende a p = 0,16.
>
> *Los tres niveles de evidencia significan lo siguiente: **Demostrado**, resultado comprobado con solidez; **Señal**, los datos apuntan a una dirección con certeza insuficiente; **No detectado**, con estos datos el efecto no se distingue del azar. Conviene subrayar un principio que sostiene todo el trabajo: **un resultado nulo es un resultado.** La ausencia de detección no implica que el efecto no exista, sino que no resulta observable con la información disponible.*
>
> *Existe además una idea que atraviesa el trabajo: **que el efecto no se observe en el promedio nacional no invalida el problema, porque el sector agropecuario representa una proporción acotada de la economía y el resto de los sectores amortigua el impacto. Donde la agricultura tiene mayor peso, el daño es considerable.** Para una familia que vive de la cosecha, una variación del uno por ciento es significativa.*

[Navegar a la página **Respuesta a la pregunta**, pestañas *La pregunta* y *Veredicto*.]

---

## 4. Origen y documentación de los datos (1 minuto)

> *Se trabajó con trece fuentes: todas oficiales, todas descargadas directamente, sin datos construidos, estimados ni completados manualmente. Cada archivo cuenta con una huella SHA-256 —una firma digital del archivo— que permite verificar que no fue alterado.*
>
> *Las cinco fuentes que sostienen el análisis son las siguientes:*
>
> - *Temperatura y precipitación del país, del CIAM y del Servicio Meteorológico Nacional, entre 1961 y 2025.*
> - *Temperatura y precipitación por provincia, de NASA POWER, entre 1981 y 2025: 1.080 combinaciones de provincia y año.*
> - *Producción por sector y por provincia, de la CEPAL, entre 2004 y 2024: 1.350 registros.*
> - *Rendimiento por cultivo, provincia y departamento, del Ministerio de Economía: 160.499 registros, correspondientes a las campañas 1969/70 a 2024/25.*
> - *Crecimiento del PBI, del Banco Mundial, y población y PBI del Maddison Project, para el cálculo del PBI per cápita.*
>
> *Las dos tablas de trabajo resultantes son una nacional, de 65 registros, y una provincial, de 1.080. Aquí cabe señalar una decisión metodológica relevante: **los conjuntos de datos no se construyen, se descargan y se articulan por año y por provincia.** Cuando falta un dato, la celda queda vacía; no se completan valores.
>
> *Existen asimismo dos fuentes descargadas que aún no fueron utilizadas, lo cual informamos expresamente: la población por provincia del INDEC, que permitiría calcular el PBI per cápita provincial, y parte del mismo conjunto de datos agrícolas.*

[Navegar a las páginas **Fuentes de datos** y **Datos descargados**, que contienen la ficha de cada fuente con su dirección y su cantidad de registros.]

---

## 5. Estrategia de análisis: seis pasos (1 minuto 30)

> *La respuesta se construye en seis pasos. Cada uno responde a tres preguntas: qué datos se disponen, qué se demuestra y cómo se demuestra.*
>
> **Paso 1, ¿el clima se modificó efectivamente?** Se calcula la línea de tendencia de la temperatura nacional y provincial —la dirección hacia la que se mueven los datos, sin atender a las fluctuaciones anuales— y su p-valor. El resultado fue inferior a 0,001. El cambio climático en Argentina constituye un hecho medido.
>
> **Paso 2, ¿se observa en la economía del país?** Se calcula la correlación anual entre la anomalía de temperatura —el grado en que un año superó el promedio 1991-2020— y el crecimiento del PBI per cápita: r = −0,12, con p = 0,35. Complementariamente, una prueba t compara años secos contra años normales: 1,31 % frente a 1,37 %, con p = 0,97. Los valores son prácticamente idénticos. No se detecta efecto.
>
> **Paso 3, ¿se observa en el sector agropecuario?** En este nivel el efecto sí aparece. Se articularon los datos de producción por sector de las 24 provincias entre 2005 y 2023 —456 observaciones— con temperatura y precipitación. El método empleado es una regresión con efectos fijos: compara cada provincia consigo misma, por ejemplo un año cálido de Córdoba frente a uno normal de Córdoba, y descuenta lo ocurrido en el conjunto del país ese año, como una crisis o una pandemia. De este modo queda aislado el efecto del clima. El resultado indica que el calor resta 5,6 puntos de crecimiento al sector.
>
> **Paso 4, ¿el calor reduce el rendimiento de los cultivos?** Esta es la medida más directa del efecto, porque el rendimiento —kilogramos por hectárea— no depende de los precios ni de la superficie destinada a la siembra. Se emplea el clima correspondiente a la temporada de cultivo y no el del año calendario: para soja y maíz, de noviembre a marzo; para trigo, de julio a noviembre. Los resultados fueron −11,3 % para el maíz, −13,2 % para el trigo y −8,8 % para la soja, por grado.
>
> **Paso 5, ¿en qué jurisdicciones el impacto es mayor?** En 18 de las 24 provincias el sector agropecuario creció menos en los años secos. Las mayores contracciones se registraron en San Luis, con −26,6 puntos, San Juan, con −23,5, y Córdoba, con −23.
>
> **Paso 6, ¿la señal resiste las pruebas de robustez?** Se aplicaron doce pruebas de resistencia al resultado, que constituyen el requisito de un análisis riguroso. La señal superó ocho de ellas.*

[Navegar por las pestañas *1 · El clima* a *6 · Pruebas* de la página **Respuesta a la pregunta**.]

---

## 6. Resultados: lo demostrado, lo señalado y lo no detectado (1 minuto 30)

> *Deseo ser preciso respecto de los tres niveles de resultado, porque no poseen el mismo peso.*
>
> **Lo demostrado.** El calentamiento: 0,13 °C por década, con p inferior a 0,001. Y el efecto del calor sobre el rendimiento del maíz y del trigo: −11,3 % y −13,2 % por grado, con p inferior a 0,001 en ambos casos. Ninguno de los controles realizados desmiente estos hallazgos: el efecto persiste al excluir una provincia; desaparece al mezclar el clima de forma aleatoria; y se desvanece al sustituir el clima de la campaña correcta por el de la campaña siguiente, que es precisamente el comportamiento esperado en una prueba placebo.
>
> **Lo que constituye una señal.** El efecto del calor sobre el valor de la producción agropecuaria: 5,6 puntos, con p = 0,026. Resiste la mayoría de las pruebas, pero al aplicar la corrección de Holm —que endurece el criterio de significancia porque se evaluaron seis combinaciones y alguna resulta significativa por azar— el valor asciende a p = 0,16 y deja de ser significativo. Lo consignamos, en consecuencia, como lo que es: un indicio sólido, no una demostración. El resultado más contundente de esta sección corresponde a la prueba de dosis-respuesta: cada punto porcentual adicional de peso del sector agropecuario en la economía añade −0,43 puntos por grado, con p inferior a 0,001. El daño, por tanto, existe y se concentra donde la agricultura tiene mayor peso, que es justamente el comportamiento esperable si el efecto fuera real.
>
> **Lo que no se detectó, y la razón.** Ni en la economía total de las provincias ni en el PBI per cápita del país. Este punto resulta compatible con lo anterior: el sector agropecuario representa entre el 4 % y el 11 % de la economía en las ocho provincias más agropecuarias. Si el campo pierde 5,6 puntos y pesa un 8 %, el impacto sobre la economía total ronda los 0,4 puntos, cifra que no se distingue del ruido estadístico. El resto de los sectores amortigua el efecto. El promedio nacional oculta el impacto porque promedia realidades económicas muy distintas entre sí.
>
> *Merece señalarse una limitación que consignamos nosotros mismos: el resultado de la soja presenta una salvedad. Su prueba placebo no se cumple, por lo que parte del efecto atribuido podría deberse a otra causa. Se deja constancia de ello en lugar de omitirlo.*
>
> *Como referencia de orden de magnitud, y al solo efecto de dimensionar el fenómeno: un grado adicional de calor equivale, sobre la producción reciente, a unos 4,6 millones de toneladas de maíz y 3,1 millones de soja. El riesgo principal no reside en el promedio, sino en el año cálido.*

[Navegar a la pestaña *4 · Cultivos* (tabla de pruebas de control) y a la pestaña *3 · El campo* (tarjetas y gráfico de rangos).]

---

## 7. La aplicación y el cierre (1 minuto)

> *Todo lo expuesto se encuentra en una aplicación desarrollada en Streamlit, una herramienta de Python para interfaces de datos. Contiene trece páginas: las fuentes con su ficha y su huella digital, los datos descargados, el análisis nacional, el análisis provincial, los mapas, los modelos, los escenarios futuros, un explorador por provincia, las conclusiones con descarga en PDF y una verificación final que muestra la cobertura de las cuarenta secciones de la consigna.*
>
> *Una decisión de diseño que merece mención: la aplicación no recalcula nada. Lee copias de los resultados generados por los módulos de análisis. En consecuencia, si una cifra aparece en pantalla, proviene de una tabla generada por código y no de una transcripción manual. Todo el análisis es reproducible: se ejecuta mediante cinco comandos.*
>
> *Para concluir, la respuesta a nuestra pregunta es la siguiente: **sí, el cambio climático afecta a la economía argentina, aunque no por la vía que suele buscarse.** No se manifiesta en el PBI per cápita ni en el PBI total, sino en el rendimiento de los cultivos, que es donde la economía se expone de verdad, y se amplifica en las provincias donde la agricultura tiene mayor peso. Medir el promedio nacional implica medir el ámbito en el que el efecto se oculta.*
>
> *Para demostrar más, sería necesario contar con series más extensas por cultivo, con la población por provincia a fin de calcular el PBI per cápita provincial, con el registro de emergencias agropecuarias en lugar de la precipitación anual y con datos de empleo y exportaciones del sector. Con esa información, parte de lo que hoy clasificamos como señal alcanzaría el rango de demostración. Y si no fuera suficiente, también sería una respuesta válida: se informaría del mismo modo.*
>
> *Gracias por su atención. Quedamos a su disposición para las preguntas.*

[Dejar la aplicación abierta en la página **Respuesta a la pregunta**; si las preguntas se orientan a la metodología, en **Fuentes de datos**.]

---

## 8. Cuadro de cifras clave

**Calentamiento**

| Concepto | Valor |
|---|---|
| Argentina | +0,13 °C por década (0,0135 °C/año) |
| Acumulado en 64 años | +0,86 °C |
| Significancia | p = 1,5·10⁻⁹ (p < 0,001) |
| Año más cálido | 2023, +0,83 °C respecto de 1991-2020 |
| Jurisdicciones de mayor calentamiento | CABA +0,032 °C/año, Misiones +0,019, Corrientes y Chaco +0,015 |

**Rendimiento por grado de calor durante la temporada de cultivo**

| Cultivo | Efecto | p | Placebo | Provincias con el mismo signo |
|---|---|---|---|---|
| Maíz | −11,3 % (rango −16,0 a −6,6) | < 0,001 | 0,24 (cumple) | 15 de 15 |
| Trigo | −13,2 % | 0,0006 | 0,14 (cumple) | 11 de 12 |
| Soja | −8,8 % | 0,0002 | 0,0047 (no cumple) | 14 de 15 |
| Girasol | −1,3 % | 0,59 | 0,75 (cumple) | sin efecto |

**Sector agropecuario y economía**

| Concepto | Calor (+1 °C) | Año seco |
|---|---|---|
| Producción agropecuaria | −5,64 puntos, p = 0,026 | −2,98, p = 0,125 |
| Economía total de la provincia | −0,99, p = 0,174 | −0,18, p = 0,767 |
| PBI per cápita nacional | r = −0,12, p = 0,35 | r = −0,14, p = 0,27 |
| PBI per cápita, años secos frente a normales | — | 1,31 % frente a 1,37 %, p = 0,97 |

**Pruebas de robustez sobre la señal del campo (cumple 8 de 12)**

| Prueba | Resultado | Veredicto |
|---|---|---|
| Exclusión de una provincia | Se mantiene en 22 de 24; peor caso p = 0,057 | Justo |
| Exclusión de valores extremos | −3,96, p = 0,045 | Cumple |
| Permutación (2.000 mezclas) | p = 0,0035 | Cumple |
| Placebo: construcción, comercio, transporte, finanzas | p entre 0,11 y 0,69, sin efecto | Cumple |
| Alimentos y bebidas | −1,10, p = 0,031 | Cumple |
| Dosis-respuesta (peso del campo) | −0,43 puntos por °C, p < 0,001 | Cumple |
| Spearman sobre el orden de las provincias | −0,35, p = 0,093 | Justo |
| Solo años muy cálidos | −2,97, p = 0,064 | Justo |
| Efecto rezagado | p = 0,79; el efecto es del mismo año | Informativo |
| Corrección de Holm | p = 0,155 | No cumple |

**Modelos y proyecciones**

- Modelo nacional que predice el crecimiento económico a partir del clima: regresión lineal con R² = 0,21; Random Forest con R² = −0,13, es decir, sin capacidad predictiva. La precipitación concentra el 58 % de la importancia de variables.
- Modelo provincial conjunto: R² = −0,10, sin capacidad predictiva.
- Escenario A (serie histórica completa): +0,66 °C en 2050. Escenario C (últimos 15 años): +1,10 °C, no significativo. Escenario B (IPCC AR5, citado como referencia externa): +1,0 a +2,0 °C, hasta +3,5 °C en el NOA.

**Conjuntos de datos**

| Conjunto de datos | Registros |
|---|---|
| Rendimiento agrícola (MAGyP) | 160.499 |
| Clima mensual provincial (NASA POWER) | 12.384 |
| Emisiones de GEI (Secretaría de Ambiente) | 7.780 |
| Clima anual provincial (NASA POWER) | 1.080 |
| PBI, población y CO₂ (Maddison / OWID) | 175 |
| Población provincial (INDEC, descargada, sin utilizar) | 744 |
| PBG provincial por sector (CEPAL) | 1.350 |
| Clima nacional (CIAM / SMN) | 65 años |
| PBI per cápita nacional | 62 años (1961-2022) |

---

## 9. Preguntas del docente y respuestas

**"¿Demostraste que el cambio climático causa la caída del PBI?"**
No, y no lo afirmamos. Lo que hemos demostrado es una asociación estadística; para establecer causalidad se requieren estudios que excluyan explicaciones alternativas. Todo el trabajo está formulado en términos de asociación. Además, la relación con el PBI total no fue detectada: lo demostrado es el efecto sobre el rendimiento de los cultivos.

**"Si no se detecta en el PBI, ¿por qué el trabajo afirma que sí afecta a la economía?"**
Porque el promedio nacional oculta el efecto. El sector agropecuario representa entre el 4 % y el 11 % de la economía en las ocho provincias más agropecuarias, y los demás sectores amortiguan el impacto. A ello se suma que el rendimiento por hectárea constituye una medida directa, independiente de los precios y de la superficie sembrada, y en ese nivel el efecto es claro y sólido.

**"¿Qué diferencia hay entre 'demostrado' y 'señal'?"**
Es el nivel de evidencia que se asigna al resultado según su significancia y su resistencia a las pruebas de control. "Demostrado" corresponde a p inferior a 0,001 con controles que se cumplen. "Señal" indica que el resultado apunta en la dirección esperada sin alcanzar el criterio, y que resiste parcialmente las pruebas de robustez. "No detectado" significa que no se distingue del azar. En la aplicación estos tres niveles se distinguen por color precisamente para que la diferencia resulte visible.

**"¿Por qué se utilizó regresión con efectos fijos y no una correlación simple?"**
Porque una correlación simple compara una provincia con otra, y las provincias difieren entre sí por riqueza, tamaño y estructura productiva. Los efectos fijos comparan cada provincia consigo misma y descuentan lo ocurrido en el país en cada año, de modo que lo que queda es el efecto del clima y no las diferencias estructurales entre jurisdicciones.

**"¿Qué ocurre si se mezclan las temperaturas de forma aleatoria?"**
El efecto desaparece: en 2.000 mezclas aleatorias, el azar reprodujo el efecto real en solo 6 casos, p = 0,0035. Esto descarta que el resultado sea un artefacto del método.

**"¿Qué es una prueba placebo?"**
Es repetir el análisis allí donde no debería observarse efecto. Si el calor restringe efectivamente la actividad agropecuaria, no debería restringir la construcción, el comercio ni las finanzas. Y no lo hace: los valores p se sitúan entre 0,11 y 0,69. La soja constituye la excepción, y por ello su resultado es menos firme: el placebo con el clima de la campaña siguiente arroja p = 0,0047, lo que indica que parte de ese efecto podría deberse a otra causa.

**"¿Por qué no se utilizaron los 160.000 registros agrícolas descargados?"**
Sí se utilizaron: corresponden a 1.987 observaciones de rendimiento de soja, maíz, trigo y girasol por provincia y campaña, tras filtrar las provincias con menos de 2.000 hectáreas y menos de 15 años de datos, a efectos de asegurar comparabilidad entre las estimaciones. Los 160.499 registros corresponden al archivo crudo de estimaciones agrícolas.

**"¿Qué ocurre si se utiliza el año completo en lugar de la temporada de cultivo?"**
El efecto se diluye, porque lo pertinente para el cultivo es el clima de su temporada y no el del año calendario. Por esa razón el paso 4 emplea el clima de los meses correspondientes a la temporada de cultivo, que es lo metodológicamente correcto.

**"¿La regresión no demuestra causalidad?"**
No se afirma causalidad. Que dos variables se muevan conjuntamente no prueba que una cause a la otra. Así consta en el informe y en la aplicación.

**"¿Qué es la corrección de Holm?"**
Es un ajuste estadístico que endurece el criterio de significancia cuando se realizan múltiples pruebas en simultáneo. Si se evalúan seis combinaciones, alguna resulta significativa por puro azar. El ajuste corrige esa distorsión. En nuestro caso, es lo que hace que una señal que aparecía con p = 0,026 pase a p = 0,16. Se reporta igualmente.

**"¿Qué aspecto mejoraría del trabajo?"**
Utilizar la población provincial, ya descargada, para calcular el PBI per cápita provincial; disponer de series más extensas por cultivo; emplear el registro de emergencias agropecuarias en lugar de la precipitación anual como variable de evento extremo; e incorporar empleo y exportaciones del sector. Todo ello consta en el documento de pendientes del proyecto.

**"¿Los modelos predicen adecuadamente?"**
No. El modelo lineal nacional presenta R² = 0,21, un valor bajo, y el Random Forest obtiene R² negativo, es decir, peor que predecir el promedio histórico. Esto también es un resultado: el clima por sí solo no predice el crecimiento económico. Por ello la variable dependiente del modelo es el crecimiento económico en función del clima, y no a la inversa, que es lo que requería la consigna original.

---

## 10. Advertencias sobre lo que no debe afirmarse

- **No afirmar que el cambio climático causa la caída del PBI.** El trabajo demuestra asociación, y con el PBI total no se detecta efecto alguno.
- **No afirmar que no existe impacto económico.** Lo que no se detecta es el efecto sobre el promedio; el efecto sobre el sector agropecuario sí está documentado.
- **No presentar la soja como resultado firme sin la salvedad correspondiente.** La prueba placebo no se cumple, y sin esa precisión la objeción invalida el trabajo en la primera pregunta.
- **No calificar de "demostrado" el resultado sobre el valor de la producción del campo (−5,6 puntos).** Constituye una señal: no supera la corrección de Holm.
- **No enunciar cifras que no figuren en el cuadro de la sección 8.** En caso de no recordar un valor, se recurre a la tabla y se lee.
- **No emplear lenguaje causal en ningún resultado.** "El calor frena la producción" es admisible; "el calor causa que la producción se frene", no.
- **No afirmar que el PBI per cápita provincial no existe como dato.** No fue posible calcularlo con las fuentes utilizadas; la población provincial se encuentra descargada, pero aún no analizada.

---

## 11. Glosario de apoyo

| Término | Formulación breve para la exposición |
|---|---|
| Anomalía de temperatura | Grado en que un año superó el promedio del período 1991-2020. |
| Tendencia | Dirección hacia la que se mueven los datos a lo largo de los años, sin atender a las fluctuaciones anuales. |
| p-valor | Probabilidad de que el resultado sea producto del azar; se expresa como posibilidades en 100. |
| Correlación | Número entre −1 y +1 que indica si dos variables se mueven conjuntamente; cercano a 0 indica ausencia de relación. |
| Regresión con efectos fijos | Comparación de cada provincia consigo misma, descontando lo ocurrido en el conjunto del país cada año. |
| Temporada de cultivo | Mesos en los que el cultivo se desarrolla; no el año calendario. |
| Rendimiento | Kilogramos por hectárea; independiente de los precios y de la superficie sembrada. |
| Placebo | Repetición del análisis donde no debería haber efecto, a fin de verificar que el método no genera señales espurias. |
| Permutación | Mezcla aleatoria y repetida de los datos, para comprobar con qué frecuencia el azar reproduce el resultado. |
| Dosis-respuesta | Si el clima causa el daño, este debe ser mayor donde el sector expuesto tiene mayor peso. |
| Holm | Corrección que endurece el criterio de significancia por haberse evaluado múltiples combinaciones. |
| Año seco | Definición estadística adoptada en este trabajo: el 25 % de los años con menor precipitación de la propia serie. No equivale a una sequía oficial. |
| Sectores no expuestos | Construcción, comercio, transporte y finanzas: actividades que no dependen del clima. |
| R² | Proporción de la variación de la variable explicada por el modelo; un valor negativo indica desempeño inferior al de predecir el promedio. |
| Variable dummy | Variable que vale 1 para una provincia y 0 para las restantes, a fin de permitir comparaciones internas. |
| SHA-256 | Firma digital del archivo, que permite verificar la integridad de los datos. |
| PBG | Producto bruto geográfico: equivalente del PBI para una provincia. |
| Robustez | Capacidad de un resultado de conservarse al modificar el método o los datos utilizados. |

---

## 12. Frase de cierre

> *"El promedio nacional no es el ámbito donde el clima se hace visible. Se hace visible en la cosecha."*

*En caso de que solo pueda formularse una afirmación, corresponde a esta.*
