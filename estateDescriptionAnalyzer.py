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
    
    return 0

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

#wish = df[df["link_na_oglas"] == "https://www.njuskalo.hr/nekretnine/vrhovec-luksuzan-6s-stan-duplom-garazom-terasom-pogledom-grad-oglas-50461264"]
#print(wish)



#cijena po m2
cijenapom = df.groupby("kvart")["cijena_po_m2"].mean().sort_values()
print("\n=========== Cijena po m2 ===========")
print(cijenapom)
print("\n==== Prosjecna cijena po kvartu ====")
print(avg)

bars = plt.bar(avg.index, avg.values)

plt.bar_label(bars, fmt="%.2f€", padding=3)

plt.title(f"Cijena po m2")
plt.ylabel("Cijena (€)")
plt.xlabel("Kvart")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()
#plt.show()

connection.close()
    
