# Imports:
import requests
from bs4 import BeautifulSoup

# Variables:
place = ""
list_of_places = []

# Functions:


def get_url():
    list_of_places.clear()
    get_access = requests.get(
        f"https://www.timeanddate.com/weather/?query={place}"
    ).text
    src = BeautifulSoup(get_access, "html.parser")
    table_data = src.find("table", attrs={"class": "zebra fw tb-theme"})
    all_places = table_data.find_all("tr")
    del all_places[0]
    for i in all_places:
        unedited_name = i.find("td").text
        if unedited_name.endswith(" *") is True:
            edited_name = unedited_name.replace(" *", "")
            list_of_places.append(edited_name)
        else:
            list_of_places.append(unedited_name)
