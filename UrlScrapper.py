from bs4 import BeautifulSoup
import requests

place = ''
index = 0


def scrape_url():
    global url_prefix
    url = requests.get(
        f"https://www.timeanddate.com/weather/?query={place}").text
    source = BeautifulSoup(url, 'html.parser')
    table = source.find("table", attrs={"class": "zebra fw tb-theme"})
    all_places = table.find_all('tr')
    place_data = all_places[index + 1]
    link = place_data.find('a')
    url_prefix = link.get('href')
