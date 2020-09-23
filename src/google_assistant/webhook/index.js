'use strict';

const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');

const admin = require('firebase-admin');
const serviceAccount = require("./dankers-firebase-adminsdk-r85r7-df645bc8df.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://dankers.firebaseio.com"
});
const db = admin.firestore();

const writeDeviceData = async function(device, state){
  const docRef = db.collection('devices').doc(device);
  await docRef.set({
    online: true,
    state: state
  });
}

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });

  function setLights(agent) {
    const state = parseInt(request.body.queryResult.parameters.state, 10);
    writeDeviceData('light_switch_001', state);
    agent.add(`Lights are controlled correctly`);
  }

  let intentMap = new Map();
  intentMap.set('home automation', setLights);

  agent.handleRequest(intentMap);
});
