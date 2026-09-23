import csv
import sqlite3
import requests
from bs4 import BeautifulSoup

new_format = None
url_incomplete = "https://www.njuskalo.hr/iznajmljivanje-stanova/"

def nameFormat(name):
    name = name.lower()

    count = 0
        
    for letter in name:
        #print(letter)
        if letter == " ":
            count+=1
            
            
    #name = name.replace(" ", "")
    name = name.replace("š", "s")
    name = name.replace("č", "c")
    name = name.replace("ć", "c")
    name = name.replace("ž", "z")
    name = name.replace("-", " ")
    
    name = "-".join(name.split())
    
    return name

def nameFormatdb(name):
    name = name.lower()

    count = 0
        
    for letter in name:
        #print(letter)
        if letter == " ":
            count+=1
            
            
    #name = name.replace(" ", "")
    name = name.replace("š", "s")
    name = name.replace("č", "c")
    name = name.replace("ć", "c")
    name = name.replace("ž", "z")
    name = name.replace("-", " ")
    
    name = "_".join(name.split())
    
    return name

def userInput():
    user_Input = input("Unesi kvart: ")
    
    formatted = nameFormat(user_Input)
    
    finished = adjacentLink(url_incomplete, formatted)
    
    return finished

def linkMaker(nameof):
    formatted = nameFormat(nameof)
    
    finished = adjacentLink(url_incomplete, formatted)
    
    return finished
    
def adjacentLink(url, name):
    
    completed_url = url + name
    
    return completed_url

    
def create_db(data_list, new_format):
    filename = "stanovviDB.db"
    
    connection = sqlite3.connect(filename)
    
    cursor = connection.cursor()
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{new_format}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ime_oglasa TEXT,
            tip_stana TEXT,
            kat TEXT,
            datum_objave DATE,
            najam INT,
            kvadratura FLOAT,
            link_na_oglas TEXT,
            kvart TEXT,
            podkvart TEXT
        )
    """)
    
    cursor.execute(f"delete from {new_format}")
    
    cursor.executemany(f"""
            INSERT INTO "{new_format}" (
                ime_oglasa, 
                tip_stana,
                kat,
                datum_objave, 
                najam,
                kvadratura,
                link_na_oglas,
                kvart,
                podkvart
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data_list)
    
    print(f"table {new_format} has been created and updated.")
    
    connection.commit()
    connection.close()
    
def create_update_db(data_list, userInput):
    connection = sqlite3.connect("update.db")
    cursor = connection.cursor()
    
    cursor.execute(f"""
        create table if not exists {userInput} (
            id integer primary key autoincrement,
            date_of_update date,
            median int,
            number_of_listings int
        )
    """)
    
    cursor.executemany(f"""
        insert into {userInput} (
            date_of_update,
            median,
            number_of_listings
        )
        values (?, ?, ?)
    """, data_list)
    
    connection.commit()
    connection.close()