import requests

from apis.iss import Iss
from apis.geography import GeographyInformation
from apis.wordsapi import Dictionary
from apis.twitchapi import TwitchApi
import random
import time

def shorten_url(url) -> str:
    """
    Takes a 'long url' and makes a call to GoTiny API to return a shortened URL
    :param url:
    :return:
    """
    short_url = requests.post(
        "https://gotiny.cc/api",
        json={'input': url}
    ).json()
    return short_url[0]['code']

def track_iss(iss, geography, dictionary):
    chosen_word = get_random_word_from_list()
    word_definition = dictionary.get_definition(chosen_word)
    iss_satellite_information = iss.get_satellite_location()
    current_iss_location = geography.get_geocode(
        lat=iss_satellite_information["latitude"], lng=iss_satellite_information["longitude"]
    )
    try:
        country = current_iss_location['results'][0]['country']
    except KeyError:
        country = None
    if country:
        # It's over land!
        country_shortname = current_iss_location["results"][0]["countryCode"]
        language_code = geography.get_country_language_code(country_shortname)
        translated_word = dictionary.get_translation(chosen_word, language_code)
        comment = 'The ISS is over {country} - want to translate a word into their native language? The English word is: "{chosen_word}" - this translates to {translated_word}'.format(
            country=country,
            chosen_word=chosen_word,
            translated_word=translated_word,
        )
        sock = TwitchApi.connect()
        TwitchApi.chat(sock, comment)
    else:
        address_label_name = current_iss_location['results'][0]['name']
        if "Ocean" in address_label_name or "Sea" in address_label_name:
            # It's over the ocean!
            # confirmed water
            lat_long_str = (
                    str(iss_satellite_information["latitude"])
                    + "%2C"
                    + str(iss_satellite_information["longitude"])
            )
            map_link = f"https://maps.google.com/maps?q={lat_long_str}"
            map_link = "".join(map_link.split())
            # Shorten the URL so twitch doesn't break at the comma in the URL
            shortened_url_code = shorten_url(map_link)
            short_url = "https://gotiny.cc/" + shortened_url_code
            comment = f"""Bummer for you - the ISS is currently over the WATER (it's actually right \
            here: {short_url}), which doesn't have a proper language, so I can't provide you with a cool translation. \
            Sorry! """
    sock = TwitchApi.connect()
    TwitchApi.chat(sock, comment)
    time.sleep(160)


def get_random_word_from_list():
    with open("wordlist.txt", "r") as file:
        words = [line.strip() for line in file]
    random_word = random.choice(words)
    return random_word


if __name__ == "__main__":
    while True:
        track_iss(
            iss=Iss(),
            geography=GeographyInformation(),
            dictionary=Dictionary(),
        )
