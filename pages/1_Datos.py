"""Descripción y descarga de los datos de parcelas."""

import pandas as pd
import streamlit as st

from src.eda import cargar_datos, valores_faltantes

st.set_page_config(page_title="Datos de parcelas", page_icon="📋", layout="wide")

# La tabla permite inspeccionar cada registro antes de realizar el análisis.
parcelas = cargar_datos("parcelas.csv")
st.title("Datos de parcelas")
st.write("Cada fila corresponde a una parcela observada.")
st.write(f"**Número de filas:** {parcelas.shape[0]}  ·  **Número de columnas:** {parcelas.shape[1]}")
st.dataframe(parcelas, width="stretch", hide_index=True)

# Las variables de texto son cualitativas; las variables numéricas son cuantitativas.
tipos = pd.DataFrame(
    {
        "Variable": parcelas.columns,
        "Tipo de dato": [
            "Cualitativa" if not pd.api.types.is_numeric_dtype(parcelas[col])
            else "Cuantitativa"
            for col in parcelas.columns
        ],
    }
)
st.subheader("Tipo de cada variable")
st.dataframe(tipos, width="stretch", hide_index=True)

st.subheader("Valores faltantes")
st.dataframe(
    valores_faltantes(parcelas).rename_axis("Variable").reset_index(),
    width="stretch",
    hide_index=True,
)

# Se descarga el mismo archivo que alimenta los análisis, sin modificarlo.
st.download_button(
    "Descargar parcelas.csv",
    data=parcelas.to_csv(index=False).encode("utf-8"),
    file_name="parcelas.csv",
    mime="text/csv",
)
