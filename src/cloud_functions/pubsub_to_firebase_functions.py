# test the function with the following JSON string
# {"@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage", "attributes": {"deviceId": "light_switch_001", "deviceNumId": "2833441033873397", "deviceRegistryId": "home_automation_light_switches", "deviceRegistryLocation": "europe-west1", "projectId": "dankers"}, "data": "e2xpZ2h0c19zdGF0ZTogMX0="}

import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json


def lightswitches_pubsub_to_firebase(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    message_content = analyse_pubsub_message(event)
    if message_content is not None:
        write_to_firestore(message_content)


def analyse_pubsub_message(event):
    # Fetch content from pubsub event
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_device = event['attributes']['deviceId']
    try:
        data = json.loads(pubsub_message)
        if 'light_state' in data:
            message_content = {'device_id': pubsub_device,
                               'light_state': data['light_state']}
            return message_content
        return None
    except ValueError as e:
        print("JSON conversion error in message {} -- Error: {}".format(pubsub_message, e))
        return None


def write_to_firestore(message):
    # Use the application default credentials to init firebase
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        default_app = firebase_admin.initialize_app(cred, {'projectId': 'dankers', })
    db = firestore.client()

    # Writing data to Firebase
    doc_ref = db.collection(u'devices').document(message.get('device_id'))
    doc_ref.set({
        u'online': True,
        u'state': message.get('light_state')
    })


if __name__ == '__main__':
    # Something seems to be wrong with initializing the app!!! error that occurures
    # event: {'@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage', 'attributes': {'deviceId': 'light_switch_001', 'deviceNumId': '2833441033873397', 'deviceRegistryId': 'home_automation_light_switches', 'deviceRegistryLocation': 'europe-west1', 'gatewayId': 'home_automation_light_switches_gateway', 'projectId': 'dankers'}, 'data': 'eyJsaWdodF9zdGF0ZSI6IDF9'}
    # context: {event_id: 1397797228920637, timestamp: 2020-08-05T15:57:31.889Z, event_type: google.pubsub.topic.publish, resource: {'service': 'pubsub.googleapis.com', 'name': 'projects/dankers/topics/home_automation_light_switches_state_topic', 'type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage'}}
    #
    event_arg_1 = {'@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage','attributes': {'deviceId': 'light_switch_001', 'deviceNumId': '2833441033873397', 'deviceRegistryId': 'home_automation_light_switches', 'deviceRegistryLocation': 'europe-west1','gatewayId': 'home_automation_light_switches_gateway', 'projectId': 'dankers'}, 'data': 'bGlnaHRfc3RhdGU6IDE='}
    event_arg_0 = {'data': 'bGlnaHRfc3RhdGU6IDE=', '@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage', 'attributes': {'deviceRegistryLocation': 'europe-west1', 'deviceNumId': '2833441033873397', 'deviceRegistryId': 'home_automation_light_switches', 'deviceId': 'light_switch_001', 'projectId': 'dankers'}}
    lightswitches_pubsub_to_firebase(event_arg_1, None)
    lightswitches_pubsub_to_firebase(event_arg_0, None)
