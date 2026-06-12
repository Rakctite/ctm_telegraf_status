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

