"""Funciones reutilizables para explorar datos de parcelas agrícolas."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

RUTA_DATOS = Path(__file__).resolve().parent.parent / "datos"


@st.cache_data
def cargar_datos(nombre_csv: str) -> pd.DataFrame:
    """Carga un CSV ubicado en la carpeta datos y almacena el resultado en caché."""
    ruta = RUTA_DATOS / nombre_csv
    return pd.read_csv(ruta)


def cargar_metadatos() -> dict[str, object]:
    """Lee y devuelve los metadatos de identificación del proyecto."""
    ruta = RUTA_DATOS / "metadatos.json"
    with ruta.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def resumen_numerico(serie: pd.Series) -> pd.Series:
    """Calcula estadísticos descriptivos, ignorando datos faltantes."""
    datos = serie.dropna()
    media = datos.mean()
    desviacion = datos.std(ddof=1)

    return pd.Series(
        {
            "n": datos.count(),
            "Media": media,
            "Mediana": datos.median(),
            "Desviación estándar muestral": desviacion,
            "CV (%)": (desviacion / abs(media) * 100) if media != 0 else float("nan"),
            "Mínimo": datos.min(),
            "Q1": datos.quantile(0.25),
            "Q3": datos.quantile(0.75),
            "Máximo": datos.max(),
            "RIC": datos.quantile(0.75) - datos.quantile(0.25),
            "Asimetría": datos.skew(),
        }
    )


def valores_faltantes(df: pd.DataFrame) -> pd.DataFrame:
    """Resume la cantidad y el porcentaje de valores faltantes por variable."""
    faltantes = df.isna().sum()
    return pd.DataFrame(
        {
            "Valores faltantes": faltantes,
            "Porcentaje (%)": faltantes.div(len(df)).mul(100) if len(df) else 0.0,
        }
    )


def atipicos_iqr(serie: pd.Series) -> dict[str, object]:
    """Calcula las vallas de Tukey y devuelve las observaciones atípicas."""
    datos = serie.dropna()
    q1 = datos.quantile(0.25)
    q3 = datos.quantile(0.75)
    ric = q3 - q1
    limite_inferior = q1 - 1.5 * ric
    limite_superior = q3 + 1.5 * ric
    atipicos = datos[(datos < limite_inferior) | (datos > limite_superior)]
    return {
        "Q1": q1,
        "Q3": q3,
        "RIC": ric,
        "límite_inferior": limite_inferior,
        "límite_superior": limite_superior,
        "atípicos": atipicos,
    }
