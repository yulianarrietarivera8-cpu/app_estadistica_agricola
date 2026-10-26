"""Vista previa de la serie mensual de precipitación."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.eda import cargar_datos

st.set_page_config(page_title="Series de tiempo", page_icon="🌧️", layout="wide")

st.title("Series de tiempo")
st.info("Esta página está en construcción.")
st.write("En las próximas versiones se estudiarán los siguientes temas:")
st.markdown(
    """
- Componentes de una serie temporal
- Descomposición
- Promedios móviles
- Pronóstico
"""
)

# La fecha se convierte a formato temporal para conservar el orden mensual del registro.
clima = cargar_datos("clima_mensual.csv")
clima["fecha"] = pd.to_datetime(clima["fecha"])
st.subheader("Vista previa: precipitación mensual")
figura, eje = plt.subplots(figsize=(10, 4))
eje.plot(clima["fecha"], clima["precipitacion_mm"], color="#1976D2")
eje.set_xlabel("Fecha")
eje.set_ylabel("Precipitación (mm)")
eje.set_title("Precipitación mensual, 2015–2025")
eje.grid(alpha=0.25)
figura.autofmt_xdate()
st.pyplot(figura)
plt.close(figura)
