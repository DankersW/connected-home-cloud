from google.cloud import iot_v1


def firestore_on_update_to_devices_pubsub(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    name = event['value']['name']
    state = event['value']['fields']['state']['integerValue']
    device_id = get_device_id_from_name(name)
    payload = '{"light_state": ' + state + '}'
    if device_id is not None:
        send_command_to_device(device_id, payload)


def get_device_id_from_name(name):
    i_dev_id = 6
    dir_tree = name.split('/')
    valid_name = len(dir_tree) == 7 and 'light_switch' in dir_tree[i_dev_id]
    if valid_name:
        return dir_tree[i_dev_id]
    return None


def send_command_to_device(device_id, payload):
    project = 'dankers'
    location = 'europe-west1'
    registry = 'home_automation_light_switches'
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project, location, registry, device_id)
    binary_payload = payload.encode()
    return client.send_command_to_device(device_path, binary_payload)



if __name__ == '__main__':
    event = {'oldValue': {'createTime': '2020-05-25T11:18:18.595997Z', 'fields': {'online': {'booleanValue': False}, 'state': {'integerValue': '0'}}, 'name': 'projects/dankers/databases/(default)/documents/devices/light_switch_001', 'updateTime': '2020-06-06T03:09:15.009407Z'}, 'updateMask': {'fieldPaths': ['state']}, 'value': {'createTime': '2020-05-25T11:18:18.595997Z', 'fields': {'online': {'booleanValue': False}, 'state': {'integerValue': '1'}}, 'name': 'projects/dankers/databases/(default)/documents/devices/light_switch_001', 'updateTime': '2020-06-06T03:09:15.009407Z'}}
    context = None
    firestore_on_update_to_devices_pubsub(event, context)