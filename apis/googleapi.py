import requests
import json


class GoogleApi(object):
    def __init__(self):
        self.api_key = 'YourAPI'
        self.base_url = "https://maps.googleapis.com/maps/api/"

    def get_geocode(self, lat, lng):
        geocode_information = requests.get("{base_url}geocode/json?latlng={lat},{lng}&key={api_key}".format(base_url=self.base_url, lat=lat, lng=lng, api_key=self.api_key)).json()
        return geocode_information


    def get_country_shortname(self, location_information):
        components = location_information[0]['address_components']
        for component in components:
            if 'country' in component['types'][0]:
                country_shortname = component['short_name']
                return country_shortname
        country="unknown"
        return country

    def get_country_longname(self, location_information):
        components = location_information[0]['address_components']
        for component in components:
            if 'country' in component['types'][0]:
                country = component['long_name']
                return country
        country="unknown"
        return country

    def get_country_language_code(self, country_short_name):
        base_url = "https://restcountries.eu/rest/v2/"
        language_code = requests.get("{base_url}alpha/{country_short_name}".format(base_url=base_url, country_short_name=country_short_name)).json()
        code = language_code['languages'][0]['iso639_1']
        return code

    def shorten_url(self, long_url):
        post_url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(self.api_key)
        payload = {'longUrl': long_url}
        headers = {'content-type': 'application/json'}
        response = requests.post(post_url, data=json.dumps(payload), headers=headers).json()
        short_url = response['id']
        return short_url
