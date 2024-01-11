import json
import requests
from requests import get


def get_location():
    ip = get('https://api.ipify.org').text
    send_url = (
        "http://ipwhois.app/json/{}".format(ip)
    )
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    city = geo_json["city"]
    country = geo_json["country"]
    return city, country


if __name__ == "__main__":
    print(get_location())
