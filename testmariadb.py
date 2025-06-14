#!/usr/bin/python 
import mariadb 

conn = mariadb.connect(
    user="root",
    password="ilikemarciee3",
    host="localhost",
    database="employees")
cur = conn.cursor() 

#retrieving information 
c = int(input("Type 1 to shibal: "))
if c == 1:
    
    some_name = "Georgi" 
    cur.execute("SELECT first_name,last_name FROM employees WHERE first_name=?", (some_name,)) 

    for first_name, last_name in cur: 
        print(f"First name: {first_name}, Last name: {last_name}")
    
#insert information 
try: 
    cur.execute("INSERT INTO employees (first_name,last_name) VALUES (?, ?)", ("Maria","DB")) 
except mariadb.Error as e: 
    print(f"Error: {e}")

conn.commit() 
print(f"Last Inserted ID: {cur.lastrowid}")
    
conn.close()