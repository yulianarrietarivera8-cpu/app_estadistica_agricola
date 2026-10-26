# App de Estadística Aplicada con Python y R — Ingeniería Agrícola (Unisucre)

**Estudiante:** Yuliana Arrieta Rivera
**Código:** 201252360
**Cultivo asignado:** Maíz · **Municipio:** Corozal · **Huella:** F795CCCA

## Descripción
App multipágina de Streamlit para explorar datos de parcelas y variables climáticas.

## Páginas
- **Inicio:** identificación del proyecto y descripción de la aplicación.
- **Datos:** tabla de parcelas, tipos de variables, datos faltantes y descarga del CSV.
- **EDA:** resúmenes estadísticos, distribuciones, relaciones entre variables y muestra
  de 10 parcelas para verificar cálculos manuales.
- **Regresión:** página en construcción.
- **Series de tiempo:** página en construcción con vista previa de la precipitación mensual.

## Cómo ejecutarla
Desde la raíz del repositorio, instala las dependencias y ejecuta Streamlit:

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py --server.headless true
```

En Codespaces, abre la pestaña **Puertos**, busca el puerto **8501** y selecciona
**Abrir en el navegador**.

## Hallazgos del EDA
(6–10 líneas escritas por ti, con cifras y unidades)
