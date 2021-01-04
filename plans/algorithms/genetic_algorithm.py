import logging as logger
from entities.models import FieldOfStudy, Teacher, Room, ScheduledSubject, Plan

from plans.algorithms import RandomPlanGenerator, create_empty_plans


class GeneticAlgorithm:
    TRIES_FOR_NEW_PLAN_CREATION = 10

    def __init__(self, generations, crossover, mutation):
        self.generations = generations
        self.the_best_result = None

    def create_plan_async(self, winter_or_summer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8,
                          max_hour=19):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        from django.db import connection
        connection.close()
        result = {"Exception"}
        case = result == {"Exception"}
        logger.log(level=logger.INFO, msg="the case: " + str(case))

        tries_for_generating_plan = 0
        while result == {"Exception"} and tries_for_generating_plan < GeneticAlgorithm.TRIES_FOR_NEW_PLAN_CREATION:
            try:
                fields_of_study = list(FieldOfStudy.objects.all())
                plans = create_empty_plans(fields_of_study, how_many_plans, winter_or_summer)
                # OnePlanGenerator.show_objects(plans)
                # in test purpose only!!!
                first_plan = RandomPlanGenerator(teachers, plans, rooms)
                result = first_plan.generate_plan(min_hour, max_hour)
            except Exception as e:
                logger.log(level=logger.INFO, msg=e)
                import traceback
                traceback.print_tb(e.__traceback__)
                tries_for_generating_plan += 1

        self.save_the_result(result_to_save=result)
        the_best_result = result
        logger.log(level=logger.INFO, msg="Improvement starts - with deleting")
        self.make_generations()

    def create_plan_async_without_deleting(self, min_hour=8, max_hour=19):
        # create exactly one plan with random generator without deleting plans
        # improve it how many times you get
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        plans = Plan.objects.all()

        from django.db import connection
        connection.close()
        result = {"Exception"}
        case = result == {"Exception"}
        logger.log(level=logger.INFO, msg="the case: " + str(case))

        tries_for_generating_plan = 0
        while result == {"Exception"} and tries_for_generating_plan < GeneticAlgorithm.TRIES_FOR_NEW_PLAN_CREATION:
            try:
                # OnePlanGenerator.show_objects(plans)
                # in test purpose only!!!
                first_plan = RandomPlanGenerator(teachers, plans, rooms)
                result = first_plan.generate_plan(min_hour, max_hour)
            except Exception as e:
                logger.log(level=logger.INFO, msg=e)
                import traceback
                traceback.print_tb(e.__traceback__)
                tries_for_generating_plan += 1

        self.save_the_result(result_to_save=result)
        self.the_best_result = result
        logger.log(level=logger.INFO, msg="Improvement starts - without deleting")
        self.make_generations()

    def save_the_result(self):
        if self.the_best_result:
            plans = self.the_best_result[0].plans
            sch_subject_plans = self.the_best_result[0].subjects_in_plans
            ScheduledSubject.objects.all().delete()
            Plan.objects.all().delete()
            # SAVE
            for plan in plans:
                plan.save()
            for i in range(len(plans)):
                title = sch_subject_plans[i][0].plan.title
                plan = Plan.objects.get(title=title)
                for sch_subject in sch_subject_plans[i]:
                    sch_subject.plan = plan
                    sch_subject.save()
        logger.log(level=logger.INFO, msg="Improvement algorithm saves plan")
