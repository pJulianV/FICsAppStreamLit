import pandas as pd
from pandas import ExcelWriter
from math import sqrt


fechaCorte = "06 30 2023  0:00:00"


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

dfSIF2023 = dfSIF2023.rename(columns={'Rentab. año':'Rentab. Ultaño'})

dfSIF2023 = dfSIF2023[dfSIF2023["Fecha corte"] == fechaCorte]



def agregarColumnas(df):
    df = df.assign(Rentab_Ytd= "" )
    df = df.assign(Rentab_3Y= "" )
    df = df.assign(Rentab_5Y= "" )
    df = df.assign(Comision_Admin= "" )
    df = df.assign(RB_mensual = "" )
    df = df.assign(RB_semestral = "" )
    df = df.assign(RB_Ytd = "" )
    df = df.assign(RB_1Y = "" )
    df = df.assign(RB_3Y = "" )
    df = df.assign(RB_5Y = "" )
    df = df.assign(ASSET_CLASS= "" )
    df = df.assign(Nombre_Entidad_Corto= "" )
    df = df.assign(Nombre_Fondo_Corto= "" )
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
    return df


dfSIF2023 = agregarColumnas(dfSIF2023)



dfTiposFondos = pd.read_excel("BD ASSET CLASS.xlsx",
                           sheet_name= "Hoja1",
                           header= 0)


dfTiposFondosNoDupl = dfTiposFondos.drop_duplicates(subset=["NOMBRE NEGOCIO"], keep='first')


diccionarioTiposFondos = dict(zip(dfTiposFondosNoDupl['NOMBRE NEGOCIO'],
                                  dfTiposFondosNoDupl['ASSET CLASS']
                                  ))


dfSIF2023.reset_index(drop=True, inplace=True)


for i in range(dfSIF2023.shape[0]):

    nombreFondo = dfSIF2023["Nombre Negocio"][i]
    
    if nombreFondo in diccionarioTiposFondos:
    
        tipoFondo= diccionarioTiposFondos[nombreFondo]
        dfSIF2023.at[i, 'ASSET_CLASS'] = tipoFondo
    else:
        dfSIF2023.at[i, 'ASSET_CLASS'] = "INDEFINIDO"


dfPrueba = dfSIF2023
dfSIF2023 = dfSIF2023[dfSIF2023["ASSET_CLASS"] != "CAPITAL PRIVADO"]
dfSIF2023.reset_index(drop=True, inplace=True)

# ! MODELO_TodosLosFondos para sacar las volatilidades y veces negativas

excel_modelo = "MODELO_TodosLosFondos.xlsb"

dfVolatilidades = pd.read_excel(excel_modelo,
                   sheet_name= "R_diarias",
                   header=17,
                   usecols = "C:APV",
                   nrows= 6
                   )

dfVecesNegativo = pd.read_excel(excel_modelo,
                   sheet_name= "R_diarias",
                   header=28,
                   usecols = "C:APV",
                   nrows= 5
                   )


dfRentabilidades = pd.read_excel(excel_modelo,
                   sheet_name = "VU",
                   header = 12,
                   usecols = "B:APU",
                   nrows= 6
                   )
df_IBR = pd.read_excel(excel_modelo,
                   sheet_name = "IBR",
                   header = 5,
                   usecols = "H",
                   nrows = 3
                   )

# De Aqui saco el Nombre Corto y la Comision
dfIndustriaLocal = pd.read_excel( "BDIndustriaLocalFICs.xlsx",
                   sheet_name= "BD 30Abr2023",
                   header=1,
                   usecols = "A:Z",
                   )


# for (columnName, columnData) in dfVolatilidades.iteritems(): es igual a excepto con  
# ! dfVolatilidades


print(list(dfIndustriaLocal.columns))


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


dictNombresCortos = dict(zip(dfIndustriaLocal['Nombre Negocio'],
                                  dfIndustriaLocal['Nombre Corto']
                                  ))

dictComisionAdmin = dict(zip(dfIndustriaLocal['concatenar'],
                                  dfIndustriaLocal['Comisión admin(%)']
                                  )) 

dictEntidadCorto = dict(zip(dfIndustriaLocal['Nombre Entidad'],
                                  dfIndustriaLocal['Nombre Corto Entidad']
                                  ))


def revisarDicts(dict):
    keysList = list(dict.keys())
    print(keysList)
    print(len(keysList))
    print(dict[keysList[0]])
    print(dict[keysList[2]], "\n")



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
for i in range(dfSIF2023.shape[0]):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictRentabilidades:

        rentabilidad = dictRentabilidades[nombreFondo]
        dfSIF2023.at[i,"Rentab_Ytd"] = procesarDato(rentabilidad[2])
        dfSIF2023.at[i,"Rentab_3Y"] = procesarDato(rentabilidad[4])
        dfSIF2023.at[i,"Rentab_5Y"] = procesarDato(rentabilidad[5])

    else:

        dfSIF2023.at[i,"Rentab_Ytd"] = "-"
        dfSIF2023.at[i,"Rentab_3Y"] = "-"
        dfSIF2023.at[i,"Rentab_5Y"] = "-"




print("Corriendo Rentabilidades brutas")
def calcularRB(rentabilidad, comision):
    
    try:
        rentB = (1+rentabilidad)/(1+(comision/100))-1

    except:
        rentB = "ND"

    return rentB


