import csv
import sqlite3
import requests
from bs4 import BeautifulSoup
import math
import matplotlib
import pandas as pd


def openConnectionDb():
    connection = sqlite3.connect("stanoviDB.db")
    cursor = connection.cursor()

    user_input_table = input("Unesi tablicu: ")

    cursor.execute(f"select * from {user_input_table}")

    data = cursor.fetchall()

    for row in data:
        print(row)
        
    connection.close()
    
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
