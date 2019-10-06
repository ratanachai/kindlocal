import requests
from tempfile import TemporaryFile

from api.constants import app_constant as const

class TranslateTTS:

    def __init__(self):
        pass

    def speak(self, msg, lang_code='th-TH'):
        r = requests.get(const.TTS_API, params={
            'q': msg,
            'tl': lang_code,
            'ie': 'UTF-8',
            'client': 'tw-ob',
        })
        return r

    def save_mp3(self, msg, lang_code='th-TH'):
        r = self.speak(msg, lang_code)
        file = TemporaryFile()
        for chunk in r.iter_content(100000):
            file.write(chunk)
        file.close()

