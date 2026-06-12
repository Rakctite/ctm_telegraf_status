# Sensor Status Telegraf Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consume plate sensor status MQTT messages and insert every sensor snapshot into `core.sensor_status`.

**Architecture:** Telegraf 1.38.4 expands the `sensors` JSON array into individual metrics. A Python execd processor validates and normalizes line protocol before the SQL output's PostgreSQL `pgx` driver inserts rows with the metric timestamp stored as `update_time`.

**Tech Stack:** Telegraf 1.38.4, MQTT, JSON v2 parser, Python 3, Influx line protocol, PostgreSQL, Docker

---

### Task 1: Processor Contract

**Files:**
- Create: `tests/test_mapping_processor.py`
- Create: `telegraf_py/mapping_processor.py`

- [x] Write tests that require `process_line()` to rename the measurement, keep the five allowed fields, preserve the timestamp, omit optional null fields, and reject missing required fields.
- [x] Run `python -m unittest discover -s tests -v` and verify failure because the processor module does not exist.
- [x] Implement a side-effect-free parser/formatter plus a stdin/stdout main loop guarded by `if __name__ == "__main__"`.
- [x] Run the tests and verify all cases pass.

### Task 2: Telegraf Pipeline

**Files:**
- Create: `telegraf.conf`

- [x] Configure the same agent batching values as `ctm_telegraf`.
- [x] Configure MQTT topic `C-S/+/+/+/+/+/+/+/status`, QoS 1, and JSON v2 array expansion at `sensors`.
- [x] Configure the execd processor to run `/telegraf/telegraf_py/mapping_processor.py`.
- [x] Configure SQL output with the PostgreSQL `pgx` driver, schema search path `core`, table `sensor_status`, timestamp column `update_time`, and no conflict action.
- [x] Run Telegraf 1.38.4 config validation.

### Task 3: End-to-End Parser Verification

**Files:**
- Create: `tests/fixtures/status.json`
- Create: `tests/telegraf-test.conf`

- [x] Add a representative two-sensor payload containing both populated and null optional fields.
- [x] Run Telegraf with file input, the production processor, and stdout output.
- [x] Verify two normalized `sensor_status` metrics are emitted with expected timestamps and fields.
- [x] Run the full unit test and Python compile checks.
