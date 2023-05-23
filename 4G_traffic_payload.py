import pandas as pd
import patoolib
import MySQLdb
import os
import shutil

#copy report_cell_volte
source_path = "path to file"
volte_move  = "path to file"
shutil.copy(source_path, volte_move)

#extract data volte
patoolib.extract_archive("path to file")
print("extract Success")
#pilih column dari data volte
column = [6, 14]
df_volte = pd.read_csv("path to file", usecols=column)
# Ubah nama header data volte
df_volte.columns.values[0] = "Cell Name"
df_volte.columns.values[1] = "Volte_Traffic"

#baca data 4g csv & merge dengan data carrier
df_4g = pd.read_csv(r"C:\Users\User\Downloads\hari ini\py\4g.csv")
df_join = pd.merge(df_4g, df_volte, on="Cell Name", how="inner")
column_join = df_join[["Date","SiteID", "Band","Volte_Traffic","Total_Payload_GB"]]

#Ubah Carrier
column_join.loc[column_join['Band'] == 'LTE 900', 'Band'] = 'LTE900'
column_join.loc[column_join['Band'] == 'LTE 1800', 'Band'] = 'LTE1800'
column_join.loc[column_join['Band'] == 'LTE 2100', 'Band'] = 'LTE2100'
column_join.loc[column_join['Band'] == 'LTE 2300', 'Band'] = 'LTE2300'


#Group data 4g
column_join= column_join.groupby(['Date','SiteID','Band']).sum().reset_index()
column_join['Sum process'] = column_join['Volte_Traffic']+column_join['Total_Payload_GB']
column_join.drop(column_join[column_join['Sum process'] == 0].index, inplace=True)

#Ubah menjadi data Final
column_final = column_join[["Date","SiteID", "Band","Volte_Traffic","Total_Payload_GB"]]
column_final.to_csv(r"C:\Users\User\Downloads\hari ini\py\4g_traffic_payload.csv", index=None)
print("4g Traffic Payload Success")


# remove old excel file
if os.path.exists(r"C:\Users\User\Downloads\hari ini\py\report_cell_volte.csv"):
   os.remove(r"C:\Users\User\Downloads\hari ini\py\report_cell_volte.csv")
   print("Delete report cell volte csv File Success")
else:
    print("File not exist")




if os.path.exists(r"C:\Users\User\Downloads\report_cell_volte.rar"):
   os.remove(r"C:\Users\User\Downloads\report_cell_volte.rar")
   print("Delete Delete report cell volte rar File Success")
else:
    print("File not exist")
