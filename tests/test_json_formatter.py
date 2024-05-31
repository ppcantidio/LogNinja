import datetime as dt
import json
import logging
import unittest

from logninja.ninja_json_formatter import NinjaJsonFormatter


class NinjaJsonFormatterTests(unittest.TestCase):
    def test_format(self):
        formatter = NinjaJsonFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="/path/to/file.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
            func="test_function",
            sinfo=None,
        )

        formatted_message = formatter.format(record)
        self.assertIsInstance(formatted_message, str)
        expected_result = {
            "level": "INFO",
            "message": "Test message",
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
            "logger": "test_logger",
            "module": "file",
            "function": "test_function",
            "line": 10,
            "thread_name": "MainThread",
        }
        self.assertDictEqual(
            expected_result,
            json.loads(formatted_message),
        )


if __name__ == "__main__":
    unittest.main()
