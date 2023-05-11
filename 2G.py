import patoolib
import shutil
from datetime import date
from datetime import timedelta
import os
import pandas as pd
import numpy as np
import MySQLdb
conn=MySQLdb.connect(host="", user="", password="", database="", port="")
import time
start_time = time.time()

# notes: df=data frame
# get todays date
today = date.today()
yesterday = today - timedelta(days=1) 
yesterday_choose = yesterday.strftime("%Y%m%d")

#extract rar file
patoolib.extract_archive(r"location\2G NG-Tinem_Daily Performance Report_"+yesterday_choose+".rar", outdir=r"location")
print("extract success")

#move files
source_2g = r"location\2G NG-Tinem_Daily Performance Report_"+yesterday_choose+".rar"
move_source = r'location'
shutil.move(source_2g, move_source)

#renaming xlsx
old_name='location'+yesterday_choose+'.xls'
new_name='location\\2G.xls'

os.rename(old_name, new_name)
print("renaming success")
#Choose Cell daily and export it into xlsx
columns = ["selected column name"]
df = pd.read_excel(r"location\2G.xls",sheet_name="Cell Daily", usecols=columns)
print("Choosing column success")

#processing payload
df["TOTAL_PAYLOAD_MByte"] = df["EDGE Payload New(Mbyte)"] + df["GPRS Payload New(Mbyte)"]
df["Total_Payload_GB"] = df["TOTAL_PAYLOAD_MByte"].div(1024)


#renaming Column
df["Date"]=pd.to_datetime(df["Date"]).dt.date


#processing into database
df = df[["Selected column name"]]
df.fillna('\\N',inplace=True)
df.to_csv(r"location\2G.csv", index=None)
print("Excel to csv done")

cursor = conn.cursor()
sql = "LOAD DATA LOCAL INFILE 'location/2G.csv' INTO TABLE 2g FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES"
cursor.execute(sql)
conn.commit()
cursor.close()
print(cursor.rowcount, 'Was inserted')
print("2G Done")

#remove old excel file
if os.path.exists(r"location\2G.xls"):
   os.remove(r"location\2G.xls")
   print("Remove file success")
else:
    print("File not exist")
end_time = time.time()

elapsed_time = round((end_time - start_time)/60,2)
print(f"Elapsed time: {elapsed_time} minutes")