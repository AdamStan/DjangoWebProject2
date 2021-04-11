import sys
from statistics import mean

from entities.models import FieldOfStudy, Teacher, Room
from .base_test import BaseTest
from plans.algorithms import create_empty_plans, create_scheduled_subjects, \
    NeuralNetworkForThreeInputConcatenation
from ..algorithms.algorithms_helper import get_events_by_day, check_scheduled_subjects_in_plans, \
    group_subjects_by_teachers, \
    group_subjects_by_rooms, check_scheduled_subjects_with_lectures
from ..report_generator import BasicAlgorithmReport


class NeuralNetworkThreeInputGoodResultsTests(BaseTest):
    HOW_MANY_TIMES_RUN = 10

    def setUp(self):
        super(NeuralNetworkThreeInputGoodResultsTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.min_hour = 8
        self.max_hour = 19

    def run_algorithm(self, fields, teachers, rooms):
        results = list()
        plans = create_empty_plans(fields, self.how_many_plans, self.winter_or_summer)
        try:
            plans_scheduled_subjects = dict()

            for plan in plans:
                scheduled_subjects = create_scheduled_subjects(plan)
                plans_scheduled_subjects[plan.title] = scheduled_subjects

            first_plan = \
                NeuralNetworkForThreeInputConcatenation(teachers, plans=plans, rooms=rooms,
                                                        scheduled_subjects_in_plans=plans_scheduled_subjects,
                                                        min_hour=self.min_hour, max_hour=self.max_hour)
            out = first_plan.create_plan()
            out.append(self.check_conflicts_in_result(first_plan))
            results.append(out)

        except Exception as e:
            results.append(["Exception", sys.maxsize])
        return results

    def test_neural_network3_algorithm_correctness(self):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        fields = FieldOfStudy.objects.all()
        results = list()
        for i in range(NeuralNetworkThreeInputGoodResultsTests.HOW_MANY_TIMES_RUN):
            results += self.run_algorithm(fields, teachers, rooms)
            print(results)
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
        times_was_run = NeuralNetworkThreeInputGoodResultsTests.HOW_MANY_TIMES_RUN

        report = BasicAlgorithmReport(time_in_seconds, mean_value, "improvement_algo_tests",
                                      other_info_dict={"times_was_run": times_was_run,
                                                       "good_results": len(good_results), "errors": error_rate,
                                                       "min_value": min_value, "max_value": max_value,},
                                      lists_with_results=[good_results, result_was_good],
                                      file_name="report_nn_3_conflicts")
        report.create_report()

    def check_conflicts_in_result(self, generator_with_scheduled_subjects):
        # check conflicts in all plan
        for sch_subject_list in generator_with_scheduled_subjects.scheduled_subjects.values():
            # get subject by days and use function to check conflicts for that
            sch_by_days = get_events_by_day(sch_subject_list)
            are_correct = check_scheduled_subjects_in_plans(sch_by_days)
            if not are_correct:
                return True
        # check conflicts for teachers
        teachers_subjects = group_subjects_by_teachers(generator_with_scheduled_subjects.scheduled_subjects)
        # get subject by days and use function to check conflicts for that
        are_correct = check_scheduled_subjects_with_lectures(teachers_subjects)
        if not are_correct:
            return True
        # check conflicts for rooms
        rooms_subjects = group_subjects_by_rooms(generator_with_scheduled_subjects.scheduled_subjects)
        # get subject by days and use function to check conflicts for that
        are_correct = check_scheduled_subjects_with_lectures(rooms_subjects)
        if not are_correct:
            return True
        return False
