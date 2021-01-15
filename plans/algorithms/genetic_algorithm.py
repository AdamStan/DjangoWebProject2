import logging as logger
import random
from datetime import time

from entities.models import FieldOfStudy, Teacher, Room, ScheduledSubject, Plan

from .random_algorithm import RandomPlanGenerator
from .algorithms_helper import create_empty_plans, get_events_by_day, check_action_can_be_done, \
    create_scheduled_subjects, check_room_can_be_set, check_teacher_can_teach, check_hour_is_available, \
    get_the_same_lecture
from .state import Action


class GeneticAlgorithm:

    def __init__(self, number_of_generations, chance_of_crossover, chance_of_mutation, plans,
                 scheduled_subjects_in_plan, sch_subjects_teachers, sch_subjects_rooms, min_hour, max_hour):
        self.number_of_generations = number_of_generations
        self.crossover_rate = chance_of_crossover
        self.mutation_rate = chance_of_mutation
        self.min_hour = min_hour
        self.max_hour = max_hour
        # TODO: pass as parameter
        self.days = [1, 2, 3, 4, 5]

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
        for plan_title, scheduled_subjects in self.scheduled_subjects.items():
            for sch_subject in scheduled_subjects:
                if self.mutation_rate > random.random():
                    self.mutate_sch_subject(sch_subject)
                    break

    def mutate_sch_subject(self, sch_subject):
        teachers = list(sch_subject.subject.teachers.all())
        rooms = list(Room.objects.filter(room_type=sch_subject.type))
        if sch_subject.type == ScheduledSubject.LABORATORY:
            print("Make steps to mutate laboratory")
            other_subjects_in_plan = self.scheduled_subjects[sch_subject.plan.title]
            other_subjects_in_plan = get_events_by_day(other_subjects_in_plan)
            while True:
                room_new = random.choice(rooms)
                teacher_new = random.choice(teachers)
                new_day = random.choice(self.days)

                available_hours = []
                for hour in range(self.min_hour, self.max_hour):
                    if check_hour_is_available(hour, other_subjects_in_plan[new_day], sch_subject.how_long):
                        available_hours.append(hour)

                if len(available_hours) < 1:
                    continue

                start_hour = time(random.choice(available_hours), 0, 0)
                end_hour = time(start_hour.hour + sch_subject.how_long, 0, 0)
                older_start_hour = sch_subject.whenStart
                older_end_hour = sch_subject.whenFinnish
                older_day = sch_subject.dayOfWeek

                sch_subject.whenStart = start_hour
                sch_subject.whenFinnish = end_hour
                sch_subject.dayOfWeek = new_day
                if check_teacher_can_teach(sch_subject, self.scheduled_subjects_to_teachers[teacher_new]) \
                        and check_room_can_be_set(sch_subject, self.scheduled_subjects_to_rooms[room_new]):
                    self.scheduled_subjects_to_teachers[sch_subject.teacher].remove(sch_subject)
                    self.scheduled_subjects_to_rooms[sch_subject.room].remove(sch_subject)
                    self.scheduled_subjects_to_teachers[teacher_new].append(sch_subject)
                    self.scheduled_subjects_to_rooms[room_new].append(sch_subject)
                    sch_subject.teacher = teacher_new
                    sch_subject.room = room_new
                    print("mutation for lab: " + str(sch_subject) + "; was made.")
                    break
                else:
                    sch_subject.whenStart = older_start_hour
                    sch_subject.whenFinnish = older_end_hour
                    sch_subject.dayOfWeek = older_day
        else:
            print("Make steps to mutate lecture")
            current_plan = sch_subject.plan
            plan_all = self.plans[str(current_plan.fieldOfStudy) + str(current_plan.semester)]
            plans_sch_subjects = dict()
            for plan in plan_all:
                plans_sch_subjects[plan.title] = get_events_by_day(self.scheduled_subjects[plan.title])

            while True:
                room_new = random.choice(rooms)
                teacher_new = random.choice(teachers)
                new_day = random.choice(self.days)

                available_hours = []
                for hour in range(self.min_hour, self.max_hour):
                    is_available = True
                    for plan_sch_subjects_ in plans_sch_subjects.values():
                        is_available = is_available and check_hour_is_available(hour, plan_sch_subjects_[new_day],
                                                                                sch_subject.how_long)
                    if is_available:
                        available_hours.append(hour)

                if len(available_hours) < 1:
                    continue

                start_hour = time(random.choice(available_hours), 0, 0)
                end_hour = time(start_hour.hour + sch_subject.how_long, 0, 0)
                older_start_hour = sch_subject.whenStart
                older_end_hour = sch_subject.whenFinnish
                older_day = sch_subject.dayOfWeek

                sch_subject.whenStart = start_hour
                sch_subject.whenFinnish = end_hour
                sch_subject.dayOfWeek = new_day

                if check_teacher_can_teach(sch_subject, self.scheduled_subjects_to_teachers[teacher_new]) \
                        and check_room_can_be_set(sch_subject, self.scheduled_subjects_to_rooms[room_new]):
                    lectures_to_modify = list()
                    for plan in plan_all:
                        lecture = get_the_same_lecture(sch_subject, self.scheduled_subjects[plan.title])
                        if lecture is None:
                            print("It shouldn't happened!")
                            raise Exception("This lecture: " + str(sch_subject) + ", was not found in plan: " +
                                            str(plan))
                        lectures_to_modify.append(lecture)
                    for lecture in lectures_to_modify:
                        self.scheduled_subjects_to_teachers[lecture.teacher].remove(lecture)
                        self.scheduled_subjects_to_rooms[lecture.room].remove(lecture)
                        self.scheduled_subjects_to_teachers[teacher_new].append(lecture)
                        self.scheduled_subjects_to_rooms[room_new].append(lecture)
                        lecture.teacher = teacher_new
                        lecture.room = room_new
                        lecture.whenStart = start_hour
                        lecture.whenFinnish = end_hour
                        lecture.dayOfWeek = new_day
                    print("mutation for lecture: " + str(sch_subject) + "; was made.")
                    break
                else:
                    sch_subject.whenStart = older_start_hour
                    sch_subject.whenFinnish = older_end_hour
                    sch_subject.dayOfWeek = older_day

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
                    # how to not check changing laboratory? -
                    # doesn't matter, if laboratories are in the same time there is no reason to swap
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

        self.scheduled_subjects_to_rooms[scheduled_subject.room].remove(scheduled_subject)
        scheduled_subject.room = action.room
        self.scheduled_subjects_to_rooms[action.room].append(scheduled_subject)

        self.scheduled_subjects_to_teachers[scheduled_subject.teacher].remove(scheduled_subject)
        scheduled_subject.teacher = action.teacher
        self.scheduled_subjects_to_teachers[action.teacher].append(scheduled_subject)


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
        while result == {"Exception"} \
                and tries_for_generating_plan < GeneticAlgorithmRunner.TRIES_FOR_NEW_PLAN_CREATION:
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
        while result == {"Exception"} \
                and tries_for_generating_plan < GeneticAlgorithmRunner.TRIES_FOR_NEW_PLAN_CREATION:
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
        print("result was saved")

    def make_generations(self, min_hour, max_hour):
        if self.the_best_result:
            subjects_teachers = self.the_best_result[0].subjects_for_teachers
            subjects_rooms = self.the_best_result[0].subjects_in_room
            algorithm = GeneticAlgorithm(self.generations, self.crossover, self.mutation, self.the_best_result[0].plans,
                                         self.the_best_result[0].subjects_in_plans, subjects_teachers, subjects_rooms,
                                         min_hour, max_hour)
            algorithm.perform()
