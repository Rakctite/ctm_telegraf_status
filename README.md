# ctm_telegraf_status

Consumes `C-S/+/+/+/+/+/+/+/status` MQTT messages and inserts each sensor snapshot into `core.sensor_status`.

## Build

```sh
docker build -t ctm_telegraf_status:1.0.1 .
```

The image is built independently from the official `telegraf:1.38.4` image.

## Runtime dependencies

The container must be able to resolve and connect to:

- MQTT broker: `mosquitto:1883`
- PostgreSQL: `hmi-db-postgres:5432`

## Status MQTT Contract

Status messages use the same topic mapping scheme as the measurement Telegraf pipeline. The final `status` segment marks the message as sensor status:

```text
C-S/{plant}/{building}/{process}/{line_code}/{equip_name}/{station}/{sensor_code}/status
```

Payload:

```json
{
  "sensor_code": "Temp_ST01_PL01",
  "conn_status": "on",
  "last_seen": "2026-06-18 05:25:09.580+07",
  "health_score": 100,
  "error_msg": null,
  "update_time": "2026-06-18 05:25:10.210+07"
}
```

`mapping_processor.py` maps `line_code:equip_name:sensor_code` through `core.v_topic_mapping` and inserts into `core.sensor_status`.

## Docker Compose

The included `docker-compose.yml` starts the database, MQTT broker, and status Telegraf service. The Telegraf configuration and mapping processor are loaded from inside the image; no host file mounts are required.

```sh
docker compose pull
docker compose up -d
```

See [docs/docker-compose.md](docs/docker-compose.md) for deployment details, environment variables, volumes, and shutdown commands.
