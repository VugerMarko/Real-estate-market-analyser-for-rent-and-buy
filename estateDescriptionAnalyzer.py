import sqlite3
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from userInputSelection import create_update_db

nameDb = "stanovviDB.db"

update_list = []

connection = sqlite3.connect(nameDb)
cursor = connection.cursor()

cursor.execute(f"""
    select *
    from zagreb
""")

data_table = cursor.fetchall()


cursor.execute("""
    select *
    from updates
""")

update_data = cursor.fetchall()

def save_update(dbname, tablename):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    
    cursor.execute(f"""
        select najam
        from {tablename}
    """)
    
    median = df["najam"].mean()
    today = datetime.today()
    
    update_list.append((
        today,
        median
    ))
    
    create_update_db(update_list)
    
    print("update list updated.")
    
    connection.close()
    
def delete_table():
    userInput = input("enter the table you want to delete: ")
    
    connection = sqlite3.connect("stanoviDB.db")
    cursor = connection.cursor()
    
    cursor.execute(f"drop table if exists {userInput}")
    
    connection.commit()
    connection.close()
    
    print(f"the table called {userInput} has been deleted.")

columns = [description[0] for description in cursor.description]

df = pd.DataFrame(data_table, columns=columns)

kv = 35

filtered = df[df["kvadratura"] == kv]

#cijena po m2
df["cijena_po_m2"] = df["najam"] / df["kvadratura"]
#prosjek po odredjenoj kvadraturi
avg = filtered.groupby("kvart")["najam"].min().sort_values()
#cijena po m2
cijenapom = df.groupby("kvart")["cijena_po_m2"].mean().sort_values()

save_update("stanovviDB.db", "zagreb")

connection.close()
    
