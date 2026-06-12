import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "telegraf_py"))

from mapping_processor import process_line


class MappingProcessorTests(unittest.TestCase):
    def test_normalizes_status_metric_and_preserves_timestamp(self):
        line = (
            'mqtt_consumer,topic=C-S/site/iot_temp/status '
            'sensor_id=211i,conn_status="on",last_seen="2026-06-12 06:07:10.034+07",'
            'health_score=98.3,error_msg="crc error" 1781222830037000000'
        )

        result = process_line(line)

        self.assertEqual(
            result,
            'sensor_status sensor_id=211i,conn_status="on",'
            'last_seen="2026-06-12 06:07:10.034+07",health_score=98.3,'
            'error_msg="crc error" 1781222830037000000\n',
        )

    def test_omits_unknown_fields(self):
        line = (
            'mqtt_consumer sensor_id=211i,conn_status="off",health_score=50.0,'
            'unexpected="drop-me" 1781222830037000000'
        )

        result = process_line(line)

        self.assertNotIn("unexpected", result)
        self.assertEqual(
            result,
            'sensor_status sensor_id=211i,conn_status="off",health_score=50.0 '
            '1781222830037000000\n',
        )

    def test_rejects_metric_without_required_fields(self):
        self.assertIsNone(
            process_line(
                'mqtt_consumer health_score=0.0 1781222830037000000'
            )
        )

    def test_handles_escaped_commas_and_quotes_in_error_message(self):
        line = (
            'mqtt_consumer sensor_id=211i,conn_status="off",'
            'error_msg="CRC failed, response=\\\"bad\\\"" 1781222830037000000'
        )

        result = process_line(line)

        self.assertIn('error_msg="CRC failed, response=\\\"bad\\\""', result)


if __name__ == "__main__":
    unittest.main()
