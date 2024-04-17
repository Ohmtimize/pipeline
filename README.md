# pipeline

Data Pipelines to collect and store data from ohmtimize installations

## Run

> Prerequisite: install docker.

Then, run the command:

```zsh
docker-compose up -d
```

To stop the docker services, run

```zsh
docker compose stop
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
