#basic libraries
from bs4 import BeautifulSoup
import requests
import math
import csv
import pandas as pd
import numpy as np
import sqlite3
import matplotlib

#custom libraries
from findingStreets import *
from config import *

#unique libraries 
from playwright.sync_api import sync_playwright



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)

    #page.wait_for_timeout(1000)

    html_code = page.content()

    print("CategoryListing-topCategoryLink" in html_code)

    browser.close()



pronadjiKvart()