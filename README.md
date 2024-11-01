# pipeline

Data Pipelines to collect and store data from ohmtimize installations. This project connects to a mqtt instance and subscribes to a topic, publishing it's content in a db. Please create a .env file to store the settings of your mqtt instance and mysql instance

## Run

> Prerequisite: install docker.

### Install depencies

Run:

```zsh
pip install -r requirements.txt
```

Note: when you add new dependencies, don't forget to add them to the `requirements.txt` file by doing

```zsh
pip freeze > requirements.txt
```

### Turn on docker services

Then, run the command:

```zsh
docker-compose up -d
```

To stop the docker services, run

```zsh
docker compose stop
```

### Run migrations

If database tables are not yet created, or whenever the database structure needs to change, you can run the migration script with the following command

```zsh
python migrations/migrate.py
```

### Run the programm

You can simply run the program by doing:

```zsh
python src/main.py
```

### Test the programm

Run the tests with

```zsh
pytest
```

### Test MQTT Service

Open two terminals.  
In the first one, you can subscribe to the service by running:

```zsh
docker container exec mosquitto mosquitto_sub -i mosq_sub1 -t "#"
```

In the second one, you can publish a message by running:

```zsh
docker container exec mosquitto mosquitto_pub -t base_topic/domain/entity/state -m "this is a value"
```

## Usefull links

- tutorial to create mqtt service into the docker-compose file: <https://medium.com/@agalliani/what-is-mqtt-what-is-a-broker-and-how-to-deploy-it-with-docker-a2120b918741>

## Pipeline documentation

1. The HomeAssistant publishes on an MQTT server with the MQTT Statestream plugin.  Which publishes every state changes according to the documentation: <https://www.home-assistant.io/integrations/mqtt_statestream/>.
Note that the topics are structured this way: `base_topic/domain/entity/state`, for example: `homeassistant/light/master_bedroom_dimmer/state`
2. Our pipeline subscribes to the MQTT broker and saves every messages into a MySQL database in the table `messages`.
3. A DB Trigger runs after insert to copy the information into tables structured in such a way that it is easy to query values from defined entities, etc.
For example, you can use the following query to retrieve all values:

```SQL
select
    facts.id,
    facts.fact,
    states.label as state,
    states.id as state_id,
    entities.label as entity,
    entities.id as entity_id,
    base_topics.label as main_topic,
    base_topic_id as main_topic_id
from facts
join states on facts.state_id = states.id
join entities on states.entity_id = entities.id
join base_topics on entities.base_topic_id = base_topics.id
```
