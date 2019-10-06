'use strict';
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

// App constants, and Load places data
const AUDIO_BASE_URL = "https://peyrone.pythonanywhere.com/text-to-speech"
let places; const fs = require('fs');
fs.readFile('./data/places_en2th.json', 'utf8', function (err, data) {
  if (err) throw err;
  places = JSON.parse(data);
});

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function howtosay(agent) {
    const placeEn = agent.parameters.placeinthailand;
    const placeTh = places[placeEn] !== null ? places[placeEn].thai : `Sorry no information`
    const soundUrl = `${AUDIO_BASE_URL}?msg=${placeTh}`;
    agent.add(`<speak>
                  <audio src="${soundUrl}"> 
                    <desc>${placeEn} is ${placeTh} in Thai.</desc>
                  </audio>
                  Do you want to learn more about it? Or do you want me to say it again?
                </speak>`);
  }
  function learnAbout(agent) {
    const placeEn = agent.parameters.placeinthailand;
    const text = places[placeEn] !== null ? places[placeEn].about : `Sorry no information`
    agent.add(text);
    agent.add(`Are you Interested? Do you want to see it on Google Maps?`)
  }

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('How to say', howtosay);
  intentMap.set('How to say - repeat', howtosay);
  intentMap.set('How to say - more', learnAbout);
  intentMap.set('Learn about', learnAbout);
  agent.handleRequest(intentMap);
});
