import pandas as pd
from pandas import ExcelWriter
from math import sqrt

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
    df = df.assign(Rentab_Neg_Semestre= "" )
    df = df.assign(Rentab_Neg_1Y= "" )
    df = df.assign(ASSET_CLASS= "" )
    return df


dfSIF2023 = agregarColumnas(dfSIF2023)



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
                   sheet_name = "VU",
                   header = 12,
                   usecols = "B:NB",
                   nrows= 6
                   )

df_IBR = pd.read_excel(excel_modelo,
                   sheet_name = "IBR",
                   header = 5,
                   usecols = "H",
                   nrows = 3
                   )
# for (columnName, columnData) in dfVolatilidades.iteritems(): es igual a excepto con  
# ! dfVolatilidades





def listasADiccionarios(df):
    listName = []
    listData = []

    for (columnName, columnData) in df.items():
        listName.append(str(columnName))
        listData.append(columnData)
    

    diccionario = dict(zip(listName,listData))
    return diccionario


dictVolatilidad = listasADiccionarios(dfVolatilidades)
dictRentabilidades =listasADiccionarios(dfRentabilidades)
dictVecesNegativo = listasADiccionarios(dfVecesNegativo)
dictIBR = listasADiccionarios(df_IBR)



def revisarDicts(dict):
    keysList = list(dict.keys())
    print(keysList)
    print(len(keysList))
    print(dict[keysList[0]])
    print(dict[keysList[1]], "\n")



revisarDicts(dictVolatilidad)
revisarDicts(dictRentabilidades)
revisarDicts(dictVecesNegativo)

uniqueKeyIBR = list(dictIBR.keys())[0]
valoresIBR = dictIBR[uniqueKeyIBR] 


ibr1y = valoresIBR[0]*100 
ibr3y = valoresIBR[1]*100 
ibr5y = valoresIBR[2]*100    

#10.6
#5.1
#4.7


print(
    ibr1y, "  ",
    ibr3y, "  ",
    ibr5y
)

def procesarDato(dato):
    if dato == "ND":
        return dato
    else:
        return dato * 100

print("Corriendo Rentabilidades")
for i in range(rowCount2023):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictVecesNegativo:

        rentabilidad = dictRentabilidades[nombreFondo]
        dfSIF2023.at[i,"Rentab_1Y"] = procesarDato(rentabilidad[3])
        dfSIF2023.at[i,"Rentab_3Y"] = procesarDato(rentabilidad[4])
        dfSIF2023.at[i,"Rentab_5Y"] = procesarDato(rentabilidad[5])

    else:

        dfSIF2023.at[i,"Rentab_1Y"] = "-"
        dfSIF2023.at[i,"Rentab_3Y"] = "-"
        dfSIF2023.at[i,"Rentab_5Y"] = "-"



print("Corriendo Volatilidad")
for i in range(rowCount2023):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictVolatilidad:

        volatilidad = dictVolatilidad[nombreFondo]
        dfSIF2023.at[i,"V_mensual"] = procesarDato(volatilidad[0])
        dfSIF2023.at[i,"V_semestral"] = procesarDato(volatilidad[1])
        dfSIF2023.at[i,"V_Ytd"] = procesarDato(volatilidad[2])
        dfSIF2023.at[i,"V_1Y"] = procesarDato(volatilidad[3])
        dfSIF2023.at[i,"V_3Y"] = procesarDato(volatilidad[4])
        dfSIF2023.at[i,"V_5Y"] = procesarDato(volatilidad[5])

    else:
        dfSIF2023.at[i,"V_mensual"] = "-"
        dfSIF2023.at[i,'V_semestral'] = "-"
        dfSIF2023.at[i,"V_Ytd"] = "-"
        dfSIF2023.at[i,"V_1Y"] = "-"
        dfSIF2023.at[i,"V_3Y"] = "-"
        dfSIF2023.at[i,"V_5Y"] = "-"



print("Corriendo Sharpe")
def calcularSharpe(rentabilidad, ibr, volatilidad):
    try:
        sharpe = (rentabilidad*100)-ibr/(volatilidad*100)

    except:
        sharpe = "ND"
    return sharpe


for i in range(rowCount2023):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictVolatilidad and nombreFondo in dictRentabilidades:

        rentabilidad = dictRentabilidades[nombreFondo]
        volatilidad = dictVolatilidad[nombreFondo]

        dfSIF2023.at[i, "Sharpe_1Y"] = calcularSharpe(rentabilidad[3], ibr1y, volatilidad[3])
        dfSIF2023.at[i, "Sharpe_3Y"] = calcularSharpe(rentabilidad[4], ibr3y,volatilidad[4])
        dfSIF2023.at[i, "Sharpe_5Y"] = calcularSharpe(rentabilidad[5], ibr5y,volatilidad[5])
    else:
        dfSIF2023.at[i, "Sharpe_1Y"] = "-"
        dfSIF2023.at[i, "Sharpe_3Y"] = "-"
        dfSIF2023.at[i, "Sharpe_5Y"] = "-"
    

print("Corriendo Veces Negativo")
for i in range(rowCount2023):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictRentabilidades:

        vecesNegativo = dictVecesNegativo[nombreFondo]
        dfSIF2023.at[i, "Rentab_Neg_semana"] = vecesNegativo[0]
        dfSIF2023.at[i, "Rentab_Neg_mes"] = vecesNegativo[1]
        dfSIF2023.at[i, "Rentab_Neg_YtD"] = vecesNegativo[2]
        dfSIF2023.at[i, "Rentab_Neg_Semestre"] = vecesNegativo[3]
        dfSIF2023.at[i, "Rentab_Neg_1Y"] = vecesNegativo[4]


    else:
        dfSIF2023.at[i, "Rentab_Neg_semana"] = "-"
        dfSIF2023.at[i, "Rentab_Neg_mes"] = "-"
        dfSIF2023.at[i, "Rentab_Neg_YtD"] = "-"
        dfSIF2023.at[i, "Rentab_Neg_1Y"] = "-"


writer = ExcelWriter('SIF_2023Actualizado.xlsx')
dfSIF2023.to_excel(writer, 'SIF_2023Actualizado', index=False)
writer.close()



dfSIF2023NoDupl = dfSIF2023.drop_duplicates(subset=["Nombre Negocio"], keep='first')
print(dfSIF2023NoDupl.shape[0])

writer = ExcelWriter('SIF_2023NoDuplAct.xlsx')
dfSIF2023NoDupl.to_excel(writer, 'SIF_2023NoDuplAct.xlsx', index=False)
writer.close()