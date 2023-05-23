import pandas as pd
from datetime import date
from datetime import timedelta
import shutil

#get todays date
today = date.today()
yesterday = today - timedelta(days=1) 
yesterday_choose = yesterday.strftime("%Y%m%d")

nama_file="5G_KPI_DASHBOARD_TELKOMSEL_Cluster_5G_SS_"+yesterday_choose+".xlsm"
source_5g = "path to files"+nama_file
move_path = r'path to files'
shutil.move(source_5g, move_path)

df_5g = pd.read_excel('path to files'+nama_file,sheet_name='cell daily')
df_5g["Site_cek"]= df_5g["Cell Name"].str[2:6]
df_5g["Site_cek_2"] = df_5g["Cell Name"].str[12:16]

df_5g["Site_ID1"]=df_5g["Cell Name"].str[2:8]
df_5g["Site_ID2"]=df_5g["Cell Name"].str[12:18]

#if implementation
df_5g.loc[df_5g['Site_cek'] == df_5g["Site_cek_2"], 'SiteID']=df_5g["Site_ID2"]
df_5g.loc[df_5g['Site_cek'] != df_5g["Site_cek_2"], 'SiteID']=df_5g["Site_ID1"]
df_5g['Band']='NR2100'
df_5g=df_5g[['date','SiteID','Band','RLC_Payload']]
df_5g= df_5g.groupby(['date','SiteID','Band']).sum().reset_index()
df_5g['Traffic_ERL']=None
df_5g=df_5g[['date','SiteID','Band','Traffic_ERL','RLC_Payload']]
print(df_5g)
df_5g.to_csv("path to files", index=None)
print("5G Done")

