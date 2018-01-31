import requests
import time
import json
import random
import string
import socket
import time
import re
from apis.wheretheiss import WhereTheIss
from apis.googleapi import GoogleApi
from apis.oceanapi import OceanApi
from apis.wordsapi import WordsApi
from apis.twitchapi import TwitchApi

def track_iss(iss_api, google_api, ocean_api, words_api, twitch_api):
    chosen_word = get_random_word_from_list()
    word_definition = words_api.get_definition(chosen_word)
    iss_information = iss_api.get_satellite_location()
    current_iss_location = google_api.get_geocode(lat=iss_information['latitude'],lng=iss_information['longitude'])
    if current_iss_location['results']:
        # It's over land!
        country_shortname = google_api.get_country_shortname(current_iss_location['results'])
        country_longname = google_api.get_country_longname(current_iss_location['results'])
        language_code = google_api.get_country_language_code(country_shortname)
        translated_word = words_api.get_translation(chosen_word, language_code)
        comment = 'The ISS is over {country_longname} - want to translate a word into their native language? The English word is: "{chosen_word}" - this translates to {translated_word}'.format(country_longname=country_longname, chosen_word=chosen_word, translated_word=translated_word)
        sock = TwitchApi.connect()
        TwitchApi.chat(sock, comment)

    else:
        # It's over the ocean!
        iss_ocean_location = ocean_api.get_ocean_geocode(lat=iss_information['latitude'],lng=iss_information['longitude'])
        if iss_ocean_location['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind'] == 'hydro':
            #confirmed water
            ocean_name = iss_ocean_location['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            lat_long_str = str(iss_information['latitude'])+','+str(iss_information['longitude'])
            map_link = 'https://maps.google.com/maps?q={lat_long_str}'.format(lat_long_str=lat_long_str)
            map_link = ''.join(map_link.split())
            short_url = google_api.shorten_url(map_link)
            comment = "Bummer for you - the ISS is currently over the {ocean_name} (it's actually right here:{map_link}), which doesn't have a proper language, so I can't provide you with a cool translation. Sorry!".format(ocean_name=ocean_name, map_link=short_url)
            sock = TwitchApi.connect()
            TwitchApi.chat(sock, comment)

    time.sleep(600)


def get_random_word_from_list():
    with open('wordlist.txt', 'r') as file:
        words = [line.strip() for line in file]
    random_word = random.choice(words)
    return random_word


if __name__ == "__main__":
    iss_api = WhereTheIss()
    google_api = GoogleApi()
    ocean_api = OceanApi()
    words_api = WordsApi()
    twitch_api = TwitchApi()
    while True:
        track_iss(iss_api=iss_api, google_api=google_api, ocean_api=ocean_api, words_api=words_api, twitch_api=twitch_api)
