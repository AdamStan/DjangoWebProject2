import sys
import time
from statistics import mean
import logging as log

from entities.models import FieldOfStudy, Teacher, Room
from .base_test import BaseTest, check_conflicts_in_result_dict
from plans.algorithms import create_empty_plans, create_scheduled_subjects, NeuralNetworkForOneInput
from ..report_generator import BasicAlgorithmReport


class NeuralNetworkOneInputTests(BaseTest):
    HOW_MANY_TIMES_RUN = 100

    def setUp(self):
        super(NeuralNetworkOneInputTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.tries = 1
        self.min_hour = 8
        self.max_hour = 19

    # def test_random_algorithm(self):
    #     teachers = Teacher.objects.all()
    #     rooms = Room.objects.all()
    #     fields = FieldOfStudy.objects.all()
    #     results = self.run_algorithm(fields, teachers, rooms)
    #     self.assertEqual(10, len(results))
    #
    #     error_rate = 0
    #     for res in results:
    #         if res[0] == "Exception":
    #             error_rate += 1
    #     self.assertLess(error_rate, 5, "The error rate is " + str(error_rate/self.tries))

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
                                                       "min_value": min_value, "max_value": max_value},
                                      file_name="report_nn1_")
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
#
#
# class NeuralNetworkOneInputGoodResultsTests(BaseTest):
#     HOW_MANY_TIMES_RUN = 10
#
#     def setUp(self):
#         super(NeuralNetworkOneInputGoodResultsTests, self).setUp()
#         self.how_many_plans = 3
#         self.winter_or_summer = FieldOfStudy.WINTER
#         self.min_hour = 8
#         self.max_hour = 19
#
#     def run_algorithm(self, fields, teachers, rooms):
#         results = list()
#         plans = create_empty_plans(fields, self.how_many_plans, self.winter_or_summer)
#         try:
#             plans_scheduled_subjects = dict()
#
#             for plan in plans:
#                 scheduled_subjects = create_scheduled_subjects(plan)
#                 plans_scheduled_subjects[plan.title] = scheduled_subjects
#
#             first_plan = \
#                 NeuralNetworkForOneInput(teachers, plans=plans, rooms=rooms,
#                                          scheduled_subjects_in_plans=plans_scheduled_subjects,
#                                          min_hour=self.min_hour, max_hour=self.max_hour)
#             out = first_plan.create_plan()
#             out.append(check_conflicts_in_result_dict(first_plan))
#             results.append(out)
#
#         except Exception as e:
#             results.append(["Exception", sys.maxsize])
#         return results
#
#     def test_neural_network1_algorithm_correctness(self):
#         teachers = Teacher.objects.all()
#         rooms = Room.objects.all()
#         fields = FieldOfStudy.objects.all()
#         results = list()
#         for i in range(NeuralNetworkOneInputGoodResultsTests.HOW_MANY_TIMES_RUN):
#             results += self.run_algorithm(fields, teachers, rooms)
#             print(results)
#         # counting generating with error
#         error_rate = 0
#         good_results = list()
#         result_was_good = list()
#         for res in results:
#             if res[0] == "Exception":
#                 error_rate += 1
#             else:
#                 good_results.append(res[1])
#                 result_was_good.append(res[2])
#
#         min_value = min(good_results)
#         max_value = max(good_results)
#         mean_value = mean(good_results)
#         time_in_seconds = "doesn't matter"
#         times_was_run = NeuralNetworkOneInputGoodResultsTests.HOW_MANY_TIMES_RUN
#
#         report = BasicAlgorithmReport(time_in_seconds, mean_value, "neural networks 1",
#                                       other_info_dict={"times_was_run": times_was_run,
#                                                        "good_results": len(good_results), "errors": error_rate,
#                                                        "min_value": min_value, "max_value": max_value,},
#                                       lists_with_results=[good_results, result_was_good],
#                                       file_name="report_nn_1_conflicts_")
#         report.create_report()
