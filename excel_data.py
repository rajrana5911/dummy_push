import pandas as pd
# this is my code work
import mysql.connector
mydb = mysql.connector.connect(
  host="3.140.57.116",
  user="wp_raj1",
  password="rajPassword95$",
  database="url_automation"
)
category=input("enter the category: ")
file_name=input("enter the file name: ")
# read by default 1st sheet of an excel fileH:\automation_scripts\url_from_excel_to_database\skenews.csv
df = open(f'/home/ubuntu/article_automation/{file_name}','r',encoding='utf-8')

count=0
for i in df:

    mycursor = mydb.cursor()
    # mycursor.execute("SELECT * FROM bulk_quill_bank ")
    # myres = mycursor.fetchall()

    new_sql_date ="insert into bulk_quill_bank(url,bqt_id,Category) values(%s,%s,%s)"
    new_val_of_data = (i,64,category)
    mycursor.execute(new_sql_date, new_val_of_data)
    mydb.commit()
    count+=1
    print(count,i)
    if count==10:
        break
  
print("done")
print("work has been done")
print("work has been done")