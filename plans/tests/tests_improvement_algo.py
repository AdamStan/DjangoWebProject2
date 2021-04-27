import sys
import time
from statistics import mean

from entities.models import FieldOfStudy
from .base_test import BaseTest
from plans.algorithms import ImprovementAlgorithm
from ..report_generator import BasicAlgorithmReport


class ImprovementAlgorithmTests(BaseTest):
    HOW_MANY_TIMES_RUN = 100

    def setUp(self):
        super(ImprovementAlgorithmTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.min_hour = 8
        self.max_hour = 19
        self.how_many_tries_improve = 1_000

    def test_improvement_algorithm(self):
        results = self.run_algorithm()
        self.assertNotEqual("Exception", results[0])

    def test_improvement_algorithm_performance(self):
        results = list()
        before = time.time_ns()
        for _ in range(ImprovementAlgorithmTests.HOW_MANY_TIMES_RUN):
            results.append(self.run_algorithm())
        after = time.time_ns()

        error_rate = 0
        good_results = list()
        good_results_before_improvement = list()
        tries_labs = list()
        tries_lec = list()
        suc_labs = list()
        suc_lec = list()
        for res in results:
            if res[0] == "Exception":
                error_rate += 1
            else:
                good_results.append(res[1][0])
                tries_labs.append(res[1][1])
                tries_lec.append(res[1][2])
                suc_labs.append(res[1][3])
                suc_lec.append(res[1][4])
                good_results_before_improvement.append(res[2])

        min_value = min(good_results)
        max_value = max(good_results)
        mean_value = mean(good_results)

        time_in_seconds = (after - before) / 1_000_000_000
        times_was_run = ImprovementAlgorithmTests.HOW_MANY_TIMES_RUN

        report = BasicAlgorithmReport(time_in_seconds, mean_value, "improvement_algo_tests",
                                      other_info_dict={"times_was_run": times_was_run,
                                                       "good_results": len(good_results), "errors": error_rate,
                                                       "min_value": min_value, "max_value": max_value,
                                                       "improvement_tries": self.how_many_tries_improve},
                                      lists_with_results=[good_results, good_results_before_improvement, tries_labs,
                                                          tries_lec, suc_labs, suc_lec],
                                      file_name="report_improvement_lab_and_lectures_tests_")
        report.create_report()

    def run_algorithm(self):
        try:
            first_plan = ImprovementAlgorithm(self.how_many_tries_improve)
            result = first_plan.create_plan_async(min_hour=self.min_hour, max_hour=self.max_hour)
            return result
        except Exception as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            return ["Exception", sys.maxsize]
