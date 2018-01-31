import requests
import json


class OceanApi(object):
    def __init__(self):
        self.base_url = "https://geocode-maps.yandex.ru/1.x/"

    def get_ocean_geocode(self, lat, lng):
        ocean_information = requests.get("{base_url}?format=json&sco=latlong&geocode={lat},{lng}&lang=en_US".format(base_url=self.base_url, lat=lat, lng=lng)).json()
        return ocean_information
