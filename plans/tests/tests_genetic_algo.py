import sys
import time
from statistics import mean

from entities.models import FieldOfStudy
from .base_test import BaseTest
from ..algorithms.genetic_algorithm import GeneticAlgorithmRunner
from ..report_generator import BasicAlgorithmReport


class GeneticAlgorithmTests(BaseTest):
    HOW_MANY_TIMES_RUN = 40

    def setUp(self):
        super(GeneticAlgorithmTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.min_hour = 8
        self.max_hour = 19
        self.generations = 24
        self.crossover = 0.8
        self.mutation = 0.2

    def test_improvement_algorithm(self):
        results = self.run_algorithm()
        self.assertNotEqual("Exception", results[0])

    def test_genetic_algorithm_performance(self):
        results = list()
        before = time.time_ns()
        for _ in range(GeneticAlgorithmTests.HOW_MANY_TIMES_RUN):
            results.append(self.run_algorithm())
        after = time.time_ns()

        error_rate = 0
        good_results = list()
        good_results_after = list()
        for res in results:
            if res[0] == "Exception":
                error_rate += 1
            else:
                good_results.append(res[1])
                good_results_after.append(res[2])

        min_value = min(good_results_after)
        max_value = max(good_results_after)
        mean_value = mean(good_results_after)

        time_in_seconds = (after - before) / 1_000_000_000
        times_was_run = GeneticAlgorithmTests.HOW_MANY_TIMES_RUN

        report = BasicAlgorithmReport(time_in_seconds, mean_value, "genetic algo tests",
                                      other_info_dict={"times_was_run": times_was_run,
                                                       "good_results": len(good_results_after), "errors": error_rate,
                                                       "min_value": min_value, "max_value": max_value,
                                                       "generations": self.generations,
                                                       "crossover rate": self.crossover,
                                                       "mutation rate": self.mutation},
                                      lists_with_results=[good_results, good_results_after],
                                      file_name="report_genetic_algo_")
        report.create_report()

    def run_algorithm(self):
        try:
            first_plan = GeneticAlgorithmRunner(self.generations, self.crossover, self.mutation)
            result = first_plan.create_plan_async(min_hour=self.min_hour, max_hour=self.max_hour)
            return result
        except Exception as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            return ["Exception", sys.maxsize]
