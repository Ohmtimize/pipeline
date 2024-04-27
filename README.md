# pipeline

Data Pipelines to collect and store data from ohmtimize installations

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

```
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
docker container exec mosquitto mosquitto_pub -t bedroom/temperature -m "bedroom_temperature celsius=20"
```

## Usefull links

- tutorial to create mqtt service into the docker-compose file: <https://medium.com/@agalliani/what-is-mqtt-what-is-a-broker-and-how-to-deploy-it-with-docker-a2120b918741>
