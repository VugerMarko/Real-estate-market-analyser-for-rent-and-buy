import csv
import sqlite3
import requests
from bs4 import BeautifulSoup


url_incomplete = "https://www.njuskalo.hr/iznajmljivanje-stanova/"

def nameFormat(name):
    name = name.lower()

    name = name.replace("š", "s")
    name = name.replace("č", "c")
    name = name.replace("ć", "c")
    name = name.replace("ž", "z")
    name = name.replace("-", "")
    
    name = name.replace(" ", "-")
    
    return name

def userInput():
    user_Input = input("Unesi kvart: ")
    
    with open("kvartovi.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row["Kvart"] == user_Input:
                print("Found: ", row["Kvart"])
                print("Num of apartments: ", row["Broj Stanova"])
            else:
                print("Name not found")
                break
                
    
    print(nameFormat(user_Input))
    