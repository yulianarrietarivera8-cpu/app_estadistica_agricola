"""Análisis exploratorio univariado, cualitativo y bivariado."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from src.eda import atipicos_iqr, cargar_datos, resumen_numerico

st.set_page_config(page_title="Análisis exploratorio", page_icon="📊", layout="wide")

UNIDADES = {
    "dosis_N": "Dosis de nitrógeno (kg/ha)",
    "lamina_riego": "Lámina de riego (mm)",
    "materia_organica": "Materia orgánica (%)",
    "ph": "pH del suelo (sin unidad)",
    "rendimiento": "Rendimiento (t/ha)",
}


def titulo_variable(variable: str) -> str:
    """Devuelve el nombre de una variable junto con su unidad."""
    return UNIDADES.get(variable, variable)


def mostrar_histograma(datos: pd.Series, variable: str) -> None:
    """Dibuja el histograma y su estimación de densidad."""
    figura, eje = plt.subplots()
    sns.histplot(x=datos, kde=True, ax=eje, color="#2E7D32")
    eje.set_xlabel(titulo_variable(variable))
    eje.set_ylabel("Frecuencia (parcelas)")
    eje.set_title(f"Distribución de {titulo_variable(variable).lower()}")
    st.pyplot(figura)
    plt.close(figura)


def mostrar_caja(datos: pd.DataFrame, variable: str, eje_x: str | None = None) -> None:
    """Dibuja un diagrama de caja para una variable o grupo."""
    figura, eje = plt.subplots()
    sns.boxplot(data=datos, x=eje_x, y=variable, ax=eje, color="#81C784")
    eje.set_xlabel(eje_x.title() if eje_x else "")
    eje.set_ylabel(titulo_variable(variable))
    st.pyplot(figura)
    plt.close(figura)


# Los filtros se aplican a los análisis de parcelas de esta página.
parcelas = cargar_datos("parcelas.csv")
st.title("Análisis exploratorio de datos (EDA)")
with st.sidebar:
    st.header("Filtros de parcelas")
    suelos = st.multiselect(
        "Suelo",
        options=sorted(parcelas["suelo"].dropna().unique()),
        default=sorted(parcelas["suelo"].dropna().unique()),
    )
    riegos = st.multiselect(
        "Riego",
        options=sorted(parcelas["riego"].dropna().unique()),
        default=sorted(parcelas["riego"].dropna().unique()),
    )

filtradas = parcelas[parcelas["suelo"].isin(suelos) & parcelas["riego"].isin(riegos)]
if filtradas.empty:
    st.warning("No hay parcelas que coincidan con los filtros seleccionados.")

st.header("a) Análisis univariado")
variables_numericas = (
    filtradas.select_dtypes(include="number").columns.tolist()
    if not filtradas.empty
    else []
)
if variables_numericas:
    variable = st.selectbox(
        "Variable numérica",
        variables_numericas,
        format_func=titulo_variable,
    )
    st.dataframe(
        resumen_numerico(filtradas[variable]).rename("Valor").to_frame(),
        width="stretch",
    )
    col_histograma, col_caja = st.columns(2)
    with col_histograma:
        mostrar_histograma(filtradas[variable].dropna(), variable)
    with col_caja:
        mostrar_caja(filtradas, variable)

    resultado_atipicos = atipicos_iqr(filtradas[variable])
    st.subheader("Parcelas atípicas según las vallas de Tukey")
    st.caption(
        f"Valla inferior: {resultado_atipicos['límite_inferior']:.3f} · "
        f"Valla superior: {resultado_atipicos['límite_superior']:.3f}"
    )
    indices_atipicos = resultado_atipicos["atípicos"].index
    tabla_atipicos = filtradas.loc[indices_atipicos, ["parcela", variable]]
    if tabla_atipicos.empty:
        st.info("No se detectaron parcelas atípicas con el criterio de 1.5 × RIC.")
    else:
        st.dataframe(tabla_atipicos, width="stretch", hide_index=True)
else:
    st.info("Los filtros no dejan variables numéricas para resumir.")

st.header("b) Análisis cualitativo")
if filtradas.empty:
    st.info("No hay categorías para mostrar con los filtros seleccionados.")
else:
    for variable_cualitativa in ("suelo", "riego"):
        frecuencias = filtradas[variable_cualitativa].value_counts(dropna=False)
        relativas = filtradas[variable_cualitativa].value_counts(
            normalize=True, dropna=False
        )
        tabla_frecuencias = pd.DataFrame(
            {
                "Frecuencia absoluta": frecuencias,
                "Frecuencia relativa (%)": relativas.mul(100),
            }
        )
        st.subheader(f"Frecuencias de {variable_cualitativa}")
        st.dataframe(tabla_frecuencias, width="stretch")
        figura, eje = plt.subplots()
        sns.countplot(data=filtradas, x=variable_cualitativa, ax=eje, color="#4CAF50")
        eje.set_xlabel(variable_cualitativa.title())
        eje.set_ylabel("Frecuencia (parcelas)")
        eje.set_title(f"Parcelas por {variable_cualitativa}")
        st.pyplot(figura)
        plt.close(figura)

st.header("c) Análisis bivariado")
if not filtradas.empty:
    st.subheader("Rendimiento por tipo de suelo")
    mostrar_caja(filtradas, "rendimiento", "suelo")
    st.subheader("Rendimiento por tipo de riego")
    mostrar_caja(filtradas, "rendimiento", "riego")

    opciones_x = [col for col in variables_numericas if col != "rendimiento"]
    if opciones_x:
        variable_x = st.selectbox(
            "Variable X para comparar con el rendimiento",
            opciones_x,
            format_func=titulo_variable,
        )
        figura, eje = plt.subplots()
        sns.scatterplot(
            data=filtradas,
            x=variable_x,
            y="rendimiento",
            hue="riego",
            ax=eje,
        )
        eje.set_xlabel(titulo_variable(variable_x))
        eje.set_ylabel(titulo_variable("rendimiento"))
        eje.set_title("Relación entre la variable seleccionada y el rendimiento")
        st.pyplot(figura)
        plt.close(figura)

    st.subheader("Correlación de Pearson entre variables numéricas")
    correlaciones = filtradas.select_dtypes(include="number").corr(method="pearson")
    nombres_con_unidad = {
        variable: titulo_variable(variable) for variable in correlaciones.columns
    }
    correlaciones = correlaciones.rename(
        index=nombres_con_unidad, columns=nombres_con_unidad
    )
    figura, eje = plt.subplots(figsize=(9, 6))
    sns.heatmap(
        correlaciones,
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        ax=eje,
    )
    eje.set_title("Matriz de correlación de Pearson")
    st.pyplot(figura)
    plt.close(figura)

st.header("d) Muestra de 10 parcelas (verificación del cálculo a mano)")
muestra = cargar_datos("muestra10.csv")
st.dataframe(muestra, width="stretch", hide_index=True)
resumen_muestra = resumen_numerico(muestra["rendimiento"])
st.subheader("Resumen numérico del rendimiento")
st.dataframe(resumen_muestra.rename("Valor").to_frame(), width="stretch")

vallas_muestra = atipicos_iqr(muestra["rendimiento"])
st.subheader("Vallas de Tukey y parcelas atípicas")
st.write(
    f"Valla inferior: {vallas_muestra['límite_inferior']:.3f} t/ha · "
    f"Valla superior: {vallas_muestra['límite_superior']:.3f} t/ha"
)
atipicos_muestra = muestra.loc[
    vallas_muestra["atípicos"].index, ["parcela", "rendimiento"]
]
if atipicos_muestra.empty:
    st.info("No hay atípicos en esta muestra según el criterio de 1.5 × RIC.")
else:
    st.dataframe(atipicos_muestra, width="stretch", hide_index=True)

st.subheader("Rendimiento medio por tipo de riego")
st.dataframe(
    muestra.groupby("riego", as_index=False)["rendimiento"]
    .mean()
    .rename(columns={"rendimiento": "Rendimiento medio (t/ha)"}),
    width="stretch",
    hide_index=True,
)
