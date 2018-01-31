import requests
import json


class WhereTheIss(object):
    def __init__(self):
        self.base_url = "https://api.wheretheiss.at/v1/"

    def get_satellite_location(self, satellite='25544'):
        iss_information = requests.get("{base_url}satellites/{satellite}".format(base_url=self.base_url, satellite=satellite)).json()
        return iss_information
