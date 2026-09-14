import sqlite3
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
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
    select *
    from podatci
""")

data_table = cursor.fetchall()

columns = [description[0] for description in cursor.description]

df = pd.DataFrame(data_table, columns=columns)

kv = 115

filtered = df[df["kvadratura"] == kv]

#cijena po m2
df["cijena_po_m2"] = df["najam"] / df["kvadratura"]


#prosjek po odredjenoj kvadraturi
avg = filtered.groupby("kvart")["najam"].mean().sort_values()

#wish = df[df["link_na_oglas"] == "https://www.njuskalo.hr/nekretnine/vrhovec-luksuzan-6s-stan-duplom-garazom-terasom-pogledom-grad-oglas-50461264"]
#print(wish)

#cijena po m2
cijenapom = df.groupby("kvart")["cijena_po_m2"].mean().sort_values()
print("\n=========== Cijena po m2 ===========")
print(cijenapom)
print("\n==== Prosjecna cijena po kvartu ====")
print(avg)

bars = plt.bar(cijenapom.index, cijenapom.values)

plt.bar_label(bars, fmt="%.2f€", padding=3)

plt.title(f"Cijena po m2")
plt.ylabel("Cijena (€)")
plt.xlabel("Kvart")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()

connection.close()
    
