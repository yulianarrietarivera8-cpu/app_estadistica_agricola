"""Página de inicio de la app multipágina de estadística agrícola."""

import streamlit as st

from src.eda import cargar_metadatos

st.set_page_config(
    page_title="Estadística Agrícola | Inicio",
    page_icon="🌱",
    layout="wide",
)

# La portada presenta la identidad del proyecto y orienta el recorrido por páginas.
metadatos = cargar_metadatos()
st.title("Estadística Aplicada con Python y R — Ingeniería Agrícola, Unisucre")
st.write(
    "Aplicación didáctica para organizar, resumir y visualizar datos de parcelas "
    "agrícolas y variables climáticas."
)

st.subheader("Datos del proyecto")
col_nombre, col_codigo, col_cultivo = st.columns(3)
col_nombre.metric("Nombre", str(metadatos["nombre"]))
col_codigo.metric("Código", str(metadatos["codigo"]))
col_cultivo.metric("Cultivo", str(metadatos["cultivo"]))

col_municipio, col_huella, col_parcelas = st.columns(3)
col_municipio.metric("Municipio", str(metadatos["municipio"]))
col_huella.metric("Huella", str(metadatos["huella"]))
col_parcelas.metric("Parcelas", str(metadatos["n_parcelas"]))

st.subheader("Recorrido por la aplicación")
st.markdown(
    """
- **Datos:** consulta la tabla de parcelas, los tipos de variables y los datos faltantes.
- **EDA:** explora distribuciones, categorías, relaciones entre variables y una muestra
  de 10 parcelas para verificar cálculos manuales.
- **Regresión:** próximamente incluirá modelos lineales y diagnóstico.
- **Series de tiempo:** próximamente explorará la precipitación mensual y su pronóstico.
"""
)
