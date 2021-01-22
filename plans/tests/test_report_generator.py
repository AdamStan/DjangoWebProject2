import unittest
from plans.report_generator import BasicAlgorithmReport
import os


class TestAllParameters(unittest.TestCase):
    def test_report_generation(self):
        report_gen = BasicAlgorithmReport(time=100, result_value=123, quality_function_name="ddd",
                                          other_info_dict={"key1": "value1", "key2": "value2"})
        self.file_name = report_gen.create_report()

    def tearDown(self):
        if self.file_name:
            os.remove(self.file_name)
