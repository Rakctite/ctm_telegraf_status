import importlib
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "telegraf_py"))
sys.modules.setdefault("psycopg2", types.SimpleNamespace(connect=None))


class MappingProcessorTests(unittest.TestCase):
    def setUp(self):
        self.processor = importlib.import_module("mapping_processor")
        with self.processor.cache_lock:
            self.processor.mapping_cache = {
                "LO054:MC02:ST01:Temp_ST01_PL01": (211, 20),
                "LO054:MC02:ST01:Temp_ST01_PL02": (212, 20),
                "LO054:MC02:ST02:Temp_ST01_PL01": (311, 21),
            }

    def test_maps_status_topic_station_and_sensor_code_to_sensor_id(self):
        line = (
            'mqtt_consumer,equip_name=MC02,line_code=LO054,station=ST01,source=iot_temp,status_suffix=status '
            'sensor_code="Temp_ST01_PL01",conn_status="on",last_seen="2026-06-18 05:25:09.580+07",'
            'health_score=100,error_msg="",update_time="2026-06-18 05:25:10.210+07" '
            "1781735110210000000"
        )

        result = self.processor.process_line(line)

        self.assertEqual(
            result,
            'sensor_status sensor_id=211i,conn_status="on",'
            'last_seen="2026-06-18 05:25:09.580+07",health_score=100 '
            "1781735110210000000\n",
        )

    def test_uses_station_to_disambiguate_same_sensor_code(self):
        line = (
            'mqtt_consumer,equip_name=MC02,line_code=LO054,station=ST02,source=iot_temp,status_suffix=status '
            'sensor_code="Temp_ST01_PL01",conn_status="on",update_time="2026-06-18 05:25:10.210+07" '
            "1781735110210000000"
        )

        result = self.processor.process_line(line)

        self.assertEqual(
            result,
            'sensor_status sensor_id=311i,conn_status="on" 1781735110210000000\n',
        )

    def test_rejects_non_status_topic(self):
        line = (
            'mqtt_consumer,equip_name=MC02,line_code=LO054,station=ST01,source=iot_temp '
            'conn_status="on" 1781735110210000000'
        )

        self.assertIsNone(self.processor.process_line(line))

    def test_rejects_unmapped_sensor_code(self):
        self.assertIsNone(
            self.processor.process_line(
                'mqtt_consumer,equip_name=MC02,line_code=LO054,station=ST01,source=iot_temp,status_suffix=status '
                'sensor_code="UNKNOWN",conn_status="on",update_time="2026-06-18 05:25:10.210+07" 1781735110210000000'
            )
        )

    def test_keeps_error_message_with_escaped_commas_and_quotes(self):
        line = (
            'mqtt_consumer,equip_name=MC02,line_code=LO054,station=ST01,source=iot_temp,status_suffix=status '
            'conn_status="off",last_seen="2026-06-18 05:25:09.580+07",'
            'sensor_code="Temp_ST01_PL02",health_score=50,error_msg="CRC failed, response=\\\"bad\\\"",'
            'update_time="2026-06-18 05:25:10.210+07" 1781735110210000000'
        )

        result = self.processor.process_line(line)

        self.assertEqual(
            result,
            'sensor_status sensor_id=212i,conn_status="off",'
            'last_seen="2026-06-18 05:25:09.580+07",health_score=50,'
            'error_msg="CRC failed, response=\\"bad\\"" 1781735110210000000\n',
        )


if __name__ == "__main__":
    unittest.main()
