import sys
import time


ALLOWED_FIELDS = {
    "sensor_id",
    "conn_status",
    "last_seen",
    "health_score",
    "error_msg",
}
REQUIRED_FIELDS = {"sensor_id", "conn_status"}


def _split_fields(value):
    fields = []
    start = 0
    quoted = False
    escaped = False

    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quoted:
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
            continue
        if char == "," and not quoted:
            fields.append(value[start:index])
            start = index + 1

    fields.append(value[start:])
    return fields


def process_line(line):
    line = line.strip()
    if not line:
        return None

    parts = line.rsplit(" ", 1)
    if len(parts) != 2 or not parts[1].isdigit():
        return None

    metric_and_fields, timestamp = parts
    head = metric_and_fields.split(" ", 1)
    if len(head) != 2:
        return None

    selected = []
    present = set()
    for item in _split_fields(head[1]):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        if key not in ALLOWED_FIELDS:
            continue
        selected.append(f"{key}={value}")
        present.add(key)

    if not REQUIRED_FIELDS.issubset(present):
        return None

    return f"sensor_status {','.join(selected)} {timestamp}\n"


def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                time.sleep(1)
                continue

            result = process_line(line)
            if result:
                sys.stdout.write(result)
                sys.stdout.flush()
            else:
                sys.stderr.write("[sensor_status] Dropped malformed metric\n")
                sys.stderr.flush()
        except KeyboardInterrupt:
            break
        except Exception as exc:
            sys.stderr.write(f"[sensor_status] Processor error: {exc}\n")
            sys.stderr.flush()
            time.sleep(1)


if __name__ == "__main__":
    main()
