import pandas as pd


#baca data 2g dan carrier
df_2g = pd.read_csv("path to files")
df_carrier = pd.read_excel("path to files")

#cek bts Hotel
df_2g["Site_cek"]= df_2g["CellName"].str[2:6]
df_2g["Site_cek_2"] = df_2g["CellName"].str[12:16]

df_2g["Site_ID1"]=df_2g["CellName"].str[2:8]
df_2g["Site_ID2"]=df_2g["CellName"].str[12:18]

#if implementation
df_2g.loc[df_2g['Site_cek'] == df_2g["Site_cek_2"], 'SiteID']=df_2g["Site_ID2"]
df_2g.loc[df_2g['Site_cek'] != df_2g["Site_cek_2"], 'SiteID']=df_2g["Site_ID1"]


#Mendapatkan cell code
df_2g["Cell_Code"] = df_2g["CellName"].str[-3]

# IF UNTUK CELL  CODE
df_2g.loc[df_2g['Cell_Code'] == 'M', 'Cell_Code'] = 'D'
df_2g.loc[df_2g['Cell_Code'] != 'M', 'Cell_Code'] = df_2g["Cell_Code"]

#Merge data 
df_join = pd.merge(df_2g, df_carrier, on="Cell_Code", how="inner")
df_columnz = df_join[["Date","SiteID","carrier","TCH Traffic (Erl)","Total_Payload_GB"]]


#UNTUK SUM 
df_columnz = df_columnz.groupby(['Date','SiteID','carrier']).sum().reset_index()
df_columnz["Sum process"] = df_columnz['TCH Traffic (Erl)']+df_columnz['Total_Payload_GB']

#memilih site kalau traffic + payload = 0 maka hapus
df_columnz.drop(df_columnz[df_columnz['Sum process'] == 0].index, inplace=True)

df_final = df_columnz[["Date","SiteID","carrier","TCH Traffic (Erl)","Total_Payload_GB"]]
df_final.to_csv("path to files", index=None)
print("2g traffic payload Done\n")

