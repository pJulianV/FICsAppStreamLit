# ! Las dependencia, rutas y codigos que se usan en la terminal de anaconda

# cd OneDrive - Grupo Bancolombia\Workspace\PruebaStreamLit
# cd Workspace\FIC StreamLit


# pip install -r requirements.txt

# pip install ______ -i https://artifactory.apps.bancolombia.com/api/pypi/python-org/simple --trusted-host artifactory.apps.bancolombia.com
# pip install -r requirements.txt -i https://artifactory.apps.bancolombia.com/api/pypi/python-org/simple --trusted-host artifactory.apps.bancolombia.com




# streamlit run streamlit_app.py

# ! Los Dataframe con terminacion "NoDupl" es para la visualizacion NO USAR en el excel final


import pandas as pd
from io import BytesIO
# from pyxlsb import open_workbook as open_xlsb

from xlsxwriter import Workbook
import streamlit as st

# import plotly.express as px
from PIL import Image


from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)



st.set_page_config(
    page_title="FICs App",
    page_icon="img/LogoBancolombiaNegro.png",
    # layout="wide",
    initial_sidebar_state="expanded",

)


customized_button = st.markdown("""
    <style >
    # .stDownloadButton, div.stButton {text-align:center}
    .stDownloadButton button, div.stButton > button:first-child {
        background-color: #ff4b4b;
        color:#ffffff;
        padding-left: 20px;
        padding-right: 20px;
        transition: opacity 0.5s ease-in-out;
    }
    
    .css-1n543e5:focus:not(:active) {
    border-color: rgb(255, 75, 75);
    color: #ffffff;
    }

    .stDownloadButton button:hover, div.stButton > button:hover {
        font-size: 2.5rem;
        background-color: #ffffff;
        color: #ff4b4b;
        border-color: #ff4b4b;
    }
    .stDownloadButton button:focus:not(:active) {
        background-color: #ffffff;
        color: #ff4b4b;
        border-color: #ff4b4b;
    }
    .stDownloadButton button:visited {
        background-color: #ff4b4b;
        color: #ffffff;
        border-color: #ff4b4b;
    }
        }
    </style>""", unsafe_allow_html=True)



empty_left, contents, empty_right = st.columns([0.55, 3, 0.1])

with contents:
    st.header("Explora Fondos a tu Medida 📈")
    
st.text(" ")


img = Image.open("img/investment3.jpeg")
st.image(img, use_column_width=True)


excel_file = "InformeFICsAbril2023.xlsx"
sheet_name = "Hoja1"

df = pd.read_excel(excel_file,
                   sheet_name= sheet_name,
                   header=0
                   )

dfNoDupl= df.drop_duplicates(subset=["Nombre Negocio"], keep='first')

dfTiposFondos = pd.read_excel("TiposFondos.xlsx",
                           sheet_name= "Hoja1",
                           header= 0)

dfTiposFondosNoDupl = dfTiposFondos.drop_duplicates(subset=["Nombre Negocio"], keep='first')


# ! Emparejar fondo con su tipo:

df = df.assign(ASSET_CLASS= "" )

nombreFondos70 = df["Nombre Negocio"].unique().tolist()

nombresDBTiposFondos = dfTiposFondos["Nombre Negocio"].unique().tolist()


listaTiposFondos = dfTiposFondos["ASSET_CLASS.ASSET CLASS"].unique().tolist()


diccionarioTiposFondos = dict(zip(dfTiposFondosNoDupl['Nombre Negocio'],
                                  dfTiposFondosNoDupl['ASSET_CLASS.ASSET CLASS']
                                  ))



rowCountdf = df.shape[0]

for i in range(rowCountdf):


    nombreFondo = df["Nombre Negocio"][i]
    
    if nombreFondo in diccionarioTiposFondos:
    
        tipoFondo= diccionarioTiposFondos[nombreFondo]
        df.at[i, 'ASSET_CLASS'] = tipoFondo
    else:
        df.at[i, 'ASSET_CLASS'] = "INDEFINIDO"





st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")

empty_left, contents, empty_right = st.columns([0.65, 3, 0.1])

with contents:
    st.subheader("Descargue nuestros :red[_fondos sugeridos_]")

