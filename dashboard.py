import streamlit as st
import pandas as pd

df = pd.read_csv("./datasets/Internet_Penetracion.csv")

df["Accesos por cada 100 hogares"] = df["Accesos por cada 100 hogares"].str.replace(',','.')
df["Accesos por cada 100 hogares"] = pd.to_numeric(df["Accesos por cada 100 hogares"])
df["variacion_trimestral"] = (df["Accesos por cada 100 hogares"] - df["Accesos por cada 100 hogares"].shift(2)) / df["Accesos por cada 100 hogares"].shift(2)


df_agrupado = df.groupby("Año")["variacion_trimestral"].mean()

df["Año-Tri"] = df['Año'].astype(str).str.cat(df['Trimestre'].astype(str), sep='-')
internet_penetracion_acceso_hogares = df[["Año-Tri", "Accesos por cada 100 hogares"]].groupby("Año-Tri").mean()
# internet_penetracion_acceso_hogares.set_index("Año-Tri", inplace=True)

st.title("""
    Acceso a internet por cada 100 hogares
""")

st.line_chart(data=internet_penetracion_acceso_hogares)


st.title("""Variación porcentual trimestral de los accesos a Internet por cada 100 hogares""")


st.line_chart(data=df_agrupado)


filtro_anio = st.slider("Selecciona el rango de años:", int(df_agrupado.index.get_level_values(0).min()), int(df_agrupado.index.get_level_values(0).max()))

df_filtrado = df_agrupado[df_agrupado.index.get_level_values(0).isin(range(filtro_anio, filtro_anio + 1))]
st.line_chart(df_filtrado)

st.table(df_filtrado)

df_filtrado_porcentaje = df_filtrado.pct_change()

st.bar_chart(df_filtrado_porcentaje)

st.markdown("## Conclusiones")

