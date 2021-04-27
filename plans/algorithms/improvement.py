import logging as logger
from django.db import transaction
from random import choice
from datetime import time

from . import RandomPlanGenerator
from .algorithms import AlgorithmsHelper
from entities.models import Room, Teacher, ScheduledSubject, Plan, FieldOfStudy
from .algorithms_helper import create_empty_plans, get_events_by_day
from .value_strategies import ValueOfPlanStrategy1


class ImprovementManagerQuerySets:
    def __init__(self, plans, sch_subjects, teachers, rooms):
        self.scheduled_subjects = sch_subjects
        self.plans = plans
        self.day_of_week = [1, 2, 3, 4, 5, ]  # I've deleted 6 and 7 because we don't have saturday
        self.how_many_laboratory = 0
        self.how_many_lecture = 0
        self.success_lab = 0
        self.success_lec = 0
        self.value_strategy = ValueOfPlanStrategy1()

    @transaction.atomic
    def generation(self, min_hour=8, max_hour=19):
        """
        One try to improve random plan
        :param min_hour: min_hour when subject can start
        :param max_hour: max hout when subject can start
        :return: None
        """
        sid = transaction.savepoint()
        try:
            # 1. losujemy plan
            plan_to_change = choice(self.plans)
            # 2. losujemy dzien do poki dzien nie jest pusty
            day = choice(self.day_of_week)
            while True:
                subjects_in_day = self.scheduled_subjects.filter(dayOfWeek=day, plan=plan_to_change)
                if subjects_in_day.count() == 0:
                    day = choice(self.day_of_week)
                else:
                    break
            # 3. z tego dnia wybieramy przedmiot
            subject_to_change = choice(subjects_in_day)
            # 4. liczymy wartosc planu
            value_before = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=plan_to_change))
            # 4.1 jesli jest to lab
            if subject_to_change.type == "LAB":
                if self.steps_for_laboratory(min_hour, max_hour, value_before, subject_to_change, plan_to_change):
                    self.success_lab += 1
                    transaction.savepoint_commit(sid)
                else:
                    transaction.savepoint_rollback(sid)
            # 4.2 jesli jest to lec
            elif subject_to_change.type == "LEC":
                self.how_many_lecture += 1
                # 4.1.1 losujemy nowe wartosci
                new_dayOfWeek = choice(self.day_of_week)
                subject_to_change.dayOfWeek = new_dayOfWeek
                available_hours_to_start = self.get_available_hours(min_hour, max_hour, subjects_in_day,
                                                                    subject_to_change)
                new_whenStart = time(choice(available_hours_to_start), 0, 0)
                fin = new_whenStart.hour + subject_to_change.how_long
                new_whenFinnish = time(fin, 0, 0)

                # 4.1.2 check new value
                others_lectures = ScheduledSubject.objects.filter(subject=subject_to_change.subject,
                                                                  type=subject_to_change.type)
                values_after = []
                values_before = []
                for sub in others_lectures:
                    value = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=sub.plan))
                    values_before.append(value)
                    sub.whenStart = new_whenStart
                    sub.whenFinnish = new_whenFinnish
                    sub.dayOfWeek = new_dayOfWeek
                    sub.save()

                for sub in others_lectures:
                    value = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=sub.plan))
                    values_after.append(value)

                value_case = all(value_a <= value_b for value_b, value_a in zip(values_before, values_after))

                all_cases = True
                for sub in others_lectures:
                    case1 = AlgorithmsHelper.check_room_is_not_taken_exclude(sub, sub.room)
                    case2 = AlgorithmsHelper.check_teacher_can_teach_exclude(sub, sub.teacher)
                    case3 = AlgorithmsHelper.check_subject_to_subject_time(
                        sub,self.scheduled_subjects.filter(plan=sub.plan).exclude(id=subject_to_change.id))
                    all_cases = all_cases and case1 and case2 and case3

                if all_cases and value_case:
                    self.success_lec += 1
                    transaction.savepoint_commit(sid)
                else:
                    transaction.savepoint_rollback(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            print(str(e))
            raise e

    def steps_for_laboratory(self, min_hour, max_hour, value_before, subject_to_change, plan_to_change):
        """
        :param min_hour:
        :param max_hour:
        :param value_before
        :param subject_to_change:
        :param plan_to_change:
        :return: true if are conditionals are correct
        """
        self.how_many_laboratory += 1
        subject_to_change.dayOfWeek = choice(self.day_of_week)
        subjects_in_day = self.scheduled_subjects.filter(dayOfWeek=subject_to_change.dayOfWeek, plan=plan_to_change)
        available_hours_to_start = self.get_available_hours(min_hour, max_hour, subjects_in_day,
                                                            subject_to_change)
        if len(available_hours_to_start) == 0:
            return False
        subject_to_change.whenStart = time(choice(available_hours_to_start), 0, 0)
        fin = subject_to_change.whenStart.hour + subject_to_change.how_long
        subject_to_change.whenFinnish = time(fin, 0, 0)
        # 4.1.2 check new value
        subject_to_change.save()
        value_after = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=plan_to_change))

        isRoomTakenCorrectly = AlgorithmsHelper.check_room_is_not_taken_exclude(subject_to_change,
                                                                                subject_to_change.room)
        teacher_can_teach = AlgorithmsHelper.check_teacher_can_teach_exclude(subject_to_change,
                                                                             subject_to_change.teacher)
        plan_is_correct = AlgorithmsHelper.check_subject_to_subject_time(subject_to_change,
                                                                         self.scheduled_subjects.filter(
                                                                              plan=plan_to_change).exclude(
                                                                              id=subject_to_change.id))
        return isRoomTakenCorrectly and teacher_can_teach and plan_is_correct and value_before > value_after

    def get_available_hours(self, min_hour, max_hour, subjects_in_day, subject_to_change):
        available_hours_to_start = []
        for i in range(min_hour, max_hour + 1):
            available_hours_to_start.append(i)

        for event in subjects_in_day:
            if not subject_to_change.compare_to(event):
                for i in range(event.whenStart.hour, event.whenFinnish.hour):
                    if i in available_hours_to_start:
                        available_hours_to_start.remove(i)

        return available_hours_to_start

    def value_for_plan(self, subjects_in_plan):
        """
        formula: days - empty days +  (end - start - all how long)
        :param subjects_in_plan:
        :return:
        """
        value = 5

        for day in self.day_of_week:
            subjects_how_long, first_hour, last_hour = 0, 24, 0
            list_of_subjects_in_one_day = subjects_in_plan.filter(dayOfWeek=day)
            for subject in list_of_subjects_in_one_day:
                if subject.whenStart.hour < first_hour:
                    first_hour = subject.whenStart.hour
                if subject.whenFinnish.hour > last_hour:
                    last_hour = subject.whenFinnish.hour
                subjects_how_long += subject.how_long

            if not list_of_subjects_in_one_day:  # checks that list is empty
                value -= 1
            else:
                value += last_hour - first_hour - subjects_how_long

        return value

    def calculate_value(self):
        value = 0
        sch_subjects_by_plan = self.create_scheduled_subjects_by_plan()
        for sch_subject_list in sch_subjects_by_plan.values():
            sch_subjects_by_days = get_events_by_day(sch_subject_list)
            value += self.value_strategy.get_value_of_plan(sch_subjects_by_days)
        return value

    def create_scheduled_subjects_by_plan(self):
        sch_by_plans = dict()
        for sch_subject in self.scheduled_subjects:
            if sch_subject.plan.title not in sch_by_plans:
                sch_by_plans[sch_subject.plan.title] = []
            sch_by_plans[sch_subject.plan.title].append(sch_subject)
        return sch_by_plans

    def show_conclusion(self):
        print("Tries for lab: " + str(self.how_many_laboratory))
        print("Tries for lec: " + str(self.how_many_lecture))
        print("Success (lab): " + str(self.success_lab))
        print("Success (lec): " + str(self.success_lec))
        return self.how_many_laboratory, self.how_many_lecture, self.success_lab, self.success_lec


