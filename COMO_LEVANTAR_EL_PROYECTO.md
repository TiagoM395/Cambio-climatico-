# Cómo levantar el proyecto

## Dónde está el entorno

El entorno virtual **no** está dentro de la carpeta del proyecto, sino en:

```
C:\Users\tiago\.venvs\clima
```

**¿Por qué?** Cuando el proyecto estaba en una carpeta muy larga, Windows no
podía cargar las DLL de las librerías (shapely, geopandas) a más de 260
caracteres de distancia. El error que salía era
`ImportError: DLL load failed while importing lib: El nombre del archivo o la
extensión es demasiado largo.` El entorno quedó en una ruta corta y no se movió
cuando la carpeta del proyecto se mudó a `C:\Trabajo base cambio climatico`.

Todo lo demás (código, datos, resultados) sí está en la carpeta del proyecto.

---

## Las próximas veces (ya está todo instalado)

**1. Abrí una terminal** (PowerShell o Windows Terminal).

**2. Pegá esto — una sola línea, todo junto:**

```
cd "C:\Trabajo base cambio climatico\argentina-clima-front"; C:\Users\tiago\.venvs\clima\Scripts\python.exe -m streamlit run streamlit_app.py
```

**3. Apretá Enter.** Se abre solo el navegador en `http://localhost:8501`.

Para cerrarlo: `Ctrl` + `C` en esa misma ventana.

> No hace falta activar el entorno con `activate`: se llama directo al
> intérprete de `C:\Users\tiago\.venvs\clima`.

---

## La primera vez en otra máquina

Abrí PowerShell y pegá esta línea **una sola vez** (tarda varios minutos):

```
cd "C:\ruta\de\la\carpeta\argentina-clima-front"; python -m venv "C:\ruta\corta\clima"; C:\ruta\corta\clima\Scripts\python.exe -m pip install -r requirements.txt
```

Donde `C:\ruta\corta\clima` tiene que ser una ruta **corta** (por ejemplo
`C:\Users\tu_usuario\.venvs\clima`), nunca dentro de la carpeta del proyecto.

---

## Importante

- No escribas nunca una línea que empiece con `PS C:\` — eso no es un
  comando, es lo que la terminal muestra sola.
- Si la aplicación ya estaba abierta, cerrala con `Ctrl` + `C` y volvé a
  levantarla para ver los cambios.
- Si querés la dirección de red para abrirla desde el celular, Streamlit la
  muestra al arrancar (`Network URL`).
- Si algo falla, pasame el mensaje de error completo, tal cual aparece.

---

**Dónde está la respuesta a la pregunta principal:** en la aplicación, menú
**Respuesta a la pregunta**. Explicada por escrito (qué datos hay, qué se
demuestra y cómo) en `LA_PREGUNTA_Y_LA_RESPUESTA.md`, en esta misma carpeta.
