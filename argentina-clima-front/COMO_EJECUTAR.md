# Cómo ejecutar el front

## Dónde vive el entorno virtual

El entorno virtual **no** está dentro de esta carpeta, sino en
`C:\Users\tiago\.venvs\clima`.

**¿Por qué?** Cuando el proyecto estaba en una carpeta muy larga, Windows no
lograba cargar las DLL de `shapely` y `geopandas` (el error era
`ImportError: DLL load failed while importing lib: El nombre del archivo o la
extensión es demasiado largo.`). El entorno quedó en una ruta corta y no se movió
cuando la carpeta del proyecto se mudó. Todo lo demás (código, datos,
resultados) sí está en esta carpeta.

## Cada vez que quieras usar la app

Pegar esta línea **entera, una sola vez**, en PowerShell:

```powershell
cd "C:\Trabajo base cambio climatico\argentina-clima-front"; C:\Users\tiago\.venvs\clima\Scripts\python.exe -m streamlit run streamlit_app.py
```

Se abre solo en el navegador, en `http://localhost:8501`. Si no se abre solo,
copiar esa dirección en el navegador a mano.

No hace falta `activate`: se llama directo al intérprete del entorno.

## La primera vez en otra computadora

```powershell
python -m venv "C:\Users\tu_usuario\.venvs\clima"; C:\Users\tu_usuario\.venvs\clima\Scripts\python.exe -m pip install -r requirements.txt
```

La ruta del entorno tiene que ser **corta**, nunca dentro de la carpeta del
proyecto.

## ¿Hay que instalar `requirements.txt` cada vez?

**No.** Solo hace falta instalarlo:
- La primera vez que usás esta carpeta en una computadora, o
- Si borraste la carpeta del entorno, o
- Si `requirements.txt` cambió (por ejemplo, agregué una librería nueva).

El resto de las veces, **solo hay que correr la línea de arriba**.

## Para cerrarlo

Volver a la terminal donde quedó corriendo y presionar `Ctrl+C`.

## Problemas comunes

**"streamlit no se reconoce como un comando"** → usar siempre
`python -m streamlit run streamlit_app.py` (no `streamlit run ...` solo),
porque el comando corto a veces no queda en el PATH de Windows.

**"la carpeta .venv no existe"** → repetir los pasos de "La primera vez".

**El puerto 8501 ya está en uso** → cerrar la terminal anterior donde
haya quedado corriendo, o usar otro puerto:
```powershell
python -m streamlit run streamlit_app.py --server.port 8502
```
