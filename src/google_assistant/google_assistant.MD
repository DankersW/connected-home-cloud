# Google Assistant

## Dialogflow
[Dialogflow](https://dialogflow.cloud.google.com/?region=EU2#) is used to create the voice command and custom responses.
It is also an interface to specify the training phases and the parameters and actions belonging to that trigger

### Intents
Will listen set the state entity to the value specified by the user. 1 for on, 0 for off.

#### Training phases

| Training phrase       | Parameter name | Entiy  | Resolved value |
|-----------------------|----------------|--------|----------------|
| Power off the lights  | state          | @state | Power off      |
| Power on the lights   | state          | @state | Power on       |
| Switch on the lights  | state          | @state | Switch on      |
| Switch off the lights | state          | @state | Switch off     |
| turn off the lights   | state          | @state | Turn off       |
| turn on the lights    | state          | @state | Turn on        |

### Entities
Entities are used to map values to synonyms that are detected in the users phrases. 

#### State

|       | Value | Synonyms                            |
|-------|-------|-------------------------------------|
| 0     | "0"   | "Turn off","Power off","Switch off" |
| 1     | "1"   | "Turn on","Power on","Switch on"    |

### Fulfilment
Fulfilment is handled by the webhook which runs as a cloud function. It fetches the state from the request body and 
writes this one to the Firestore DB.
