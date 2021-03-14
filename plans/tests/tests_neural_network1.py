import sys
import time
from statistics import mean
import logging as log

from entities.models import FieldOfStudy, Teacher, Room
from .base_test import BaseTest
from plans.algorithms import create_empty_plans, create_scheduled_subjects, NeuralNetworkForOneInput
from ..report_generator import BasicAlgorithmReport


class NeuralNetworkOneInputTests(BaseTest):
    HOW_MANY_TIMES_RUN = 50

    def setUp(self):
        super(NeuralNetworkOneInputTests, self).setUp()
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

    def test_neural_network1_algorithm_performance(self):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        fields = FieldOfStudy.objects.all()
        results = list()
        before = time.time_ns()
        logger = log.getLogger("NeuralNetwork1")
        for i in range(NeuralNetworkOneInputTests.HOW_MANY_TIMES_RUN):
            logger.info("Next 10 tries, actual progress: " + str(i+1) + "/" + str(NeuralNetworkOneInputTests.HOW_MANY_TIMES_RUN))
            print("Next 10 tries, actual progress: " + str(i+1) + "/" + str(NeuralNetworkOneInputTests.HOW_MANY_TIMES_RUN))
            results += self.run_algorithm(fields, teachers, rooms)
        after = time.time_ns()
        # counting generating with error
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
        times_was_run = NeuralNetworkOneInputTests.HOW_MANY_TIMES_RUN * self.tries

        report = BasicAlgorithmReport(time_in_seconds, mean_value, "neural network one input - sequential model",
                                      other_info_dict={"times_was_run": times_was_run,
                                                       "good_results": len(good_results), "errors": error_rate,
                                                       "min_value": min_value, "max_value": max_value})
        report.create_report()

    def run_algorithm(self, fields, teachers, rooms):
        results = list()
        for _ in range(self.tries):
            plans = create_empty_plans(fields, self.how_many_plans, self.winter_or_summer)
            try:
                plans_scheduled_subjects = dict()

                for plan in plans:
                    scheduled_subjects = create_scheduled_subjects(plan)
                    plans_scheduled_subjects[plan.title] = scheduled_subjects

                first_plan = NeuralNetworkForOneInput(teachers, plans=plans, rooms=rooms,
                                                      scheduled_subjects_in_plans=plans_scheduled_subjects,
                                                      min_hour=self.min_hour, max_hour=self.max_hour)
                results.append(first_plan.create_plan())
            except Exception as e:
                results.append(["Exception", sys.maxsize])
        return results
