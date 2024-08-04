import requests
from bs4 import BeautifulSoup

url = "https://ru.myfin.by/converter/usd-rub/1"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

def usd_rub():

    rub = soup.find('div', class_='converter-currency__value converter-currency__value--bold')
    return float(rub.text.split(" ")[0])


