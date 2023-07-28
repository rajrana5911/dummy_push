# import pandas lib as pd
import pandas as pd
import mysql.connector
mydb = mysql.connector.connect(
  host="64.227.176.243",
  user="phpmyadmin",
  password="Possibilities123.@",
  database="url_automation"
)
# read by default 1st sheet of an excel fileH:\automation_scripts\url_from_excel_to_database\skenews.csv
df = open(r'H:\automation_scripts\url_from_excel_to_database\swadeshibuzz.csv','r',encoding='cp1252')

count=0
for i in df:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bulk_quills ")
    myres = mycursor.fetchall()
    new_sql_date ="insert into bulk_quills(url,bqt_id) values(%s,%s)"
    new_val_of_data = (i,5)#total+prev_post[cou]
    mycursor.execute(new_sql_date, new_val_of_data)
    mydb.commit()
    count+=1
    if count==25:
        break
print("done")
# print(dataframe1)
