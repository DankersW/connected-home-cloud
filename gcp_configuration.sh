PROJECT_ID="dankers"
REGION="europe-west1"

# Creating a device registry
REGISTRY_ID="home_automation_light_switches"
EVENT_PUBSUB_TOPIC="home_automation_light_switches_event_topic"
STATE_PUBSUB_TOPIC="home_automation_light_switches_state_topic"
gcloud iot registries create ${REGISTRY_ID} --project=${PROJECT_ID} --region=${REGION} --enable-mqtt-config --no-enable-http-config --event-notification-config=topic=${EVENT_PUBSUB_TOPIC} --state-pubsub-topic=${STATE_PUBSUB_TOPIC}

# Creating public/private key pairs
mkdir -p certificates
openssl genpkey -algorithm RSA -out certificates/rsa_light_switch_private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in certificates/rsa_light_switch_private.pem -pubout -out certificates/rsa_light_switch_public.pem
wget https://pki.goog/roots.pem

# Create a device
DEVICE_ID="light_switch_001"
gcloud iot devices create ${DEVICE_ID} --project=${PROJECT_ID} --region=${REGION} --registry=${REGISTRY_ID} --log-level=info --public-key path=/home/wouter_dankers/certificates/rsa_light_switch_public.pem,type=rsa-pem

# Create iot-gateway
PROJECT_ID="dankers"
REGION="europe-west1"
REGISTRY_ID="home_automation_light_switches"
GATEWAY_ID="home_automation_light_switches_gateway"
gcloud iot devices create ${GATEWAY_ID} --device-type=gateway --project=${PROJECT_ID} --region=${REGION} --registry=${REGISTRY_ID} --public-key path=/home/wouter_dankers/certificates/rsa_light_switch_public.pem,type=rsa-pem --auth-method=ASSOCIATION_ONLY

# Bind device to iot-gateway
GATEWAY_ID="home_automation_light_switches_gateway"
DEVICE_ID="light_switch_001"
PROJECT_ID="dankers"
REGION="europe-west1"
REGISTRY_ID="home_automation_light_switches"
gcloud iot devices gateways bind --gateway=${GATEWAY_ID} --device=${DEVICE_ID} --project=${PROJECT_ID} --device-region=${REGION} --device-registry=${REGISTRY_ID} --gateway-region=${REGION} --gateway-registry=${REGISTRY_ID}
# Unbind a device
gcloud iot devices gateways unbind --gateway=${GATEWAY_ID} --device=${DEVICE_ID} --project=${PROJECT_ID} --device-region=${REGION} --device-registry=${REGISTRY_ID} --gateway-region=${REGION} --gateway-registry=${REGISTRY_ID}

# Create the pubsub topics
gcloud pubsub topics create ${EVENT_PUBSUB_TOPIC} --project=${PROJECT_ID}
gcloud pubsub topics create ${STATE_PUBSUB_TOPIC} --project=${PROJECT_ID}

# Create test subsription for testing
SUBSCRIPTION_ID="test_home_automation_light_switches_event_subsription"
gcloud pubsub subscriptions create ${SUBSCRIPTION_ID} --topic=${EVENT_PUBSUB_TOPIC} --project=${PROJECT_ID}
gcloud pubsub subscriptions pull --auto-ack projects/${PROJECT_ID}/subscriptions/${SUBSCRIPTION_ID} --limit=100

# Cloud function creation
# Create cloud function - listen to pubsub messages
FUNCTION_NAME="home_automation_light_switches_write_pubsub_message_to_firebase"
SOURCE="/home/wouter_dankers/cloud_function_sources/"
ENTRY_POINT="lightswitches_pubsub_to_firebase"
STATE_PUBSUB_TOPIC="home_automation_light_switches_state_topic"
REGION="europe-west1"
gcloud functions deploy ${FUNCTION_NAME} --region=${REGION} --runtime python37 --trigger-topic=${STATE_PUBSUB_TOPIC} --allow-unauthenticated --entry-point=${ENTRY_POINT} --source=${SOURCE} --project=${PROJECT_ID}
gcloud functions logs read ${FUNCTION_NAME} --limit=50
# Create cloud function - on firebase update
FUNCTION_NAME="home_automation_light_switches_on_firebase_update_to_dev_pubsub"
SOURCE="/home/wouter_dankers/cloud_function_sources/"
ENTRY_POINT="firestore_on_update_to_devices_pubsub"
STATE_PUBSUB_TOPIC="home_automation_light_switches_state_topic"
REGION="europe-west1"
RESOURCE="projects/dankers/databases/(default)/documents/devices/{device_id}"
EVENT_TYPE="providers/cloud.firestore/eventTypes/document.update"
gcloud functions deploy ${FUNCTION_NAME} --region=${REGION} --runtime python37 --trigger-resource=${RESOURCE} --trigger-event=${EVENT_TYPE} --allow-unauthenticated --entry-point=${ENTRY_POINT} --source=${SOURCE} --project=${PROJECT_ID}
