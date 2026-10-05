# Cómo trabajar con Git y GitHub en equipo

Este documento explica cómo nos organizamos para trabajar en este proyecto usando Git y GitHub, de modo que **nadie pise el trabajo de otro**, el código no se rompa y siempre sepamos quién hizo cada cambio.

---

## 1. La regla de oro

> **Nadie hace cambios ni sube commits directamente a la rama `main`.**  
> La rama `main` es la versión oficial y estable: siempre tiene que funcionar y estar lista para mostrar o entregar.  
> **Todo trabajo nuevo se hace en una rama propia** y se incorpora a `main` únicamente mediante un **Pull Request (PR)** en GitHub.

---

## 2. Configuración inicial (una sola vez por máquina)

Si recién instalás Git o estás en una computadora nueva, asegurate de que Git sepa quién sos:

```powershell
git config --global user.name "Tu Nombre y Apellido"
git config --global user.email "tu_email@ejemplo.com"
```

---

## 3. El ciclo de trabajo diario (Paso a paso)

Cada vez que vayas a agregar una función, corregir un texto o retocar un gráfico, seguí estos pasos en orden:

### Paso 1: Actualizá tu `main` local
Antes de empezar a tocar código, asegurate de tener lo último que hayan subido tus compañeros:

```powershell
git checkout main
git pull origin main
```

### Paso 2: Creá una rama para tu tarea
Creá una rama nueva con un nombre que identifique quién sos y qué vas a hacer:

```powershell
git checkout -b tu-nombre/que-vas-a-hacer
```

**Ejemplos de buenos nombres de rama:**
- `lucas/analisis-provincial`
- `tiago/fix-grafico-lluvias`
- `sofia/estilos-front-kpis`
- `martin/actualizar-doc-metodologia`

> **Tip:** Con `git branch` podés ver en qué rama estás parado en cualquier momento (la que tiene el asterisco `*` en verde).

---

### Paso 3: Trabajá y probá tus cambios
Hacé los cambios que necesites en el código o en los documentos.  
Antes de commitear, **probá que la aplicación siga levantando bien**:

```powershell
# Probar que la app levanta sin errores
cd "C:\Trabajo base cambio climatico\argentina-clima-front"
C:\Users\tiago\.venvs\clima\Scripts\python.exe -m streamlit run streamlit_app.py
```
*(Si estás en otra máquina, usá la ruta de tu propio entorno virtual).*

---

### Paso 4: Guardá tus cambios en Git (Commit)
Revisá qué archivos modificaste:

```powershell
git status
```

Agregá los archivos modificados y creá el commit con un mensaje descriptivo en español:

```powershell
git add .
git commit -m "Ajustar escala del gráfico de precipitaciones provinciales"
```

> **Buenas prácticas para el mensaje de commit:**
> - Explicá **qué** hiciste (ej: `Corregir cálculo de anomalía`, `Sumar tabla a página 4`).
> - Evitá mensajes vacíos como `cambios`, `asdf` o `arreglos`.
> - Hacé commits chicos y frecuentes: es mucho más fácil rastrear un error en 3 commits chicos que en 1 commit gigante de 50 archivos.

---

### Paso 5: Subí tu rama a GitHub (Push)
La primera vez que subas tu rama a GitHub, corré:

```powershell
git push -u origin tu-nombre/que-vas-a-hacer
```
*(Las siguientes veces que hagas commits en esa misma rama, alcanza con poner simplemente `git push`).*

---

## 4. Integrar los cambios (Pull Request en GitHub)

Una vez que subiste tu rama, no la unís desde tu máquina: se hace en GitHub para que el resto del equipo pueda ver qué cambió.