for i in range(dfSIF2023.shape[0]):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictComisionAdmin :

        comision = dictComisionAdmin[nombreFondo]

        dfSIF2023.at[i, "RB_mensual"] = calcularRB(dfSIF2023["Rentab. mes"][i], comision)
        dfSIF2023.at[i, "RB_semestral"] = calcularRB(dfSIF2023["Rentab. sem"][i], comision)
        dfSIF2023.at[i, "RB_Ytd"] = calcularRB(dfSIF2023["Rentab_Ytd"][i], comision)
        dfSIF2023.at[i, "RB_1Y"] = calcularRB(dfSIF2023["Rentab. Ultaño"][i], comision)
        dfSIF2023.at[i, "RB_3Y"] = calcularRB(dfSIF2023["Rentab_3Y"][i], comision)
        dfSIF2023.at[i, "RB_5Y"] = calcularRB(dfSIF2023["Rentab_5Y"][i], comision)

    else:
        dfSIF2023.at[i, "RB_mensual"] = "-" 
        dfSIF2023.at[i, "RB_semestral"] = "-" 
        dfSIF2023.at[i, "RB_Ytd"] = "-" 
        dfSIF2023.at[i, "RB_1Y"] = "-" 
        dfSIF2023.at[i, "RB_3Y"] = "-" 
        dfSIF2023.at[i, "RB_5Y"] = "-" 
    



print("Corriendo Volatilidad")
for i in range(dfSIF2023.shape[0]):

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
        sharpe = ((rentabilidad*100)-ibr)/(volatilidad*100)
        sharpe = ((rentabilidad*100)-ibr)/(volatilidad*100)

    except:
        sharpe = "ND"

    return sharpe


for i in range(dfSIF2023.shape[0]):

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
    

# Ver cuales fondos estan en modelo pero no en SIF
listaNoEncontrados = []

for i in range(dfSIF2023.shape[0]):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictVolatilidad:
        dictVolatilidad[nombreFondo]


print(listaNoEncontrados)


print("Corriendo Veces Negativo")
for i in range(dfSIF2023.shape[0]):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictVecesNegativo:

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





listNombreCorto = []

print("Corriendo Nombre Corto")
for i in range(dfSIF2023.shape[0]):

    nombreFondo = dfSIF2023["Nombre Negocio"][i]
    if nombreFondo in dictNombresCortos:
        nombreCorto = dictNombresCortos[nombreFondo]
        dfSIF2023.at[i, "Nombre_Fondo_Corto"] = nombreCorto
    else:
        listNombreCorto.append(nombreFondo)
        dfSIF2023.at[i, "Nombre_Fondo_Corto"] = nombreFondo



listNombreCortoEnt = []

print("Corriendo Nombre Corto Entidad")
for i in range(dfSIF2023.shape[0]):

    nombreEntidad = dfSIF2023["Nombre Entidad"][i]
    if nombreEntidad in dictEntidadCorto:
        nombreCorto = dictEntidadCorto[nombreEntidad]
        dfSIF2023.at[i, "Nombre_Entidad_Corto"] = nombreCorto
    else:
        listNombreCortoEnt.append(nombreEntidad)
        dfSIF2023.at[i, "Nombre_Entidad_Corto"] = nombreEntidad




print("Corriendo Comision")
for i in range(dfSIF2023.shape[0]):

    nombreFondo = dfSIF2023["concatenar"][i]
    if nombreFondo in dictComisionAdmin:
        comisionAdmin = dictComisionAdmin[nombreFondo]
        dfSIF2023.at[i, "Comision_Admin"] = comisionAdmin
    else:
        dfSIF2023.at[i, "Comision_Admin"] = "-"



dfSIF2023SinFilt = dfSIF2023

dfSIF2023 = dfSIF2023[["concatenar","Fecha corte","ASSET_CLASS", "Nombre_Entidad_Corto", "Nombre_Fondo_Corto", "Cons. id Part.", "Núm. unidades", "Valor unidad para las operaciones del día t", "Valor fondo al cierre del día t", "Núm. Invers.", "Comision_Admin", "Rentab. dia",	"Rentab. mes",	"Rentab. sem",	"Rentab. Ultaño",	"Rentab_Ytd",	"Rentab_3Y",	"Rentab_5Y", "RB_mensual",	"RB_semestral",	"RB_Ytd",	"RB_1Y",	"RB_3Y",	"RB_5Y", "V_mensual",	"V_semestral",	"V_Ytd",	"V_1Y",	"V_3Y",	"V_5Y", "Sharpe_1Y",	"Sharpe_3Y",	"Sharpe_5Y", "Rentab_Neg_semana",	"Rentab_Neg_mes",	"Rentab_Neg_YtD",	"Rentab_Neg_Semestre",	"Rentab_Neg_1Y"


]]


dfSIF2023.rename(columns={ 'Cons. id Part.': 'ID Participacion' })
# dfSIF2023.rename(columns={ 'Nombre_Corto': 'Nombre Fondo' })


dfSIF2023.columns = dfSIF2023.columns.str.replace('Cons. id Part.', 'ID Participacion')
# dfSIF2023.columns = dfSIF2023.columns.str.replace('Nombre_Fondo_Corto', 'Nombre Fondo')
# dfSIF2023.columns = dfSIF2023.columns.str.replace('Nombre_Entidad_Corto', 'Nombre Entidad')




writer = ExcelWriter('SIF_2023Actualizado.xlsx')
dfSIF2023.to_excel(writer, 'SIF_2023Actualizado', index=False)
writer.close()



writer = ExcelWriter('SIF_2023Prueba.xlsx')
dfPrueba.to_excel(writer, 'SIF_2023Prueba', index=False)
writer.close()


writer = ExcelWriter('SIF_2023AllCol.xlsx')
dfSIF2023SinFilt.to_excel(writer, 'SIF_2023AllCol', index=False)
writer.close()



print("Nombre Corto Entidad: ",len(listNombreCortoEnt))
print("Nombre Corto: ",len(listNombreCorto))

print("dfSIF2023 rows: ", dfSIF2023.shape[0])
print("dfSIF sin Capital Privado rows: ", dfPrueba.shape[0])

