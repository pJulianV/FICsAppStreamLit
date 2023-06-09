# streamlit run streamlit_app.py
# pip install -r requirements.txt

# cd OneDrive - Grupo Bancolombia\Workspace\PruebaStreamLit
# cd Workspace\FIC StreamLit

import pandas as pd
# from io import BytesIO
# from pyxlsb import open_workbook as open_xlsb
import streamlit as st

# import plotly.express as px
# from PIL import Image


from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)



st.set_page_config(
    page_title="FICs App",
    page_icon="📈",
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


st.header("📈 FICs App")
st.subheader("Descargue nuestros fondos sugeridos o seleccione los que usted desee\n")
st.text(" ")

with open("InformeFICs.xlsx", 'rb') as my_file:
    st.download_button(label = 'Nuestros Sugeridos', data = my_file, file_name = 'FondosSugeridos.xlsx', mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




st.text(" ")

excel_file = "InformeFICs.xlsx"
sheet_name = "Hoja1"

df = pd.read_excel(excel_file,
                   sheet_name= sheet_name,
                   header=0
                   )




# fondo = df["Nombre Negocio"].unique().tolist()

# fondo_selection = st.multiselect("Fondo: ",
#                                  fondo,
#                                  default=fondo[0])




# mask = df["Nombre Negocio"].isin(fondo_selection)

# number_of_result = df[mask].shape[0]
# st.markdown(f"*Avaliable Results: {number_of_result}*")

dfNoDupl= df.drop_duplicates(subset=["Nombre Negocio"], keep='first')
st.dataframe(dfNoDupl[['Nombre Entidad','Nombre Negocio']], hide_index=True )


# fondo_tipo = df["Tipo Fondo"].unique().tolist()
fondo_tipo = ["Todo", "Renta Fija", "Balanceados","Acciones","1525"]
fondo_tipo_selection = st.multiselect("Tipo Fondo: ",
                                 fondo_tipo,
                                 default=fondo_tipo[1])

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:


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


    with modification_container:
        to_filter_columns = ["Nombre Negocio"]
                            # st.multiselect("Filtrar Por", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            
            # if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                
            user_cat_input = right.multiselect(
                    f"{column}",
                    df[column].unique(),
                    default=df[column][0],
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

st.dataframe(df_downlNoDupl[['Nombre Entidad','Nombre Negocio']],  hide_index=True )



# Descargar por CSV
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df_downl)

st.text(" ")

st.download_button(
   "Press to Download",
   csv,
   "MisFondos.csv",
   "text/csv",
   key='download-csv'
)


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