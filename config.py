import requests
from bs4 import BeautifulSoup



url = "https://www.njuskalo.hr/iznajmljivanje-stanova/zagreb"

response = requests.get(url)

if response.status_code == 200:
    html_code = response.text
    print("Successfully downloaded the page")

soup = BeautifulSoup(html_code, "html.parser")