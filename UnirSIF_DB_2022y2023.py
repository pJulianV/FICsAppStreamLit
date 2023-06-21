import pandas as pd
from pandas import ExcelWriter
# decodigo.com

dfSIF2022 = pd.read_excel("SIF_BD_2022.xlsx",
                          sheet_name= "Sheet1",
                          header= 0)

dfSIF2023 = pd.read_excel("SIF_BD_2023.xlsx",
                          sheet_name= "Sheet1",
                          header= 0)


# dfSIF = pd.concat([dfSIF2022, dfSIF2023], axis=0)
dfSIF = dfSIF2022.append(dfSIF2023)


writer = ExcelWriter('SIF_2022+2023.xlsx')
dfSIF.to_excel(writer, 'SIF_2022+2023', index=False)
writer.save()
