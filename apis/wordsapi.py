import requests
import json
import os


class Dictionary(object):
    def __init__(self):
        self.yandex_api_key = os.environ.get("YANDEX_API_KEY")
        self.yandex_translate_url = "https://translate.yandex.net/api/v1.5/"
        self.owl_api_key = os.environ.get("OWL_API_KEY")
        self.owl_base_url = "https://owlbot.info/api/v4/"

    def get_definition(self, chosen_word):
        headers = {"Authorization": "Token " + self.owl_api_key}
        definition = requests.get(
            "{base_url}dictionary/{chosen_word}".format(
                base_url=self.owl_base_url, chosen_word=chosen_word
            ),
            headers=headers,
        ).json()
        return definition

    def get_translation(self, word_to_translate, language):
        translated_word_response = requests.get(
            "{base_url}tr.json/translate?key={api_key}&text={chosen_word}&lang=en-{lang}".format(
                base_url=self.yandex_translate_url,
                api_key=self.yandex_api_key,
                chosen_word=word_to_translate,
                lang=language,
            )
        ).json()
        breakpoint()
        translated_word = translated_word_response["text"][0]
        return translated_word
