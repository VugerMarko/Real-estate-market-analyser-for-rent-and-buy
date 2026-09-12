#basic libraries
from bs4 import BeautifulSoup
import requests
import math
import csv
import pandas as pd
import numpy as np
import sqlite3
import matplotlib


#unique libraries 
from playwright.sync_api import sync_playwright

url = "https://www.njuskalo.hr/iznajmljivanje-stanova/zagreb"

response = requests.get(url)

if response.status_code == 200:
    html_code = response.text
    print("Successfully downloaded the page")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)
    html_code = page.content()

    print("CategoryListing-topCategoryLink" in html_code)

    browser.close()

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

    print(name, num_of_apartments)

    data.append((name, num_of_apartments))


with open("kvartovi.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Kvart", "Broj Stanova"])
    writer.writerows(data)