1. **Abrí el repositorio en el navegador:**  
   [https://github.com/TiagoM395/Cambio-climatico-](https://github.com/TiagoM395/Cambio-climatico-)
2. Vas a ver un cartel amarillo arriba con tu rama y un botón que dice **"Compare & pull request"**. Hacé clic ahí.
3. **Escribí un título y descripción:**
   - Título claro (ej: *Actualización de gráficos en página 4*).
   - En la descripción contá brevemente qué tocaste y si hay algo que los demás tengan que probar.
4. Hacé clic en **"Create pull request"**.
5. **Revisión:** en la pestaña *"Files changed"*, cualquier compañero (o vos mismo) puede ver exactamente qué líneas se borraron (en rojo) y cuáles se agregaron (en verde).
6. Si todo está correcto y no hay conflictos, hacé clic en **"Merge pull request"** y después en **"Confirm merge"**.
7. Listo: los cambios de tu rama ahora forman parte oficial de `main`.

---

### Paso 6: Cerrar el ciclo en tu máquina
Una vez mergeado el Pull Request en GitHub:

1. Volvé a `main`:
   ```powershell
   git checkout main
   ```
2. Bajate el `main` actualizado con tu cambio ya incorporado:
   ```powershell
   git pull origin main
   ```
3. *(Opcional)* Borrá la rama local que ya terminaste para no acumular ramas viejas:
   ```powershell
   git branch -d tu-nombre/que-vas-a-hacer
   ```

---

## 5. Cómo evitar que nos pisemos (Conflictos)

Un **conflicto de merge** ocurre cuando dos personas editan las **mismas líneas del mismo archivo** al mismo tiempo. Git no puede adivinar cuál de las dos versiones es la correcta y pide que una persona elija.

### Reglas prácticas para prevenir conflictos:
1. **Dividirse las tareas:**  
   Si una persona está trabajando en `app_pages/3_nacional.py`, que otra trabaje en `app_pages/4_provincial.py` o en la documentación. Si tocan archivos distintos, Git los junta automáticamente sin ningún problema.
2. **Subir seguido:**  
   No te quedes con ramas de dos semanas sin subir. Cuanto más rápido se mergee una tarea chica, menos chances de cruzarse.
3. **Traer `main` a tu rama si la tarea es larga:**  
   Si estás trabajando en una rama hace varios días y viste que otros compañeros ya mergearon cosas a `main`, actualizá tu rama para no quedar desfasado:
   ```powershell
   git checkout tu-nombre/que-vas-a-hacer
   git fetch origin
   git merge origin/main
   ```

### ¿Qué hacer si aparece un conflicto?
Si al hacer merge Git te avisa que hay un conflicto:
1. Abrí el archivo en conflicto en VS Code.
2. Vas a ver marcas como estas:
   ```text
   <<<<<<< HEAD (lo que está en main)
   texto o código original
   =======
   texto o código que hiciste vos
   >>>>>>> tu-rama
   ```
3. VS Code te muestra botones arriba de esas líneas:  
   *Accept Current Change* (dejar lo que estaba), *Accept Incoming Change* (dejar lo tuyo), o *Accept Both* (dejar ambos).
4. Elegí la opción correcta (o editá el texto a mano para que quede prolijo), guardá el archivo, hacé `git add .`, `git commit -m "Resolver conflicto"` y subí con `git push`.

---

## 6. Particularidades importantes de este proyecto

- **Nunca subir entornos virtuales (`.venv`, `env`, etc.):**  
  El entorno virtual está fuera del repositorio por diseño (`C:\Users\tiago\.venvs\clima`). Nunca crees un entorno adentro de la carpeta del proyecto porque pesaría cientos de megabytes y rompería Git.
- **Cuidado con archivos pesados:**  
  Los shapefiles y datasets oficiales ya están en el repositorio. No agregues archivos pesados (de más de 50 MB) sin consultar antes.
- **La frontera entre Frontend y Backend (`data_front/`):**  
  El front no corre los scripts de procesamiento; lee directamente de `argentina-clima-front/data_front/`. Si alguien corre un script de backend que genera un nuevo `.csv` o figura en `argentina-clima-pbi/outputs/`, tiene que acordarse de copiar ese archivo a la carpeta equivalente de `argentina-clima-front/data_front/` y commitear ambos.
- **Saltos de línea en Windows (CRLF):**  
  Si al hacer `git add` ves un aviso que dice `warning: LF will be replaced by CRLF`, **es normal y no es un error**. Podés seguir adelante sin preocuparte.

---

## 7. Machete rápido de comandos frecuentes

| Qué querés hacer | Comando |
| :--- | :--- |
| Ver en qué rama estás y qué tocaste | `git status` |
| Ver todas las ramas locales | `git branch` |
| Actualizar tu rama `main` con lo de GitHub | `git checkout main` luego `git pull origin main` |
| Crear una rama nueva y moverte a ella | `git checkout -b mi-rama` |
| Cambiarte a una rama existente | `git checkout nombre-de-la-rama` |
| Guardar todos tus cambios | `git add .` luego `git commit -m "Mensaje claro"` |
| Subir tu rama a GitHub por primera vez | `git push -u origin mi-rama` |
| Subir cambios posteriores de esa rama | `git push` |
| Descartar cambios sin guardar de un archivo | `git restore nombre_archivo.py` |
