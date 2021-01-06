import logging as logger
import random
from datetime import time

from entities.models import FieldOfStudy, Teacher, Room, ScheduledSubject, Plan

from .random_algorithm import RandomPlanGenerator
from .algorithms_helper import create_empty_plans, get_events_by_day, check_action_can_be_done, \
    create_scheduled_subjects
from .state import Action


class GeneticAlgorithm:

    def __init__(self, number_of_generations, chance_of_crossover, chance_of_mutation, plans,
                 scheduled_subjects_in_plan, sch_subjects_teachers, sch_subjects_rooms, min_hour, max_hour):
        self.number_of_generations = number_of_generations
        self.crossover_rate = chance_of_crossover
        self.mutation_rate = chance_of_mutation
        self.min_hour = min_hour
        self.max_hour = max_hour

        self.plans = dict()
        for plan in plans:
            self.plans[str(plan.fieldOfStudy) + str(plan.semester)] = list()
        for plan in plans:
            self.plans[str(plan.fieldOfStudy) + str(plan.semester)].append(plan)

        # dict plan.title - key, list of scheduled_subjects - value
        self.scheduled_subjects = dict()
        for i in range(len(plans)):
            self.scheduled_subjects[plans[i].title] = scheduled_subjects_in_plan[i]
        # dict teacher - key, list of scheduled_subjects - value
        self.scheduled_subjects_to_teachers = sch_subjects_teachers
        # dict room - key, list of scheduled_subjects - value
        self.scheduled_subjects_to_rooms = sch_subjects_rooms

    def perform(self):
        for i in range(0, self.number_of_generations):
            print("generation: " + str(i))
            self.crossovers()
            self.mutations()

    def mutations(self):
        pass

    def crossovers(self):
        for plan_list in self.plans.values():
            for index in range(0, len(plan_list), 2):
                plan_to_cross = index + 1
                if plan_to_cross > len(plan_list) - 1:
                    plan_to_cross = index - 1
                if random.random() < self.crossover_rate:
                    self.crossover_plans(plan_list[index], plan_list[plan_to_cross])

    def crossover_plans(self, plan1, plan2):
        print("Plans crossover: " + plan1.title + ", " + plan2.title)
        sch_subjects_plan1 = self.scheduled_subjects[plan1.title]
        sch_subjects_plan2 = self.scheduled_subjects[plan2.title]
        sch_labs_plan1 = self.get_labs_in_plan(sch_subjects_plan1)
        sch_labs_plan2 = self.get_labs_in_plan(sch_subjects_plan2)

        for sch_lab1 in sch_labs_plan1:
            for sch_lab2 in sch_labs_plan2:
                if sch_lab1.subject == sch_lab2.subject:
                    sch_subjects_plan1_by_days = get_events_by_day(self.scheduled_subjects[plan1.title])
                    sch_subjects_plan2_by_days = get_events_by_day(self.scheduled_subjects[plan2.title])
                    action_from_1_to_2 = Action(plan2, sch_lab2, sch_lab1.whenStart.hour, sch_lab1.dayOfWeek,
                                                sch_lab1.teacher, sch_lab1.room)
                    action_from_2_to_1 = Action(plan1, sch_lab1, sch_lab2.whenStart.hour, sch_lab2.dayOfWeek,
                                                sch_lab2.teacher, sch_lab2.room)
                    # TODO: how to not check changing laboratory?
                    if check_action_can_be_done(action_from_1_to_2, sch_subjects_plan2_by_days) and \
                            check_action_can_be_done(action_from_2_to_1, sch_subjects_plan1_by_days):
                        print("crossover_works")
                        self.crossover_action(action_from_1_to_2)
                        self.crossover_action(action_from_2_to_1)
                    break

    def get_labs_in_plan(self, sch_subjects_list):
        labs = list()
        for sch_s in sch_subjects_list:
            if sch_s.type == ScheduledSubject.LABORATORY:
                labs.append(sch_s)
        return labs

    def crossover_action(self, action):
        scheduled_subject = action.schedule_subject
        scheduled_subject.dayOfWeek = action.day
        scheduled_subject.whenStart = action.time
        scheduled_subject.whenFinnish = time(action.time.hour + scheduled_subject.how_long, 0, 0)
        scheduled_subject.teacher = action.teacher
        scheduled_subject.room = action.room


class GeneticAlgorithmRunner:
    TRIES_FOR_NEW_PLAN_CREATION = 10

    def __init__(self, generations, crossover, mutation):
        self.mutation = mutation
        self.crossover = crossover
        self.generations = generations
        self.the_best_result = None

    def create_plan_async(self, winter_or_summer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8,
                          max_hour=19):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        result = {"Exception"}
        case = result == {"Exception"}
        logger.log(level=logger.INFO, msg="the case: " + str(case))

        tries_for_generating_plan = 0
        while result == {
            "Exception"} and tries_for_generating_plan < GeneticAlgorithmRunner.TRIES_FOR_NEW_PLAN_CREATION:
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

        self.the_best_result = result
        logger.log(level=logger.INFO, msg="Genetic algorithm starts - with deleting")
        self.make_generations(min_hour, max_hour)
        self.save_the_result()

    def create_plan_async_without_deleting(self, min_hour=8, max_hour=19):
        # create exactly one plan with random generator without deleting plans
        # improve it how many times you get
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        plans = Plan.objects.all()
        scheduled_subjects_list = []
        for plan in plans:
            bullshit = plan.fieldOfStudy.faculty
            scheduled_subjects = create_scheduled_subjects(plan, 15)
            scheduled_subjects_list.append(scheduled_subjects)
        result = {"Exception"}
        case = result == {"Exception"}
        logger.log(level=logger.INFO, msg="the case: " + str(case))

        tries_for_generating_plan = 0
        while result == {
            "Exception"} and tries_for_generating_plan < GeneticAlgorithmRunner.TRIES_FOR_NEW_PLAN_CREATION:
            try:
                first_plan = RandomPlanGenerator(teachers, plans, rooms)
                result = first_plan.generate_plan(min_hour, max_hour)
            except Exception as e:
                logger.log(level=logger.INFO, msg=e)
                import traceback
                traceback.print_tb(e.__traceback__)
                tries_for_generating_plan += 1

        self.the_best_result = result
        logger.log(level=logger.INFO, msg="Genetic algorithm starts - with deleting")
        self.make_generations(min_hour, max_hour)
        self.save_the_result()

    def save_the_result(self):
        # TODO: saves values from self.algorithm
        # if self.the_best_result:
        #     plans = self.the_best_result[0].plans
        #     sch_subject_plans = self.the_best_result[0].subjects_in_plans
        #     ScheduledSubject.objects.all().delete()
        #     Plan.objects.all().delete()
        #     # SAVE
        #     for plan in plans:
        #         plan.save()
        #     for i in range(len(plans)):
        #         title = sch_subject_plans[i][0].plan.title
        #         plan = Plan.objects.get(title=title)
        #         for sch_subject in sch_subject_plans[i]:
        #             sch_subject.plan = plan
        #             sch_subject.save()
        logger.log(level=logger.INFO, msg="Turn off!")

    def make_generations(self, min_hour, max_hour):
        if self.the_best_result:
            subjects_teachers = self.the_best_result[0].subjects_for_teachers
            subjects_rooms = self.the_best_result[0].subjects_in_room
            algorithm = GeneticAlgorithm(self.generations, self.crossover, self.mutation, self.the_best_result[0].plans,
                                         self.the_best_result[0].subjects_in_plans, subjects_teachers, subjects_rooms,
                                         min_hour, max_hour)
            algorithm.perform()
