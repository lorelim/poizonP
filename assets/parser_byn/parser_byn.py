import requests
from bs4 import BeautifulSoup

url = "https://myfin.by/converter/usd-byn/1"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

def usd_byn():

    byn = soup.find('span', class_='converter-100__info-currency-bold')
    return float(byn.text.split(" ")[0])

