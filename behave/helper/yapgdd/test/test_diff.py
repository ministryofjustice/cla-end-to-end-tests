import unittest
from unittest.mock import patch
from utils import Yapgdd, TestDatabases


class DiffTest(TestDatabases, unittest.TestCase):

    def setUp(self):
        exclude_columns = ["id", "created", "modified"]
        self.instance = Yapgdd(self.source_db, self.target_db, exclude_columns=exclude_columns, output_dir="./diffs")

    def test_diff_summary(self):
        summary = {}

        def log_summary(data):
            nonlocal summary
            summary = data

        with patch.object(self.instance, "log_summary", log_summary):
            self.instance.diff_data()

        expected_summary = [{
            "table": "logs",
            "table present": True,
            "columns equal": True,
            "source rows count": 2,
            "target rows count": 3,
            "counts equal": False,
            "rows equal": False,

        }]
        self.assertEqual(summary, expected_summary)

    def test_diff_table(self):
        expected_diffs = {
            "logs": [{
                "code": {
                    "icon": "+",
                    "row number": 2,
                    "column": "code",
                    "source": None,
                    "target": "COMPLAINT_CREATED",

                },
                "level": {
                    "icon": "+",
                    "row number": 2,
                    "column": "level",
                    "source": None,
                    "target": 29,

                }
            }]
        }

        actual_diffs = {}

        def log_table_diff(table, diff):
            nonlocal actual_diffs
            actual_diffs[table] = diff

        with patch.object(self.instance, "log_table_diff", log_table_diff):
            self.instance.diff_data()
        self.assertEqual(actual_diffs, expected_diffs)