def make_improvement(how_many=1):
    scheduled_subjects = ScheduledSubject.objects.all()
    rooms = Room.objects.all().order_by("id")
    teachers = Teacher.objects.all().order_by("user_id")
    plans = Plan.objects.all().order_by("id")

    instance = ImprovementManagerQuerySets(plans=plans, sch_subjects=scheduled_subjects, teachers=teachers, rooms=rooms)
    for i in range(0, how_many):
        instance.generation()

    tries_lab, tries_lec, suc_lab, suc_lec = instance.show_conclusion()
    print("Results after improvements")
    print(instance.calculate_value())
    return instance.calculate_value(), tries_lab, tries_lec, suc_lab, suc_lec


class ImprovementAlgorithm:
    TRIES_FOR_NEW_PLAN_CREATION = 10

    def __init__(self, tries):
        self.tries = tries
        self.the_best_result = None

    def create_plan_async(self, winter_or_summer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8,
                          max_hour=19):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        result = {"Exception"}
        case = result == {"Exception"}
        logger.log(level=logger.INFO, msg="the case: " + str(case))

        tries_for_generating_plan = 0
        while result == {"Exception"} and tries_for_generating_plan < ImprovementAlgorithm.TRIES_FOR_NEW_PLAN_CREATION:
            try:
                fields_of_study = list(FieldOfStudy.objects.all())
                plans = create_empty_plans(fields_of_study, how_many_plans, winter_or_summer)
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
        print("Result before improvements")
        print(result)
        logger.log(level=logger.INFO, msg="Improvement starts - with deleting")
        return [first_plan, make_improvement(self.tries), result[1]]

    def create_plan_async_without_deleting(self, min_hour=8, max_hour=19):
        # create exactly one plan with random generator without deleting plans
        # improve it how many times you get
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        plans = Plan.objects.all()

        result = {"Exception"}
        case = result == {"Exception"}
        logger.log(level=logger.INFO, msg="the case: " + str(case))

        tries_for_generating_plan = 0
        while result == {"Exception"} and tries_for_generating_plan < ImprovementAlgorithm.TRIES_FOR_NEW_PLAN_CREATION:
            try:
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
        make_improvement(self.tries)
        return [first_plan]

    def save_the_result(self, result_to_save):
        if result_to_save:
            plans = result_to_save[0].plans
            sch_subject_plans = result_to_save[0].subjects_in_plans
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
            self.the_best_result = result_to_save
        logger.log(level=logger.INFO, msg="Improvement algorithm saves plan")

    def save_the_best_result(self):
        logger.log(level=logger.INFO, msg="Improvement algorithm not implements save_the_best_result, consider removing")
