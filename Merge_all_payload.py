import pandas as pd
import numpy as np
import os
import MySQLdb
conn=MySQLdb.connect(host="", user="", password="", database="", port=3308)



#remove old excel file
if os.path.exists("path to files"):
   os.remove("path to files")
   print("Delete FIle Success")
else:
    print("File not exist")

collect_pay = pd.read_excel("path to files")
df_2g = pd.read_csv("path to files")
df_5g = pd.read_csv("path to files")
df_4g = pd.read_csv("path to files")


df_all = pd.DataFrame(np.concatenate([df_2g,df_5g,df_4g]), columns=collect_pay.columns)
df_all.to_excel("path to files", index=None)
print("Merge Done!")


df_csv = pd.read_excel("path to files")
df_all.fillna('\\N', inplace=True)
df_csv.to_csv("path to files", index=None)

#Check total paylaod & traffic
df_check = pd.read_csv("path to files")
df_check = df_check.groupby('VP_Date').agg({'Traffic_ERL': 'sum', 'Payload_GB': 'sum'}).reset_index()
print(df_check)

cursor = conn.cursor()
sql = "LOAD DATA LOCAL INFILE 'path to files' INTO TABLE traffic_payload_2023 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES"
cursor.execute(sql)
conn.commit()
cursor.close()
print(cursor.rowcount, 'Was inserted')
print("Traffic Payload Done!")
