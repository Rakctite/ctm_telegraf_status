# Sensor Status Telegraf Design

## Scope

Create a status-only Telegraf pipeline in `ctm_telegraf_status`, built independently from the official `telegraf:1.38.4` image. The image adds Python 3 for the execd processor and embeds `telegraf.conf` and `telegraf_py/mapping_processor.py`.

## Data Flow

1. Subscribe only to `C-S/+/+/+/+/+/+/+/status`.
2. Parse the MQTT JSON with `json_v2` and expand `sensors` into one metric per array item.
3. Use each item's `update_time` as the metric timestamp.
4. Normalize each metric in the execd processor to the `sensor_status` measurement and retain only `sensor_id`, `conn_status`, `last_seen`, `health_score`, and `error_msg`.
5. Insert every metric into `core.sensor_status` with the SQL output plugin and its PostgreSQL `pgx` driver; do not upsert.

The database generates `id`. The SQL output maps the metric timestamp to `update_time`. The SQL output is used because the dedicated PostgreSQL output's binary COPY path cannot encode the string `last_seen` field into an existing `timestamptz` column.

## Null Handling

`last_seen` and `error_msg` may be JSON null. Missing fields are omitted from line protocol, allowing PostgreSQL to store SQL NULL. Required fields are `sensor_id` and `conn_status`; malformed metrics are dropped with a stderr message.

## Database Contract

The pipeline writes to the existing table columns:

```text
sensor_id, conn_status, last_seen, health_score, error_msg, update_time
```

No retention or deletion policy is included.

## Verification

- Unit-test processor normalization, type validation, null omission, and escaping.
- Validate `telegraf.conf` with Telegraf 1.38.4.
- Feed a representative payload through Telegraf and confirm 25 output metrics can be produced.
