import pandas as pd
from pandas import ExcelWriter


def to_excel(df):
    output = BytesIO()
    from io import BytesIO
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data


dfSIF2023 = pd.read_excel("SIF_BD_2023.xlsx",
                          sheet_name= "Sheet1",
                          header= 0)

dfSIF2023NoDupl = dfSIF2023.drop_duplicates(subset=["Nombre Negocio"], keep='first')

# ! Crear Columnas Nuevas

dfSIF2023 = dfSIF2023.rename(columns={'Rentab. año':'RN.Ytd'})


def agregarColumnas(df):
    df = df.assign(Rentab_1Y= "" )
    df = df.assign(Rentab_3Y= "" )
    df = df.assign(Rentab_5Y= "" )
    df = df.assign(V_mensual= "" )
    df = df.assign(V_semestral= "" )
    df = df.assign(V_Ytd= "" )
    df = df.assign(V_1Y= "" )
    df = df.assign(V_3Y= "" )
    df = df.assign(V_5Y= "" )
    df = df.assign(Sharpe_1Y= "" )
    df = df.assign(Sharpe_3Y= "" )
    df = df.assign(Sharpe_5Y= "" )
    df = df.assign(Rentab_Neg_semana	= "" )
    df = df.assign(Rentab_Neg_mes= "" )
    df = df.assign(Rentab_Neg_YtD= "" )
    df = df.assign(Rentab_Neg_1Y= "" )
    df = df.assign(ASSET_CLASS= "" )
    return df


dfSIF2023 = agregarColumnas(dfSIF2023)
dfSIF2023NoDupl = agregarColumnas(dfSIF2023NoDupl)

print(dfSIF2023NoDupl.columns)

dfTiposFondos = pd.read_excel("TiposFondos.xlsx",
                           sheet_name= "Hoja1",
                           header= 0)


dfTiposFondosNoDupl = dfTiposFondos.drop_duplicates(subset=["Nombre Negocio"], keep='first')


diccionarioTiposFondos = dict(zip(dfTiposFondosNoDupl['Nombre Negocio'],
                                  dfTiposFondosNoDupl['ASSET_CLASS.ASSET CLASS']
                                  ))





rowCount2023 = dfSIF2023.shape[0]


for i in range(rowCount2023):

    nombreFondo = dfSIF2023["Nombre Negocio"][i]
    
    if nombreFondo in diccionarioTiposFondos:
    
        tipoFondo= diccionarioTiposFondos[nombreFondo]
        dfSIF2023.at[i, 'ASSET_CLASS'] = tipoFondo
    else:
        dfSIF2023.at[i, 'ASSET_CLASS'] = "INDEFINIDO"






# ! MODELO.xlsb para sacar las volatilidades y veces negativas

excel_modelo = "MODELO.xlsb"

dfVolatilidades = pd.read_excel(excel_modelo,
                   sheet_name= "R_diarias",
                   header=17,
                   usecols = "C:NC",
                   nrows= 6
                   )

dfVecesNegativo = pd.read_excel(excel_modelo,
                   sheet_name= "R_diarias",
                   header=28,
                   usecols = "C:NC",
                   nrows= 5
                   )


dfRentabilidades = pd.read_excel(excel_modelo,
                   sheet_name= "VU",
                   header=13,
                   usecols = "B:NB",
                   nrows= 7
                   )


# for (columnName, columnData) in dfVolatilidades.iteritems(): es igual a excepto con  
# ! dfVolatilidades

print(dfSIF2023NoDupl.shape[0])


listName = []
listData = []


def listasADiccionarios(df):
    for (columnName, columnData) in df.items():
        listName.append(columnName)
        listData.append(columnData)
    
    diccionario = dict(zip(listName,listData))
    return diccionario

# def asignarValoresColumnas(dfNoDupl):
        # for i in range(dfNoDupl.shape[0]):


dictVecesNegativo = listasADiccionarios(dfVecesNegativo)
dictVolatilidad = listasADiccionarios(dfVolatilidades)
dictRentabilidades =listasADiccionarios(dfRentabilidades)


for i in range(rowCount2023):

    nombreFondo = dfSIF2023["concatenar"][i]
    
    if nombreFondo in dictVolatilidad:
    
        tipoFondo = dictVolatilidad[nombreFondo]
        dfSIF2023.at[i, 'V_mensual'] = tipoFondo[0]
    else:
        dfSIF2023.at[i, 'V_mensual'] = "-"


                
            #     dfNoDupl.at["V_mensual", i] = "Asignacion funciona"
            #     dfNoDupl.at["V_semestral", i] = "Asignacion funciona"
            #     dfNoDupl.at["V_Ytd", i] = "Asignacion funciona"
            #     dfNoDupl.at["V_1Y", i] = "Asignacion funciona"
            #     dfNoDupl.at["V_3Y", i] = "Asignacion funciona"
            #     dfNoDupl.at["V_5Y", i] = "Asignacion funciona"


            #     Modelo -> IBR Celda H7

            #     dfNoDupl.at["Sharpe_1Y", i] = "(1+[RN. 1Y]])/(1+IBR Celda H7))-1)/RAIZ(Volatilidad. 1Y)
            #     dfNoDupl.at["Sharpe_3Y", i] = "(1+[RN. 3Y]])/(1+IBR Celda H7))-1)/RAIZ(Volatilidad. 3Y)
            #     dfNoDupl.at["Sharpe_5Y", i] = "(1+[RN. 5Y]])/(1+IBR Celda H7))-1)/RAIZ(Volatilidad. 5Y)

            #     dfNoDupl.at["Rentab_Neg_semana", i] = "Asignacion funciona"
            #     dfNoDupl.at["Rentab_Neg_mes", i] = "Asignacion funciona"
            #     dfNoDupl.at["Rentab_Neg_YtD", i] = "Asignacion funciona"
            #     dfNoDupl.at["Rentab_Neg_1Y", i] = "Asignacion funciona"       


writer = ExcelWriter('SIF_2023Actualizado.xlsx')
dfSIF2023.to_excel(writer, 'SIF_2023Actualizado', index=False)
writer.close()
