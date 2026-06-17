import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TelegrafConfigTests(unittest.TestCase):
    def test_subscribes_only_to_nine_level_status_topics(self):
        config = (ROOT / "telegraf.conf").read_text(encoding="utf-8")

        topics_match = re.search(r'^\s*topics\s*=\s*\["([^"]+)"\]', config, re.MULTILINE)

        self.assertIsNotNone(topics_match)
        self.assertEqual(topics_match.group(1), "C-S/+/+/+/+/+/+/+/status")

    def test_uses_standard_topic_mapping_tags(self):
        config = (ROOT / "telegraf.conf").read_text(encoding="utf-8")

        self.assertIn('data_format = "json_v2"', config)
        self.assertIn('path = "sensors"', config)
        self.assertIn("line_code/equip_name/station/source/status_suffix", config)


if __name__ == "__main__":
    unittest.main()
