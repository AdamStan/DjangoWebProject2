import sys
import time
from statistics import mean

from entities.models import FieldOfStudy, Teacher, Room
from .base_test import BaseTest
from plans.algorithms import RandomPlanGenerator, create_empty_plans, create_scheduled_subjects
from ..report_generator import BasicAlgorithmReport


class RandomAlgorithmTests(BaseTest):
    HOW_MANY_TIMES_RUN = 100

    def setUp(self):
        super(RandomAlgorithmTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.tries = 10
        self.min_hour = 8
        self.max_hour = 19

    def test_random_algorithm(self):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        fields = FieldOfStudy.objects.all()
        results = self.run_algorithm(fields, teachers, rooms)
        self.assertEqual(10, len(results))

        error_rate = 0
        for res in results:
            if res[0] == "Exception":
                error_rate += 1
        self.assertLess(error_rate, 5)

    def test_random_algorithm_performance(self):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        fields = FieldOfStudy.objects.all()
        results = list()
        before = time.time_ns()
        for i in range(RandomAlgorithmTests.HOW_MANY_TIMES_RUN):
            results += self.run_algorithm(fields, teachers, rooms)
        after = time.time_ns()
        # odfiltrowanie listy z Exception...
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
        times_was_run = RandomAlgorithmTests.HOW_MANY_TIMES_RUN * self.tries

        report = BasicAlgorithmReport(time_in_seconds, mean_value, "random_algo_test",
                                      other_info_dict={"times_was_run": times_was_run,
                                                       "good_results": len(good_results), "errors": error_rate,
                                                       "min_value": min_value, "max_value": max_value},
                                      file_name="report_random_algo_")
        report.create_report()

    def run_algorithm(self, fields, teachers, rooms):
        results = list()
        for i in range(self.tries):
            plans = create_empty_plans(fields, self.how_many_plans, self.winter_or_summer)
            try:
                subjects_in_plans = list()
                for plan in plans:
                    scheduled_subjects = create_scheduled_subjects(plan, 15)
                    subjects_in_plans.append(scheduled_subjects)
                first_plan = RandomPlanGenerator(teachers, plans=plans, rooms=rooms,
                                                 scheduled_subjects_in_plans=subjects_in_plans,
                                                 how_many_plans=self.how_many_plans,
                                                 winter_or_summer=self.winter_or_summer,
                                                 weeks=15)
                results.append(first_plan.generate_plan(self.min_hour, self.max_hour))
            except Exception:
                results.append(["Exception", sys.maxsize])
        return results
