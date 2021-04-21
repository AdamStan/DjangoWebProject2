import sys
import time
from statistics import mean

from entities.models import FieldOfStudy
from .base_test import BaseTest, check_conflicts_in_result_dict
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
        first_plan = GraphAlgorithmRunner()
        result = first_plan.create_plan_async(min_hour=self.min_hour, max_hour=self.max_hour)
        return result


class GraphAlgoGoodResultsTests(BaseTest):
    HOW_MANY_TIMES_RUN = 10

    def setUp(self):
        super(GraphAlgoGoodResultsTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.min_hour = 8
        self.max_hour = 19

    def run_algorithm(self):
        first_plan = GraphAlgorithmRunner()
        result = first_plan.create_plan_async(min_hour=self.min_hour, max_hour=self.max_hour)
        result.append(check_conflicts_in_result_dict(first_plan.the_best_result[0]))
        return result

    def test_graph_algorithm_correctness(self):
        results = list()
        for _ in range(GraphAlgoGoodResultsTests.HOW_MANY_TIMES_RUN):
            results.append(self.run_algorithm())
        # counting generating with error
        error_rate = 0
        good_results = list()
        result_was_good = list()
        for res in results:
            if res[0] == "Exception":
                error_rate += 1
            else:
                good_results.append(res[1])
                result_was_good.append(res[2])

        min_value = min(good_results)
        max_value = max(good_results)
        mean_value = mean(good_results)
        time_in_seconds = "doesn't matter"
        times_was_run = GraphAlgoGoodResultsTests.HOW_MANY_TIMES_RUN

        report = BasicAlgorithmReport(time_in_seconds, mean_value, "graph algorithm",
                                      other_info_dict={"times_was_run": times_was_run,
                                                       "good_results": len(good_results), "errors": error_rate,
                                                       "min_value": min_value, "max_value": max_value,},
                                      lists_with_results=[good_results, result_was_good],
                                      file_name="report_graph_algo_conflicts_")
        report.create_report()
