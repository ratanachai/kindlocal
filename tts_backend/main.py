from flask import Flask

from api.services import translate_tts_api

app = Flask(__name__)

app.register_blueprint(translate_tts_api)
