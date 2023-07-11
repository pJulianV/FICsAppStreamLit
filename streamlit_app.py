# ! Las dependencia, rutas y codigos que se usan en la terminal de anaconda

# cd OneDrive - Grupo Bancolombia\Workspace\FicsAppStreamLit
# cd Workspace\FIC StreamLit
# streamlit run streamlit_app.py

# pip install -r requirements.txt

# pip install ______ -i https://artifactory.apps.bancolombia.com/api/pypi/python-org/simple --trusted-host artifactory.apps.bancolombia.com

# pip install -r requirements.txt -i https://artifactory.apps.bancolombia.com/api/pypi/python-org/simple --trusted-host artifactory.apps.bancolombia.com



# ! Los Dataframe con terminacion "NoDupl" es para la visualizacion NO USAR en el excel final


import pandas as pd
import streamlit as st
# import plotly.express as px

from io import BytesIO
from xlsxwriter import Workbook
from PIL import Image
# from pyxlsb import open_workbook as open_xlsb



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
    st.header("Reporte de competencia industria ㅤㅤㅤㅤㅤ local de fondos")


empty_left, contents, empty_right = st.columns([2, 3, 0.1])

with contents:
    st.markdown("Fecha Corte: 05 31 2023")


st.text(" ")


img = Image.open("img/investment3.jpeg")
st.image(img, use_column_width=True)


excel_file = "MODELO.xlsb"
sheet_name = "BD"

df = pd.read_excel(excel_file,
                   sheet_name= sheet_name,
                   header=0,
                   usecols = "A:AF",
                   )

dfNoDupl= df.drop_duplicates(subset=["Nombre Negocio"], keep='first')

dfTiposFondos = pd.read_excel("BD ASSET CLASS.xlsx",
                           sheet_name= "Hoja1",
                           header= 0)

dfIndustriaLocal = pd.read_excel( "BDIndustriaLocalFICs.xlsx",
                   sheet_name= "BD 30Abr2023",
                   header=1,
                   usecols = "A:Z",
                   )

dictNombresCortos = dict(zip(dfIndustriaLocal['concatenar'],
                                  dfIndustriaLocal['Nombre Corto']
                                  ))

dictComisionAdmin = dict(zip(dfIndustriaLocal['concatenar'],
                                  dfIndustriaLocal['Comisión admin(%)']
                                  )) 

rowCount = df.shape[0]

df = df.assign(Nombre_Corto= "" )

print("Corriendo Nombre Corto")
for i in range(rowCount):

    nombreFondo = df["Llave"][i]
    if nombreFondo in dictNombresCortos:
        nombreCorto = dictNombresCortos[nombreFondo]
        df.at[i, "Nombre_Corto"] = nombreCorto
    else:
        df.at[i, "Nombre_Corto"] = nombreFondo


print("Corriendo Comision")
for i in range(rowCount):

    nombreFondo = df["Llave"][i]
    if nombreFondo in dictComisionAdmin:
        comisionAdmin = dictComisionAdmin[nombreFondo]
        df.at[i, "Comision_Admin"] = comisionAdmin
    else:
        df.at[i, "Comision_Admin"] = "-"


dfTiposFondosNoDupl = dfTiposFondos.drop_duplicates(subset=["Nombre Negocio"], keep='first')


# ! Emparejar fondo con su tipo:

df = df.assign(ASSET_CLASS= "" )

nombreFondos70 = df["Nombre Negocio"].unique().tolist()

nombresDBTiposFondos = dfTiposFondos["Nombre Negocio"].unique().tolist()


listaTiposFondos = dfTiposFondos["ASSET CLASS"].unique().tolist()


