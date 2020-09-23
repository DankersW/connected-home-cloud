# Notes
Mostly good to remember cli commands

## Cloud pub/sub
Pull messages from a specific subscription
```shell
gcloud pubsub subscriptions pull --auto-ack projects/dankers/subscriptions/test-led-subscription --limit=100
```

## Cloud IoT Core
Sending  command messages down
```shell
COMMAND_DATA="{"light_state": 1}"
REGION="europe-west1"
REGISTRY_ID="home_automation_light_switches"
DEVICE_ID="light_switch_001"
gcloud iot devices commands send --command-data=${COMMAND_DATA} --region=${REGION} --registry=${REGISTRY_ID} --device=${DEVICE_ID}
```
