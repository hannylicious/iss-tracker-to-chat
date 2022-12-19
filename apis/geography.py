import requests
import json
import os


class GeographyInformation(object):
    def __init__(self):
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        self.radar_api_key = os.environ.get("RADAR_API_KEY")
        self.location_iq_api_key = os.environ.get("LOCATION_IQ_API_KEY")
        self.geoapify_api_key = os.environ.get("GEOAPIFY_API_KEY")
        self.yandex_maps_api_url = "https://geocode-maps.yandex.ru/1.x/"
        self.google_maps_api_url = "https://maps.googleapis.com/maps/api/"
        self.radar_api_url = "https://api.radar.io/v1/geocode/reverse?"
        self.location_iq_api_url = "https://us1.locationiq.com/v1/reverse"
        self.geoapify_api_url = "https://api.geoapify.com/v1/geocode/reverse"
        self.restcountries_api_url = "https://restcountries.com/v3.1/"

    def get_geocode(self, lat, lng):
        # Radar API seems down (12/7/22)
        # headers = {"Authorization": self.radar_api_key}
        # geocode_information = requests.get(
        #     "{base_url}coordinates={lat},{lng}".format(
        #         base_url=self.radar_api_url,
        #         lat=lat,
        #         lng=lng,
        #     ),
        #     headers=headers
        # ).json()
        # Location IQ API
        # data = {
        #     'key': str(self.location_iq_api_key),
        #     'lat': str(lat),
        #     'lon': str(lng),
        #     'format': 'json'
        # }
        # breakpoint()
        # geocode_information = requests.get(url=self.location_iq_api_url, params=data)
        # GEOAPIFY API
        data = {
            'lat': str(lat),
            'lon': str(lng),
            'format': 'json',
            'apiKey': str(self.geoapify_api_key),
        }
        geocode_information = requests.get(url=self.geoapify_api_url, params=data).json()
        return geocode_information

    def get_ocean_geocode(self, lat, lng):
        ocean_information = requests.get(
            "{base_url}?format=json&sco=latlong&geocode={lat},{lng}&lang=en_US".format(
                base_url=self.yandex_maps_api_url, lat=lat, lng=lng
            )
        ).json()
        return ocean_information

    def get_country_language_code(self, country_short_name):
        language_code = requests.get(
            "{base_url}alpha/{country_short_name}".format(
                base_url=self.restcountries_api_url, country_short_name=country_short_name
            )
        ).json()
        breakpoint()
        code = language_code["languages"][0]["iso639_1"]
        return code

    def get_country_shortname(self, location_information):
        components = location_information[0]["address_components"]
        for component in components:
            if "country" in component["types"][0]:
                country_shortname = component["short_name"]
                return country_shortname
        country = "unknown"
        return country

    def get_country_longname(self, location_information):
        components = location_information[0]["address_components"]
        for component in components:
            if "country" in component["types"][0]:
                country = component["long_name"]
                return country
        country = "unknown"
        return country

    def shorten_url(self, long_url):
        post_url = "https://www.googleapis.com/urlshortener/v1/url?key={}".format(
            self.google_api_key
        )
        payload = {"longUrl": long_url}
        headers = {"content-type": "application/json"}
        response = requests.post(
            post_url, data=json.dumps(payload), headers=headers
        ).json()
        short_url = response["id"]
        return short_url
