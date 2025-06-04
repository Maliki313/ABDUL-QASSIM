import os
import tempfile
import json
from pathlib import Path
import unittest

from scripts.parse_history import sanitize_filename, write_conversation


class TestParseHistory(unittest.TestCase):
    def test_sanitize_filename(self):
        original = "conv: test/1"
        expected = "conv__test_1"
        self.assertEqual(sanitize_filename(original), expected)

    def test_write_conversation_creates_file(self):
        conv = {
            "title": "demo:conv/1",
            "mapping": {
                "1": {
                    "create_time": 0,
                    "message": {
                        "content": {"parts": ["hi"]}
                    }
                }
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            write_conversation(conv, Path(tmpdir))
            expected_file = Path(tmpdir) / "demo_conv_1.txt"
            self.assertTrue(expected_file.exists())
            self.assertEqual(expected_file.read_text(encoding="utf-8").strip(), "hi")


if __name__ == "__main__":
    unittest.main()
