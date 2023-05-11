import patoolib
from datetime import date
from datetime import timedelta
import os
import shutil
import pandas as pd
import numpy as np
import MySQLdb

conn=MySQLdb.connect(host="your host", user="your username", password="your password", database="your db", port="your port")
import time
start_time = time.time()

#get todays date
today = date.today()
yesterday = today - timedelta(days=1) 
yesterday_choose = yesterday.strftime("%Y%m%d")

#extract rar file
patoolib.extract_archive(r"your location"+" "+yesterday_choose+".rar", outdir=r"outdir location")
print("Extract Success")
#move rar file
source_4g = r"original source"+" "+yesterday_choose+".rar"
move_path = r'Destination sourceS'
shutil.move(source_4g, move_path)

#renaming csv
old_name='original source'+' '+yesterday_choose+'.xlsm'
new_name='destination source\\4G.xlsm'

os.rename(old_name, new_name)
print("Change Name Success")

columns = ["SELECTED COLUMN NAME"]

#read_4g
df = pd.read_excel(r"4G file source",sheet_name="Sheet name", usecols=columns)

df["Total_Payload_GB"] = df["Total Payload (MB)"].div(1024)

#cek bts hotel
df["Site_cek"]= df["Cell Name"].str[2:6]
df["Site_cek_2"] = df["Cell Name"].str[12:16]

df["Site_ID1"]=df["Cell Name"].str[2:8]
df["Site_ID2"]=df["Cell Name"].str[12:18]

#if implementation
df.loc[df['Site_cek'] == df["Site_cek_2"], 'SiteID']=df["Site_ID2"]
df.loc[df['Site_cek'] != df["Site_cek_2"], 'SiteID']=df["Site_ID1"]

df = df[['Selected column']]
df.fillna('\\N',inplace=True)
df.to_csv(r"Destination location", index=None)
print("Excel to csv done")






cursor = conn.cursor()
sql = "LOAD DATA LOCAL INFILE 'location file/4G.csv' INTO TABLE 4g FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES"
cursor.execute(sql)
conn.commit()
cursor.close()
print(cursor.rowcount, 'Was inserted')
print("4G Done")
end_time = time.time()

elapsed_time = round((end_time - start_time)/60,2)
print(f"Elapsed time: {elapsed_time} Minutes")
