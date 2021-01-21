import sys

from entities.models import FieldOfStudy, Teacher, Room
from .base_test import BaseTest
from plans.algorithms import RandomPlanAlgorithm, RandomPlanGenerator, create_empty_plans, create_scheduled_subjects


class RandomAlgorithmTests(BaseTest):
    def setUp(self):
        super(RandomAlgorithmTests, self).setUp()
        self.how_many_plans = 3
        self.winter_or_summer = FieldOfStudy.WINTER
        self.tries = 10

    def test_random_algorithm(self):
        self.min_hour = 8
        self.max_hour = 19
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        fields = FieldOfStudy.objects.all()
        plans = create_empty_plans(fields, self.how_many_plans, self.winter_or_summer)
        results = list()
        error_rate = 0
        for i in range(self.tries):
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
                error_rate += 1

        print(results)
        self.assertEqual(10, len(results))
        self.assertLess(error_rate, 5)
