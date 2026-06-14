# Docker Compose Deployment

`docker-compose.yml` starts the PostgreSQL database, MQTT broker, and sensor-status Telegraf service together.

The `ctm_telegraf_status` image already contains:

- `/etc/telegraf/telegraf.conf`
- `/telegraf/telegraf_py/mapping_processor.py`

Do not mount local copies over these paths unless you intentionally want to override the released image.

## Images

```text
203.228.107.184:5000/btx/edge-hmi-db:latest
203.228.107.184:5000/mosquitto:v1.0.0
203.228.107.184:5000/btx/ctm_telegraf_status:1.0.0
```

## Start

Run from the directory containing `docker-compose.yml`:

```sh
docker compose pull
docker compose up -d
```

Check service state and Telegraf logs:

```sh
docker compose ps
docker compose logs -f ctm_telegraf_status
```

## Stop

```sh
docker compose down
```

Database and MQTT data remain in named volumes. To remove those volumes as well:

```sh
docker compose down -v
```

`down -v` permanently deletes the database and MQTT volume data.

## Configuration

The compose file supports these optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `REGISTRY` | `203.228.107.184:5000` | Container registry address |
| `DB_IMAGE_TAG` | `latest` | Edge HMI database image tag |
| `MQTT_IMAGE_TAG` | `v1.0.0` | Mosquitto image tag |
| `CTM_TELEGRAF_STATUS_IMAGE_TAG` | `1.0.0` | Status Telegraf image tag |
| `TZ` | `Asia/Jakarta` | Container timezone |
| `POSTGRES_PORT` | `5432` | PostgreSQL host port |
| `MQTT_PORT` | `1883` | MQTT host port |
| `MQTT_DASHBOARD_PORT` | `9883` | MQTT dashboard host port |

PowerShell example:

```powershell
$env:CTM_TELEGRAF_STATUS_IMAGE_TAG = "1.0.0"
docker compose up -d
```

## Internal Connections

The containers communicate over the Compose default network:

- Telegraf to MQTT: `mosquitto:1883`
- Telegraf to PostgreSQL: `hmi-db-postgres:5432`

The database credentials in this release must remain:

```text
database: edge_hmi
user: admin
password: 1q2w3e4r
```

They match the connection string embedded in the released Telegraf configuration.

## Existing Containers

The compose file uses fixed container names `hmi-db-postgres`, `mqtt-mosquitto`, and `ctm_telegraf_status`. Stop or remove containers with those names before starting this stack. Do not run this compose alongside another stack that creates the same DB or MQTT containers.

