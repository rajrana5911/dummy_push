import pandas as pd
import mysql.connector
import os
import csv

current_working_folder = (os.path.realpath(os.path.dirname(__file__)))
current_working_file=__file__
# print(current_working_file)
mydb = mysql.connector.connect(
  host="3.140.57.116",
  user="wp_raj1",
  password="rajPassword95$",
  database="url_automation"
)
number_of_files = int(input('Enter the number of files: '))
file_name_and_bqt_id = {}

for i in range(number_of_files):
    file_name = input('Enter the name of file: ')
    bqt_id = input('Enter the bqt_id of source: ')
    file_name_and_bqt_id[file_name] = bqt_id

# print(file_name_and_bqt_id)

# print(type(file_name_and_bqt_id))
# read by default 1st sheet of an excel fileH:\automation_scripts\url_from_excel_to_database\skenews.csv
for i in file_name_and_bqt_id.items():
    with open(f'{current_working_folder}\\{i[0]}','r',encoding='utf-8') as file:
          reader = csv.reader(file)
          for row in reader:
              mycursor = mydb.cursor()
              mycursor.execute("SELECT * FROM bulk_quill_bank ")
              myres = mycursor.fetchall()
              new_sql_date ="insert into bulk_quill_bank(url,bqt_id) values(%s,%s)"
              new_val_of_data = (row[0],i[1])
              mycursor.execute(new_sql_date, new_val_of_data)
              mydb.commit()
              print(row[0],f'is inserted where bqt_id = {i[1]}')
#    if count==50:

print("done")
# print(dataframe1)