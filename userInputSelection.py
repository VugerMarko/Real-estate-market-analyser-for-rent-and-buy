import csv
import sqlite3
import requests
from bs4 import BeautifulSoup


url_incomplete = "https://www.njuskalo.hr/iznajmljivanje-stanova/"

new_format = ""

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

def formatter(str):
    new_format = str
    return new_format

def userInput():
    user_Input = input("Unesi kvart: ")
    
    found = False
    
    with open("kvartovi.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row["Kvart"] == user_Input:
                print("Found: ", row["Kvart"])
                print("Num of apartments: ", row["Broj Stanova"])
                found = True
                break
        
        if not found:
            print("Name not found")
    
    formatted = nameFormat(user_Input)
    
    finished = adjacentLink(url_incomplete, formatted)
   
    formatter(formatted)
    
    return finished
    
def adjacentLink(url, name):
    
    completed_url = url + name
    
    return completed_url

def create_csv(data_list):
    filename = f"{new_format}.csv"
    
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow([
            "Ime oglasa",
            "Opis",
            "Datum oglašenja",
            "Najam",
            "Link oglasa"
        ])
        
        writer.writerows(data_list)