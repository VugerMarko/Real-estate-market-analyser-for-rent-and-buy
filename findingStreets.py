from bs4 import BeautifulSoup
import requests
import csv

from config import *


podaci = []
kvartovi = []


def pronadjiKvart():
    

    response = requests.get(url)

    if response.status_code == 200:
        html_code = response.text
        print("Successfully downloaded the page2")

    
    kvartovi = soup.select("li.CategoryListing-topCategoryItem")


    for kvart in kvartovi:
        naziv = kvart.select_one(
            "a.CategoryListing-topCategoryLink"
        ).get_text(strip=True)

        broj = kvart.select_one(
            "span.CategoryListing-entitiesCount"
        ).get_text(strip=True)

        print(naziv, broj)

        podaci.append((naziv, broj))


    with open("kvartovi.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Kvart", "Broj Stanova"])
        writer.writerows(podaci)