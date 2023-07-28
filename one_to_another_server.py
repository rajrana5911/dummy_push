import mysql.connector
dest_db = mysql.connector.connect(
  host="3.140.57.116",
  user="wp_raj1",
  password="rajPassword95$",
  database="url_automation"
)

# Connect to destination database
source_db = mysql.connector.connect(
  host="64.227.176.243",
  user="phpmyadmin",
  password="Possibilities123.@",
  database="url_automation"
)

# Retrieve data from source database
with source_db.cursor() as cursor:
    cursor.execute('SELECT * FROM bulk_quill_bank where status is null and bqt_id = 52')
    data = cursor.fetchall()

# Insert data into destination database
with dest_db.cursor() as cursor:
    count=0   
    for row in data:
        print(row[1])
        cursor.execute('INSERT INTO bulk_quill_bank VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)', row)
        count+=1
    print(count)
    dest_db.commit()

# Close database connections
source_db.close()
dest_db.close()
