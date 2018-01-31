import requests
import json


class WordsApi(object):
    def __init__(self):
        self.base_url = "https://owlbot.info/api/v2/"


    def get_definition(self, chosen_word):
        definition = requests.get("{base_url}dictionary/{chosen_word}".format(base_url=self.base_url, chosen_word=chosen_word)).json()
        return definition

    def get_translation(self, word_to_translate, language):
        yandex_api_key = 'your.yandex.api.key'
        yandex_translate_url = 'https://translate.yandex.net/api/v1.5/'
        translated_word_response = requests.get("{base_url}tr.json/translate?key={api_key}&text={chosen_word}&lang=en-{lang}".format(base_url=yandex_translate_url, api_key=yandex_api_key, chosen_word=word_to_translate, lang=language)).json()
        translated_word = translated_word_response['text'][0]
        return translated_word
