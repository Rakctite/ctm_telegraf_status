CREATE SCHEMA core;

CREATE TABLE core.sensor_mst (
    id int4 PRIMARY KEY
);

INSERT INTO core.sensor_mst (id) VALUES (211), (212);

CREATE TABLE core.sensor_status (
    id int8 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sensor_id int4 NOT NULL,
    conn_status varchar(50) DEFAULT 'off' NOT NULL,
    last_seen timestamptz NULL,
    health_score float8 NULL,
    error_msg text NULL,
    update_time timestamptz DEFAULT (now() AT TIME ZONE 'UTC') NOT NULL,
    CONSTRAINT sensor_status_sensor_id_fkey
        FOREIGN KEY (sensor_id) REFERENCES core.sensor_mst(id) ON DELETE CASCADE
);

CREATE INDEX idx_sensor_status_sensor_update
    ON core.sensor_status (sensor_id, update_time DESC);