diccionarioTiposFondos = dict(zip(dfTiposFondosNoDupl['Nombre Negocio'],
                                  dfTiposFondosNoDupl['ASSET CLASS']
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

# ! Descargar por Excel
@st.cache_data(ttl=3600)
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




col1, col2, col3 = st.columns([1.2, 2, 0.1])


with col2:
    # with open(excel_file, 'rb') as my_file:
    st.download_button(label='Generar Informe SIF',
                       data=to_excel(df) ,
                       file_name= 'FondosSugeridos.xlsx'
                       )

    
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")


empty_left, contents, empty_right = st.columns([2.5, 2, 2])
st.text(" ")

with empty_left:
    st.markdown("ㅤ")
    st.markdown("SN - SENTENCIAS NACION")
    st.markdown("PP - PACTO DE PERMANENCIA")

with contents:
    st.markdown("ABREVIATURAS: ")
    st.markdown("RF - RENTA FIJA")
    st.markdown("LP - LARGO PLAZO")

with empty_right:
    st.markdown("ㅤ")
    st.markdown("TS - TASA FIJA")
    st.markdown("COL - COLOMBIA")

st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")


empty_left, contents, empty_right = st.columns([0.45, 3, 0.1])

with contents:
    st.subheader("Filtre y Seleccione los que usted desee 🔍")
    
empty_left, contents, empty_right = st.columns([1.3, 3, 0.1])

with contents:
    st.markdown("(Base de fondos sugeridos)")


st.text(" ")
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



st.dataframe(df_downlNoDupl[['Nombre Entidad','Nombre_Corto'
                             , "ASSET_CLASS"
                            ]],  hide_index=True )




# ! Descargar por CSV
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df_downl)

st.text(" ")





col1, col2, col3 = st.columns(3)

with col2:
    st.download_button(label='Generar Informe',
                                    data=to_excel(df_downl) ,
                                    file_name= 'MisFondos.xlsx')




st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")



# ! SIF 2023!!!

def filter_dataframeSIF(df: pd.DataFrame) -> pd.DataFrame:

    modifySIF = st.checkbox("Add filters SIF")

    if not modifySIF:
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

    dfColumns2023 = ["ASSET_CLASS", "Nombre Negocio"]
    with modification_container:
        
        
        to_filter_columns2023 = st.multiselect("Filtra por: ", dfColumns2023,key="SIF")
        for column in to_filter_columns2023:
        
            left, right = st.columns((1, 20))
            left.write("↳")

            user_cat_input = right.multiselect(
                    f"{column}",
                    df[column].unique(),
                    default=(df[column].to_list())[0],
                    
                )
            
            
            df = df[df[column].isin(user_cat_input)]


    return df



empty_left, contents, empty_right = st.columns([0.6, 2, 0.1])

with contents:
    st.subheader("_Base total industria local de fondos_")

empty_left, contents, empty_right = st.columns([1.3, 3, 0.1])

with contents:
    st.markdown("(Fuente: Reporte 523 Superfinanciera)")


sheetSIF2023 = "SIF_2023Actualizado"
excelSIF2023 = sheetSIF2023 + ".xlsx" 

#   Original:                       "SIF_2023Actualizado"
#   Sin "Concatenar Duplicado":     "SIF_2023NoDuplAct"

@st.cache_data(ttl=3600)
def load_data(excel,sheet):
    # Carga tu DataFrame aquí
    df = pd.read_excel(excel,
                sheet_name= sheet,
                  header= 0)
    return df
 
dfSIF2023 = load_data(excelSIF2023,sheetSIF2023)



df_downl2023 = filter_dataframeSIF(dfSIF2023)


df_downl2023NoDupl = df_downl2023.drop_duplicates(subset=["Nombre Negocio"], keep='first')


st.dataframe(df_downl2023NoDupl[['Nombre Entidad','Nombre_Corto', 
                                 "ASSET_CLASS"
                                ]],  hide_index=True )




col1, col2, col3 = st.columns(3)


with col2:

    st.download_button(label='Generar Informe SIF',
                       data=to_excel(df_downl2023) ,
                       file_name= 'SIFInforme.xlsx'
                       )


# def load_data(sheets_url):
#     csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
#     return pd.read_csv(csv_url)


# df = load_data(st.secrets["public_gsheets_url"])

# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")

@st.cache_data(ttl=3600)
def load_data(url):
    return  pd.read_csv(url, dtype=str).fillna("")



# Connect to the Google Sheet
# sheet_id = "1tfWAudn1Hkd3TizWbeif7ZdJHEQYH8UpWQv18q7gJxw"
# sheet_name = "1816189210"
# url = f"<https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}>"
# df = load_data(url)


# # Show the dataframe (we'll delete this later)
# st.write(df)