# ctm_telegraf_status

Consumes `C-S/+/+/+/+/+/+/+/status` MQTT messages and inserts each sensor snapshot into `core.sensor_status`.

## Build

```sh
docker build -t ctm_telegraf_status:1.0.0 .
```

The image is built independently from the official `telegraf:1.38.4` image.

## Runtime dependencies

The container must be able to resolve and connect to:

- MQTT broker: `mosquitto:1883`
- PostgreSQL: `hmi-db-postgres:5432`

## Docker Compose

The included `docker-compose.yml` starts the database, MQTT broker, and status Telegraf service. The Telegraf configuration and mapping processor are loaded from inside the image; no host file mounts are required.

```sh
docker compose pull
docker compose up -d
```

See [docs/docker-compose.md](docs/docker-compose.md) for deployment details, environment variables, volumes, and shutdown commands.
