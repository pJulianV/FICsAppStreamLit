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

# ! Crear Columnas Nuevas

dfSIF2023 = dfSIF2023.rename(columns={'Rentab. año':'RN.Ytd'})


dfSIF2023 = dfSIF2023.assign(Rentab_1Y= "" )
dfSIF2023 = dfSIF2023.assign(Rentab_3Y= "" )
dfSIF2023 = dfSIF2023.assign(Rentab_5Y= "" )
dfSIF2023 = dfSIF2023.assign(V_mensual= "" )
dfSIF2023 = dfSIF2023.assign(V_semestral= "" )
dfSIF2023 = dfSIF2023.assign(V_Ytd= "" )
dfSIF2023 = dfSIF2023.assign(V_1Y= "" )
dfSIF2023 = dfSIF2023.assign(V_3Y= "" )
dfSIF2023 = dfSIF2023.assign(V_5Y= "" )
dfSIF2023 = dfSIF2023.assign(Sharpe_1Y= "" )
dfSIF2023 = dfSIF2023.assign(Sharpe_3Y= "" )
dfSIF2023 = dfSIF2023.assign(Sharpe_5Y= "" )
dfSIF2023 = dfSIF2023.assign(Rentab_Neg_semana	= "" )
dfSIF2023 = dfSIF2023.assign(Rentab_Neg_mes= "" )
dfSIF2023 = dfSIF2023.assign(Rentab_Neg_YtD= "" )
dfSIF2023 = dfSIF2023.assign(Rentab_Neg_1Y= "" )


dfSIF2023 = dfSIF2023.assign(ASSET_CLASS= "" )

dfSIF2023.columns

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



dfSIF2023NoDupl = dfSIF2023.drop_duplicates(subset=["Nombre Negocio"], keep='first')


fondosCount2023 = dfSIF2023NoDupl.shape[0]



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




# dfSIF2023_downl =filter_dataframe(dfSIF2023)



# for (columnName, columnData) in dfVolatilidades.iteritems(): es igual a excepto con  
# ! dfVolatilidades

for (columnName, columnData) in dfVecesNegativo.iteritems():
    
    for i in range(dfSIF2023.shape[0]):
        nombreFondo = dfSIF2023["Nombre Negocio"][i]

        if nombreFondo in columnName:

            # dfSIF2023.at["Sharpe_1Y", i] = 
            # dfSIF2023.at["Sharpe_3Y", i] = 
            # dfSIF2023.at["Sharpe_5Y", i] = 
            
            dfSIF2023.at["V_mensual", i] = dfVolatilidades
            dfSIF2023.at["V_semestral", i] = dfVolatilidades
            dfSIF2023.at["V_Ytd", i] = dfVolatilidades
            dfSIF2023.at["V_1Y", i] = dfVolatilidades
            dfSIF2023.at["V_3Y", i] = dfVolatilidades
            dfSIF2023.at["V_5Y", i] = dfVolatilidades


            dfSIF2023.at["Rentab_Neg_semana", i] = "Asignacion funciona"
            dfSIF2023.at["Rentab_Neg_mes", i] = "Asignacion funciona"
            dfSIF2023.at["Rentab_Neg_YtD", i] = "Asignacion funciona"
            dfSIF2023.at["Rentab_Neg_1Y", i] = "Asignacion funciona"       # dfVecesNegativo



        else:
            dfSIF2023.at["Rentab_Neg_semana", i] = "-"
            dfSIF2023.at["Rentab_Neg_mes", i] = "-"
            dfSIF2023.at["Rentab_Neg_YtD", i] = "-"
            dfSIF2023.at["Rentab_Neg_1Y", i] = "-"



writer = ExcelWriter('SIF_2023Actualizado.xlsx')
dfSIF2023.to_excel(writer, 'SIF_2023Actualizado', index=False)
writer.save()
