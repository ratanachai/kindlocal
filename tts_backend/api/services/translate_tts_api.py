from flask import Blueprint, Response, request

from api.utils.translate_tts import TranslateTTS


translate_tts_api = Blueprint('translate_tts_api', __name__)


@translate_tts_api.route('/text-to-speech', methods=['GET'])
def tts():
    msg = request.args.get('msg')
    tts = TranslateTTS()

    return Response(tts.speak(msg), mimetype='audio/mp3')
