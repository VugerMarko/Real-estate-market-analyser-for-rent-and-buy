#basic libraries
from bs4 import BeautifulSoup
import requests
import math
import csv
import pandas as pd
import numpy as np
import sqlite3
import matplotlib

from userInputSelection import userInput
from userInputSelection import create_db

#unique libraries 
from playwright.sync_api import sync_playwright

url = "https://www.njuskalo.hr/iznajmljivanje-stanova/zagreb"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)
    html_code = page.content()

    soup = BeautifulSoup(html_code, "html.parser")

    streets = []
    streets = soup.select("li.CategoryListing-topCategoryItem")

    data = []

    for street in streets:
        name = street.select_one(
            "a.CategoryListing-topCategoryLink"
        ).get_text(strip=True)

        num_of_apartments = street.select_one(
            "span.CategoryListing-entitiesCount"
        ).get_text(strip=True)

        #print(name, num_of_apartments)

        data.append((name, num_of_apartments))


    with open("kvartovi.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Kvart", "Broj Stanova"])
        writer.writerows(data)

    output = userInput()

    print(output)

    page.goto(url=output)
    html_code = page.content()
        
    input("Press enter to close the browser...")    

    entity_data = []
        
    j = 0    
        
    
        
    for page_num in range(1, 22):
        if page_num == 1:
            new_url = output
        else:
            new_url = f"{output}?=page{page_num}"
        page.goto(new_url)
        page.wait_for_selector("li.EntityList-item")
        
        entity_list = page.locator("li.EntityList-item:has(div.entity-description)")
        
        for i in range(entity_list.count()):
            entity = entity_list.nth(i)
            j = j + 1
            #name finder
            name_locator = entity.locator("h3.entity-title a.link")
            
            if name_locator.count() > 0:
                name = name_locator.inner_text()
            else:
                name = "N/A"
                
            #link finder
            link_locator = entity.locator("h3.entity-title a.link")
            
            if link_locator.count() > 0:
                link = link_locator.get_attribute("href")
                link = "https://www.njuskalo.hr" + link if link else "N/A"
            else:
                link = "N/A"
            
            #price finder
            price_locator = entity.locator("strong.price.price--hrk")
            
            if price_locator.count() > 0:
                price = price_locator.inner_text()
            else:
                price = "N/A"
            
            #info finder
            info_locator = entity.locator("div.entity-description")
            
            if info_locator.count() == 0:
                    continue
            
            info = info_locator.inner_text()
            
            info_parts = [part.strip() for part in info.split("\n") if part.strip()]

            #release date finder
            time_locator = entity.locator("time.date.date--full")

            if time_locator.count() > 0:
                time = time_locator.inner_text()
            else:
                time = "N/A"
            
            #more info locator
            kat = None
            tip_stana = None
            stan = None
            
            for part in info_parts:
                if part.startswith("Stan u stambenoj zgradi,") or part.startswith("Stan u kući,"):
                    stan = part
                    break
            
            if stan:
                tip_stana, kat = stan.split(",", 1)
                tip_stana = tip_stana.strip()
                kat = kat.strip()
            else:
                tip_stana = "N/A"
                kat = "N/A"
                
            print("Tip stana: ", tip_stana)
            print("Kat: ", kat)
            #street locator
            lokacija = None
            
            for part in info_parts:
                if part.startswith("Lokacija:"):
                    lokacija = part
                    break
            
            if lokacija:
                lokacija = lokacija.replace("Lokacija:", "").strip()
                
                kvart, podkvart = lokacija.split(",", 1)
                
                kvart = kvart.strip()
                podkvart = podkvart.strip()
            else:
                kvart = lokacija
                podkvart = "N/A"
            
            print(
                "Kvart: ", kvart,
                "\npodkvart: ", podkvart
            )
            
            #livable space finder
            
            kvadratura = None
            
            for part in info_parts:
                if part.startswith("Stambena površina:"):
                    kvadratura = part
                    break
            
            if kvadratura:
                kvadratura = kvadratura.replace("Stambena površina:", "").strip()
                
                kvadratura = kvadratura.strip()
            else:
                kvadratura = "N/A"
            
            print("kvadratura: ", kvadratura)
            
            
            #output
            print("Page: ", page_num)
            print("Listing: ", j)
            print(
                "Listing name: ", name, 
                "\napartment info:", info_parts,
                "\ndate of release:", time,
                "\nmonthly rent: ", price,
                "\nlisting link: ", link
            )
            
            entity_data.append((
                name, 
                tip_stana,
                kat,
                time,
                price,
                kvadratura,
                link,
                kvart,
                podkvart
            ))
            
    browser.close()

data_name = ""

create_db(entity_data)