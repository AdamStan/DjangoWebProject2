import sys
import time
from statistics import mean

from entities.models import FieldOfStudy
from .base_test import BaseTest
from ..algorithms.graph_algorithm import GraphAlgorithmRunner
from ..report_generator import BasicAlgorithmReport


class GraphAlgorithmTests(BaseTest):
    HOW_MANY_TIMES_RUN = 100

    def setUp(self):
        super(GraphAlgorithmTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.min_hour = 8
        self.max_hour = 19

    def test_improvement_algorithm(self):
        results = self.run_algorithm()
        self.assertNotEqual("Exception", results[0])

    def test_genetic_algorithm_performance(self):
        results = list()
        before = time.time_ns()
        for _ in range(GraphAlgorithmTests.HOW_MANY_TIMES_RUN):
            results.append(self.run_algorithm())
        after = time.time_ns()

        error_rate = 0
        good_results = list()
        for res in results:
            if res[0] == "Exception":
                error_rate += 1
            else:
                good_results.append(res[1])

        min_value = min(good_results)
        max_value = max(good_results)
        mean_value = mean(good_results)

        time_in_seconds = (after - before) / 1_000_000_000
        times_was_run = GraphAlgorithmTests.HOW_MANY_TIMES_RUN

        report = BasicAlgorithmReport(time_in_seconds, mean_value, "graph algo tests",
                                      other_info_dict={"times_was_run": times_was_run,
                                                       "good_results": len(good_results),
                                                       "errors": error_rate, "min_value": min_value,
                                                       "max_value": max_value},
                                      lists_with_results=[good_results],
                                      file_name="report_graph_algo_")
        report.create_report()

    def run_algorithm(self):
        try:
            first_plan = GraphAlgorithmRunner()
            result = first_plan.create_plan_async(min_hour=self.min_hour, max_hour=self.max_hour)
            return result
        except Exception as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            return ["Exception", sys.maxsize]
