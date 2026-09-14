import sqlite3
from bs4 import BeautifulSoup
import math
import matplotlib
import pandas as pd

def delete_table():
    userInput = input("enter the table you want to delete: ")
    
    connection = sqlite3.connect("stanoviDB.db")
    cursor = connection.cursor()
    
    cursor.execute(f"drop table if exists {userInput}")
    
    connection.commit()
    connection.close()
    
    print(f"the table called {userInput} has been deleted.")

def find_desired_rent_price(max_price):
    #I will come back to this at a later dates
    return 0

connection = sqlite3.connect("stanovviDB.db")
cursor = connection.cursor()


cursor.execute(f"""
    select najam, kvadratura
    from podatci
""")

rows = cursor.fetchall()

i = 0

for row in rows:
    print(f"Kvadratura: {row[0]} | Najam: {row[1]}")
    i += 1

print(i)

connection.close()
    
