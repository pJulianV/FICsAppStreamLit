import streamlit as st
import pandas as pd

df = pd.DataFrame({'Nombre': ['Juan', 'Maria', 'Pedro', 'Luis', 'Ana'],  
                   'Apellido': ['Gomez','Perez','Lopez','Gomez','Sanchez']})

df = st.data_editor(df)
nombre_filtro = st.multiselect(
    'Seleccione nombres:',
    df['Nombre'].unique())

apellido_filtro = st.multiselect(
    'Seleccione apellidos repetidos:',
    df['Apellido'].unique())

df_filtrado = df[df['Nombre'].isin(nombre_filtro) &
                df['Apellido'].isin(apellido_filtro)] 

st.dataframe(df_filtrado)
