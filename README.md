# Kind Local Thai
"Kind Local Thai" is an actions on Google applets for Google Assistant. 

# Problem
Language differences is one of the pain for foreigner traveling in Thailand. Google Assistant can only help pronounce the words that are in Dictionary, not proper name like place names. For example, Thai people would not understand "The Grand Palace", because it is called differently. By just saying "How to say The temple of Dawn in Thai", our app can assist foreigners to know how the place is called by Thais with Thai pronunciation. User can also ask for brief information about the place and its detail in Google Maps. In addition, the app provides over useful 30 phone numbers for tourists.

# Description
This repo consists all 3 modules necessary to create the actions. 
1. Web scraper is a short Python 2.7 script used for populating Eng-Thai database of place names in JSON format. It also provides short description about the places.

2. Thai TTS backend is a Flask API server used for converting input text in Thai language to Thai speech. The API uses Google Translate's TTS to generate the audio. We need to create this backend because Thai language is not yet supported by Google's Cloud Text-to-Speech API. The audio from this backend will be played on user device.

3. Fulfillment webhook is a Firebase Cloud function used to respond to user's intent sent from Dialogflow. It takes the mapping database generated from the web scraper to provide Thai pronunciation from Thai TTS backend, as well as brief information about places.

### Team: TinyPordeeOnion 
