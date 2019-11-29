from django.db import transaction
from numpy import array, zeros
from random import randint, choice
from datetime import time
from copy import deepcopy
from .algorithm import ImprovementHelper
from .models import Room, Teacher, ScheduledSubject, Plan


class ImprovementManagerQuerySets:
    def __init__(self, plans, sch_subjects, teachers, rooms):
        self.scheduled_subjects = sch_subjects
        self.plans = plans
        self.day_of_week = [1, 2, 3, 4, 5, ]  # I've deleted 6 and 7 because we don't have saturday
        self.how_many_laboratory = 0
        self.how_many_lecture = 0
        self.success_lab = 0
        self.success_lec = 0

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
            print("Plan to change = " + str(plan_to_change))
            # 2. losujemy dzien do poki dzien nie jest pusty
            day = choice(self.day_of_week)
            while True:
                subjects_in_day = self.scheduled_subjects.filter(dayOfWeek=day, plan=plan_to_change)
                print("Przedmioty w dniu:" + str(subjects_in_day.count()))
                if subjects_in_day.count() == 0:
                    day = choice(self.day_of_week)
                else:
                    break
            # 3. z tego dnia wybieramy przedmiot
            subject_to_change = choice(subjects_in_day)
            ImprovementManagerQuerySets.show_subject(subject_to_change)
            # 4. liczymy wartosc planu
            value_before = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=plan_to_change))
            # 4.1 jesli jest to lab
            if subject_to_change.type == "LAB":
                if self.steps_for_laboratory(min_hour, max_hour, value_before, subject_to_change, plan_to_change):
                    print("Improving can be performed...")
                    self.success_lab += 1
                    transaction.savepoint_commit(sid)
                else:
                    print("Improving cannot be performed.")
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
                    ImprovementManagerQuerySets.show_subject(sub)
                    value = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=sub.plan))
                    values_before.append(value)
                    sub.whenStart = new_whenStart
                    sub.whenFinnish = new_whenFinnish
                    sub.dayOfWeek = new_dayOfWeek
                    print(value)
                    sub.save()

                print(":::AFTER:::")
                for sub in others_lectures:
                    ImprovementManagerQuerySets.show_subject(sub)
                    value = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=sub.plan))
                    values_after.append(value)
                    print(value)

                value_case = all(value_a <= value_b for value_b, value_a in zip(values_before, values_after))
                if value_case:
                    print("Zmiana jest dobra dla każdego planu")

                all_cases = True
                for sub in others_lectures:
                    case1 = ImprovementHelper.check_room_is_not_taken_exclude(sub, sub.room)
                    case2 = ImprovementHelper.check_teacher_can_teach_exclude(sub, sub.teacher)
                    case3 = ImprovementHelper.check_subject_to_subject_time(
                        sub,self.scheduled_subjects.filter(plan=sub.plan).exclude(id=subject_to_change.id))
                    all_cases = all_cases and case1 and case2 and case3

                if all_cases:
                    print("kejsy spelnione")

                if all_cases and value_case:
                    self.success_lec += 1
                    transaction.savepoint_commit(sid)
                else:
                    transaction.savepoint_rollback(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            print(str(e))
            raise e

    def steps_for_lecture(self):
        pass

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
        subject_to_change.whenStart = time(choice(available_hours_to_start), 0, 0)
        fin = subject_to_change.whenStart.hour + subject_to_change.how_long
        subject_to_change.whenFinnish = time(fin, 0, 0)
        # 4.1.2 check new value
        subject_to_change.save()
        value_after = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=plan_to_change))
        print("New value:" + str(value_after))

        isRoomTakenCorrectly = ImprovementHelper.check_room_is_not_taken_exclude(subject_to_change,
                                                                                 subject_to_change.room)
        teacher_can_teach = ImprovementHelper.check_teacher_can_teach_exclude(subject_to_change,
                                                                              subject_to_change.teacher)
        plan_is_correct = ImprovementHelper.check_subject_to_subject_time(subject_to_change,
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

    def show_subject(subject):
        print("[Subject:: " + str(subject.subject.name) + str(subject.dayOfWeek) + " " + str(subject.whenStart) + " " + str(subject.whenFinnish) + "]")

    def show_conclusion(self):
        print("Tries for lab: " + str(self.how_many_laboratory))
        print("Tries for lec: " + str(self.how_many_lecture))
        print("Success (lab): " + str(self.success_lab))
        print("Success (lec): " + str(self.success_lec))

def make_improvement(how_many=1):
    scheduled_subjects = ScheduledSubject.objects.all()
    rooms = Room.objects.all().order_by("id")
    teachers = Teacher.objects.all().order_by("user_id")
    plans = Plan.objects.all().order_by("id")

    instance = ImprovementManagerQuerySets(plans=plans, sch_subjects=scheduled_subjects, teachers=teachers, rooms=rooms)
    for i in range(0,how_many):
        instance.generation()

    instance.show_conclusion()
