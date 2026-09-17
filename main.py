#basic libraries
from bs4 import BeautifulSoup
import csv
from datetime import datetime

#custom libraries
from userInputSelection import *
from estateDescriptionAnalyzer import save_update

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

        data.append((name, num_of_apartments))


    with open("kvartovi.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Kvart", "Broj Stanova"])
        writer.writerows(data)

    #input("Press enter to close the browser...")    

    entity_data = []
    for kvart, broj_stanova in data:
        dbname = nameFormatdb(kvart)
        custom_link = linkMaker(kvart)
    
        page.goto(url=custom_link)
        html_code = page.content()
        j = 0
        
        seen_links = set()
        
        for page_num in range(1, 50):
            if page_num == 1:
                new_url = custom_link
            else:
                new_url = f"{custom_link}?page={page_num}"
            
            print("\n=============================")
            print("Page number: ", page_num)
            print("Going to: ", new_url)
            
            page.goto(new_url)
            
            page.wait_for_load_state("domcontentloaded")
            
            if "validate.perfdrive.com" in page.url:
                print("Njuskalo requested verification.")
                print("Stopping scraper.")
                print(page.url)
                break
            
            print("Actual URL: ", page.url)
            
            entity_list = page.locator("li.EntityList-item:has(div.entity-description)")
            
            listing_count = entity_list.count()
            
            try:
                entity_list.first.wait_for(
                    state="visible",
                    timeout=10000
                )
            except:
                print(f"No listings on page {page_num}. stopping...")
                break
            
            if listing_count == 0:
                print(f"No listings on page {page_num}. stopping...")
                break
            
            real_listing = 0
            
            for i in range(listing_count):
                entity = entity_list.nth(i)
                
                #name finder
                name_locator = entity.locator("h3.entity-title a.link")
                
                if name_locator.count() > 0:
                    name = name_locator.inner_text()
                else:
                    name = "N/A"
                    
                #link finder
                link_locator = entity.locator("h3.entity-title a.link")
                
                if link_locator.count() == 0:
                    continue
                
                link = link_locator.get_attribute("href")
                
                if not link:
                    continue
                
                link = "https://www.njuskalo.hr" + link
                
                if link in seen_links:
                    continue
                #price finder
                price_locator = entity.locator("strong.price.price--hrk")
                
                if price_locator.count() > 0:
                    price = price_locator.inner_text()
                    
                    price = (
                        price.replace("€", "")
                            .replace(".", "")
                            .replace(",", ".")
                            .strip()
                    )
                    price = int(price)
                    
                    if price < 300 or price > 10000:
                        continue
                else:
                    continue
                
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
                    time = datetime.strptime(time, "%d.%m.%Y.").date()
                else:
                    continue
                
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
                    
                    if not lokacija or "," not in lokacija:
                        continue
                    
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
                    
                    
                    kvadratura = kvadratura.replace("m2", "")
                        
                    kvadratura = float(kvadratura)
                else:
                    continue
                
                print("kvadratura: ", kvadratura)
                
                real_listing += 1
                
                seen_links.add(link)
                j += 1
                
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
            
            print("listing count: ", listing_count)
            print("real listings: ", real_listing)
            if real_listing == 0:
                print("No listings found. Stopping.")
                break
            
    browser.close()

data_name = ""

create_db(entity_data)
save_update("stanovviDB.db", "zagreb")
