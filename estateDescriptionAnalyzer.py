import sqlite3
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from userInputSelection import create_update_db

nameDb = "stanovviDB.db"

pd.set_option("display.max_colwidth", None)

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

selected_kvart = ["Donja Dubrava", "Maksimir", "Pešćenica - Žitnjak", "Donji Grad", "Gornji Grad - Medveščak"]

filtered = df[
    (df["kvadratura"] >= 35) &
    (df["kvadratura"] <= 60) &
    (df["najam"] <= 550) &
    (df["kvart"].isin(selected_kvart))
]

""" print(
    filtered[
        ["najam", "kvadratura", "link_na_oglas", "kvart", "podkvart"]
    ]
)
"""
#cijena po m2
df["cijena_po_m2"] = df["najam"] / df["kvadratura"]
#prosjek po odredjenoj kvadraturi
avg = filtered.groupby("kvart")["najam"].min().sort_values()

""" average = df.groupby("kvart").agg(
    najam = ("najam", "mean"),
    kvadratura = ("kvadratura", "mean")
) """

najam_median = df["najam"].median()
najam_min = df["najam"].min()
najam_max = df["najam"].max()

kvadratura_median = df["kvadratura"].median()
kvadratura_min = df["kvadratura"].min()
kvadratura_max = df["kvadratura"].max()


stats = df.groupby("kvart").agg(
    najam_mean=("najam", "mean"),
    najam_median=("najam", "median"),
    najam_min=("najam", "min"),
    najam_max=("najam", "max"),

    kvadratura_mean=("kvadratura", "mean"),
    kvadratura_median=("kvadratura", "median"),
    kvadratura_min=("kvadratura", "min"),
    kvadratura_max=("kvadratura", "max")
)

average = stats[["najam_mean", "kvadratura_mean"]].rename(
    columns={
        "najam_mean": "najam",
        "kvadratura_mean": "kvadratura"
    }
)

x = range(len(average))

width = 0.4


text = (
    f"Najam:\n"
    f"  Median: {najam_median:.0f} €\n"
    f"  Min: {najam_min:.0f} €\n"
    f"  Max: {najam_max:.0f} €\n\n"
    f"Kvadratura:\n"
    f"  Median: {kvadratura_median:.1f} m²\n"
    f"  Min: {kvadratura_min:.1f} m²\n"
    f"  Max: {kvadratura_max:.1f} m²"
)

#prosjecna kvadratura po kvartu
avg_kv = df.groupby("kvart")["kvadratura"].mean().sort_values()
#cijena po m2
cijenapom = df.groupby("kvart")["cijena_po_m2"].mean().sort_values()
#minimalna cijena po kvartu
min_cijena = df.groupby("kvart")["najam"].min().sort_values()
#kolicina oglasa po kvartu
kol = df["kvart"].value_counts()
#prosjecna cijena po kvartu
pros = df.groupby("kvart")["najam"].mean().sort_values()

#save_update("stanovviDB.db", "zagreb")

""" print("\n============= PODACI I ANALIZA PODATAKA ==============")

print('\n=========== Prosjecna kvadratura po kvartu ===========')
print(avg_kv)

print('\n=============== Cijena po m2 po kvartu ===============')
print(cijenapom)

print('\n============= Minimalna cijena po kvartu =============')
print(min_cijena)

print('\n============= Prosjecna cijena po kvartu =============')
print(pros)

print('\n============= Kolicina oglasa po kvartu ==============')
print(kol) """

#graph

fig, ax1 = plt.subplots(figsize=(12, 7))


bars = ax1.bar(
    average.index,
    average["najam"],
    label = "Prosječni najam",
    color="green"
)

ax1.set_ylabel("Najam (€)")
ax1.set_axisbelow(True)

ax2 = ax1.twinx()

ax2.plot(
    average.index,
    average["kvadratura"],
    marker="o",
    label="Prosjecna kvadratura",
    color="red"
)

ax2.set_ylabel("Kvadratura (m²)")

ax1.legend(loc="upper left", bbox_to_anchor=(1.05, 0.95))
ax2.legend(loc="upper left", bbox_to_anchor=(1.05, 0.85))

ax1.tick_params(axis="x", rotation=90)

ax1.grid(
    axis="y",
    linestyle="--",
    alpha=0.3
)

ax1.text(
    1.08,
    0.75,
    text,
    transform=ax1.transAxes,
    verticalalignment="top",
    bbox=dict(
        boxstyle="round",
        alpha=0.8,
        color="gray"
    )
)

plt.title("Najam i kvadratura po kvartu")
plt.tight_layout()

plt.subplots_adjust(right=0.75)
plt.show()

connection.close()