st.text(" ")


col1, col2, col3 = st.columns([1.2, 2, 0.1])


with col2:
    with open(excel_file, 'rb') as my_file:
        st.download_button(label = 'Descargar Sugeridos', data = my_file, file_name = 'FondosSugeridos.xlsx', mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")




empty_left, contents, empty_right = st.columns([0.45, 3, 0.1])

with contents:
    st.subheader("Filtre y Seleccione los que usted desee 🔍")
    
empty_left, contents, empty_right = st.columns([1.3, 3, 0.1])

with contents:
    st.markdown("O escriba para buscar coincidencias")





def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    modify = st.checkbox("Add filters")

    if not modify:
        return df 
    
    df = df.copy()
    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    dfColumns = ["ASSET_CLASS", "Nombre Negocio"]
    with modification_container:
        
        
        to_filter_columns = st.multiselect("Filtrar por: ", dfColumns)
        for column in to_filter_columns:
        
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            
            # if is_categorical_dtype(df[column]) or df[column].nunique() < 10:

            user_cat_input = right.multiselect(
                    f"{column}",
                    df[column].unique(),
                    default=(df[column].to_list())[0],
                    
                )
            
            
            df = df[df[column].isin(user_cat_input)]
            # elif is_numeric_dtype(df[column]):
            #     _min = float(df[column].min())
            #     _max = float(df[column].max())
            #     step = (_max - _min) / 100
            #     user_num_input = right.slider(
            #         f"Values for {column}",
            #         _min,
            #         _max,
            #         (_min, _max),
            #         step=step,
            #     )
            #     df = df[df[column].between(*user_num_input)]
            # elif is_datetime64_any_dtype(df[column]):
            #     user_date_input = right.date_input(
            #         f"Values for {column}",
            #         value=(
            #             df[column].min(),
            #             df[column].max(),
            #         ),
            #     )
            #     if len(user_date_input) == 2:
            #         user_date_input = tuple(map(pd.to_datetime, user_date_input))
            #         start_date, end_date = user_date_input
            #         df = df.loc[df[column].between(start_date, end_date)]
            # else:
            #     user_text_input = right.text_input(
            #         f"Substring or regex in {column}",
            #     )
            #     if user_text_input:
            #         df = df[df[column].str.contains(user_text_input)]





    return df



df_downl =filter_dataframe(df)

df_downlNoDupl = df_downl.drop_duplicates(subset=["Nombre Negocio"], keep='first')


st.dataframe(df_downlNoDupl[['Nombre Entidad','Nombre Negocio', "ASSET_CLASS"]],  hide_index=True )



# ! Descargar por CSV
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df_downl)

st.text(" ")


# ! Descargar por Excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data



col1, col2, col3 = st.columns(3)

with col2:
    st.download_button(label='Generar Informe',
                                    data=to_excel(df_downl) ,
                                    file_name= 'MisFondos.xlsx')



# Descarcar en Excel

# def to_excel(df):
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, index=False, sheet_name='Sheet1')
#     workbook = writer.book
#     worksheet = writer.sheets['Sheet1']
#     format1 = workbook.add_format({'num_format': '0.00'}) 
#     worksheet.set_column('A:A', None, format1)  
#     writer.save()
#     processed_data = output.getvalue()
#     return processed_data
# df_xlsx = to_excel(df)

# st.download_button(label='📥 Download Current Result',
#                                 data=df_xlsx ,
#                                 file_name= 'df_test.xlsx')



st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")


empty_left, contents, empty_right = st.columns([0.6, 2, 0.1])

with contents:
    st.subheader("_Todos Los Fondos Disponibles_")

empty_left, contents, empty_right = st.columns([1.3, 3, 0.1])

with contents:
    st.markdown("Espere hasta que el boton se active")




col1, col2, col3 = st.columns(3)

dfSIF2023 = pd.read_excel("SIF_2023Actualizado.xlsx",
                          sheet_name="SIF_2023Actualizado",
                          header=0)



with col2:
    st.download_button(label='Generar Informe SIF',
                       data=to_excel(dfSIF2023),
                       file_name= 'SIFInforme.xlsx')