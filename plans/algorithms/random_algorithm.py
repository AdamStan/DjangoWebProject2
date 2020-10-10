from entities.models import Subject, ScheduledSubject, Teacher, Plan, Room, FieldOfStudy
from multiprocessing import Process as MProcess
from random import randint, choice
from datetime import time

# :::STATIC VALUES:::
HOW_MANY_TRIES = 100

''' 
IN TEST PURPOSE ONLY
It will be request function:
'''

def create_plan(winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3):
    print("--> I GET ALL FROM DATABASE")
    teachers = Teacher.objects.all()
    rooms = Room.objects.all()
    fields_of_study = FieldOfStudy.objects.all()
    print("--> I'VE TAKEN WITH SUCCESS")
    result = ["Exception"]
    try:
        plans = OnePlanGenerator.create_empty_plans(fields_of_study, how_many_plans, winterOrSummer)
        # OnePlanGenerator.show_objects(plans)
        # in test purpose only!!!
        first_plan = OnePlanGenerator(teachers, plans, rooms)
        result = first_plan.generate_plan()
    except:
        print("Exception was thrown")
    return result


class OnePlanGenerator:
    def __init__(self, teachers, plans=None, rooms=None, scheduled_subjects_in_plans=None,
                 how_many_plans=3, winterOrSummer=FieldOfStudy.WINTER, weeks=15):
        self.teachers = list(teachers)
        # there will be the same index as in plans, teachers, rooms
        self.subjects_in_plans = []
        self.subjects_for_teachers = {}
        self.subjects_in_room = {}
        self.plans = plans

        if scheduled_subjects_in_plans:
            self.subjects_in_plans = scheduled_subjects_in_plans
        else:
            fields_of_study = FieldOfStudy.objects.all()
            self.plans = OnePlanGenerator.create_empty_plans(fields_of_study, how_many_plans, winterOrSummer)
            for plan in self.plans:
                scheduled_subjects = OnePlanGenerator.create_scheduled_subjects(plan, weeks)
                self.subjects_in_plans.append(scheduled_subjects)

        self.rooms = list(rooms)

        for room in self.rooms:
            self.subjects_in_room[room] = []

        for teacher in self.teachers:
            self.subjects_for_teachers[teacher] = []
        print("Initialize with success")

    @staticmethod
    def create_empty_plans(fields_of_study, how_many_plans, winter_or_summer):
        plans = []

        for field in fields_of_study:
            if field.whenDoesItStarts == winter_or_summer:
                sm = 1
            else:
                sm = 2
            for sem in range(sm, field.howManySemesters + 1, 2):
                for i in range(1, how_many_plans + 1):
                    title_of_plan = field.name + str(sem) + "_" + str(i) + "|" + field.degree
                    plans.append(Plan(title=title_of_plan, fieldOfStudy=field, semester=sem))
        return plans

    @staticmethod
    def create_scheduled_subjects(plan, weeks):
        subjects = Subject.objects.filter(fieldOfStudy=plan.fieldOfStudy, semester=plan.semester)
        list_of_scheduled_subjects = []
        for subject in subjects:
            bullshit = subject.fieldOfStudy.faculty
            if subject.lecture_hours and subject.lecture_hours > 0:
                list_of_scheduled_subjects.append(
                    ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LECTURE,
                                     how_long=int(subject.lecture_hours / weeks))
                )
            if subject.laboratory_hours and subject.laboratory_hours > 0:
                list_of_scheduled_subjects.append(
                    ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LABORATORY,
                                     how_long=int(subject.laboratory_hours / weeks))
                )
        return list_of_scheduled_subjects

    def generate_plan(self, min_hour=8, max_hour=19, days=[1,2,3,4,5]):
        """
        Creates timetable first time
        :param scheduled_subjects: subjects without schedule
        :param min_hour: first hour when subject can start
        :param max_hour: last hour when subject can start
        :param days: days in week 0 => sunday, 6=> saturday
        :param weeks: how many weeks semester can be
        :return: None
        """
        self.set_lectures_time(min_hour=min_hour, max_hour=max_hour, days=days)
        self.set_laboratory_time(min_hour=min_hour, max_hour=max_hour, days=days)
        self.set_rooms_to_subjects()
        self.set_teachers_to_class()
        return [self, self.calculate_value()]

    def set_lectures_time(self, min_hour=8, max_hour=19, days=[1,2,3,4,5]):
        """
        Randomizes days of week and hours when lectures will take place
        :param scheduled_subjects: subjects without schedule
        :param min_hour: first hour when subject can start
        :param max_hour: last hour when subject can start
        :param days: days in week 0 => sunday, 6=> saturday
        :param weeks: how many weeks semester can be
        :return None:
        """
        print("--- set lectures time ---")
        dict_lectures, dict_group_lectures = self.prepare_lectures()
        for sch_subject_list in dict_group_lectures.values():
            tries = HOW_MANY_TRIES
            while tries > 0:
                when_start = randint(min_hour, max_hour)
                which_day = choice(days)
                sch_subject_list[0].whenStart = time(when_start, 0, 0)
                sch_subject_list[0].dayOfWeek = which_day
                sch_subject_list[0].whenFinnish = time(when_start + sch_subject_list[0].how_long, 0, 0)
                check_for_this_key = ""
                for key, value in dict_lectures.items():
                    if value.compare_to(sch_subject_list[0]):
                        check_for_this_key = key
                        break
                if self.check_event_can_be_set(event=sch_subject_list[0], event_id=check_for_this_key, dict_of_subjects=dict_lectures):
                    for sch_subject in sch_subject_list:
                        sch_subject.whenStart = time(when_start, 0, 0)
                        sch_subject.dayOfWeek = which_day
                        sch_subject.whenFinnish = time(when_start + sch_subject_list[0].how_long, 0, 0)
                    break
            tries -= 1
            if tries == 0:
                raise Exception("lectures cannot be set!")

    def set_laboratory_time(self, min_hour=8, max_hour=19, days=[1,2,3,4,5]):
        """
        Randomizes days of week and hours when lectures will take place
        :param scheduled_subjects: subjects without schedule
        :param min_hour: first hour when subject can start
        :param max_hour: last hour when subject can start
        :param days: days in week 0 => sunday, 6=> saturday
        :param weeks: how many weeks semester can be
        :return None:
        """
        dict_laboratories, dict_all = self.prepare_laboratories()

        print("--- set laboratories time ---")
        for key, subject in dict_laboratories.items():
            tries = HOW_MANY_TRIES
            while tries > 0:
                when_start = randint(min_hour, max_hour)
                which_day = choice(days)
                subject.whenStart = time(when_start, 0, 0)
                subject.dayOfWeek = which_day
                subject.whenFinnish = time(when_start + subject.how_long, 0, 0)
                tries -= 1
                if self.check_event_can_be_set(event=subject, event_id=key, dict_of_subjects=dict_all):
                    break
                if tries == 0:
                    raise Exception("Laboratories cannot be set!")

    def set_rooms_to_subjects(self):
        self.set_rooms_for_lectures()
        self.set_rooms_for_laboratories()

    def set_rooms_for_lectures(self):
        dict_lectures, dict_group_lectures = self.prepare_lectures()
        for sch_subject_list in dict_group_lectures.values():
            rooms = list(filter(lambda x: (x.room_type == Room.LECTURE), self.rooms))
            while rooms:
                room = choice(rooms)
                sch_subject_list[0].room = room
                if self.check_room_can_be_set(room, sch_subject_list[0]):
                    for sch_subject in sch_subject_list:
                        sch_subject.room = room
                        self.subjects_in_room[room].append(sch_subject)
                    break
                rooms.remove(room)
            if len(rooms) == 0:
                OnePlanGenerator.show_subjects(list(filter(lambda x: (x.room_type == Room.LECTURE), self.rooms)))
                raise Exception("lectures cannot be set!")

    def set_rooms_for_laboratories(self):
        dict_laboratories, dict_all = self.prepare_laboratories()
        for sch_subject in dict_laboratories.values():
            rooms = list(filter(lambda x: (x.room_type == Room.LABORATORY), self.rooms))
            while rooms:
                room = choice(rooms)
                sch_subject.room = room
                if self.check_room_can_be_set(room, sch_subject):
                    sch_subject.room = room
                    self.subjects_in_room[room].append(sch_subject)
                    break
                rooms.remove(room)
            if len(rooms) == 0:
                for key, list_dupa in self.subjects_in_room.items():
                    if key.room_type == Room.LABORATORY:
                        print("***")
                        print(key)
                        OnePlanGenerator.show_subjects(list_dupa)
                print("Chujowy przedmiot:")
                OnePlanGenerator.show_subjects([sch_subject])
                raise Exception("laboratories cannot be set!")

    def set_teachers_to_class(self):
        self.teachers_to_lectures()
        self.teachers_to_labs()

    def teachers_to_lectures(self):
        dict_lectures, dict_group_lectures = self.prepare_lectures()
        for sch_subject_list in dict_group_lectures.values():
            teachers = list(sch_subject_list[0].subject.teachers.all())
            while teachers:
                teacher = choice(teachers)
                sch_subject_list[0].teacher = teacher
                if self.check_teacher_can_teach(teacher, sch_subject_list[0]):
                    for sch_subject in sch_subject_list:
                        sch_subject.teacher = teacher
                        self.subjects_for_teachers[teacher].append(sch_subject)
                    break
                teachers.remove(teacher)
            if len(teachers) == 0:
                OnePlanGenerator.show_subjects(sch_subject_list[0].subject.teachers.all())
                raise Exception("lectures cannot be set!")

    def teachers_to_labs(self):
        dict_laboratories, dict_all = self.prepare_laboratories()
        for sch_subject in dict_laboratories.values():
            teachers = list(sch_subject.subject.teachers.all())
            while teachers:
                teacher = choice(teachers)
                sch_subject.teacher = teacher
                if self.check_teacher_can_teach(teacher, sch_subject):
                    self.subjects_for_teachers[teacher].append(sch_subject)
                    break
                teachers.remove(teacher)
            if len(teachers) == 0:
                OnePlanGenerator.show_objects(sch_subject.subject.teachers.all())
                raise Exception("laboratories cannot be set!")

    def check_teacher_can_teach(self, teacher, sch_subject):
        teachers_subjects = self.subjects_for_teachers[teacher]
        for event in teachers_subjects:
            difference_between_starts = abs(event.whenStart.hour - sch_subject.whenStart.hour)
            difference_between_ends = abs(event.whenFinnish.hour - sch_subject.whenFinnish.hour)
            is_the_same_day = event.dayOfWeek == sch_subject.dayOfWeek
            if is_the_same_day and \
                    (difference_between_starts + difference_between_ends) < (event.how_long + sch_subject.how_long):
                return False

        return True

    def check_room_can_be_set(self, room, sch_subject):
        scheduled_subjects_in_room = self.subjects_in_room[room]
        for event in scheduled_subjects_in_room:
            difference_between_starts = abs(event.whenStart.hour - sch_subject.whenStart.hour)
            difference_between_ends = abs(event.whenFinnish.hour - sch_subject.whenFinnish.hour)
            is_the_same_day = event.dayOfWeek == sch_subject.dayOfWeek
            if is_the_same_day and \
                    (difference_between_starts + difference_between_ends) < (event.how_long + sch_subject.how_long):
                return False

        return True

    def check_event_can_be_set(self, event, event_id, dict_of_subjects):
        # search the subject from plan
        for key, value in dict_of_subjects.items():
            if event_id[0:3] == key[0:3] and event_id != key:
                try:
                    if event.dayOfWeek == dict_of_subjects[key].dayOfWeek:
                        difference_between_starts = abs(event.whenStart.hour - dict_of_subjects[key].whenStart.hour)
                        difference_between_ends = abs(event.whenFinnish.hour - dict_of_subjects[key].whenFinnish.hour)
                        if (difference_between_starts + difference_between_ends) < (event.how_long + dict_of_subjects[key].how_long):
                            return False
                except AttributeError:
                    return True
        return True

    def prepare_lectures(self):
        dict_lectures = {}
        for list_index in range(0, len(self.subjects_in_plans)):
            for subject_index in range(len(self.subjects_in_plans[list_index])):
                if self.subjects_in_plans[list_index][subject_index].type == ScheduledSubject.LECTURE:
                    new_id = str(list_index) + "|||" + str(subject_index)
                    dict_lectures[new_id] = self.subjects_in_plans[list_index][subject_index]

        dict_group_lectures = {}

        for sch_subject in dict_lectures.values():
            dict_group_lectures[sch_subject.subject] = []

        for sch_subject in dict_lectures.values():
            dict_group_lectures[sch_subject.subject].append(sch_subject)

        return dict_lectures, dict_group_lectures

    def prepare_laboratories(self):
        # dictionary for all laboratories
        dict_laboratories = {}
        for list_index in range(0, len(self.subjects_in_plans)):
            for subject_index in range(len(self.subjects_in_plans[list_index])):
                if self.subjects_in_plans[list_index][subject_index].type == ScheduledSubject.LABORATORY:
                    new_id = str(list_index) + "|||" + str(subject_index)
                    dict_laboratories[new_id] = self.subjects_in_plans[list_index][subject_index]

        # dictionary for all events
        dict_all = {}
        for list_index in range(0, len(self.subjects_in_plans)):
            for subject_index in range(len(self.subjects_in_plans[list_index])):
                new_id = str(list_index) + "|||" + str(subject_index)
                dict_all[new_id] = self.subjects_in_plans[list_index][subject_index]

        return dict_laboratories, dict_all

    def calculate_value(self):
        value = 0
        for sch_subject_list in self.subjects_in_plans:
            value += self.value_for_plan(sch_subject_list)
        return value

    def value_for_plan(self, subjects_in_plan, days=[1,2,3,4,5]):
        """
        formula: days - empty days +  (end - start - all how long)
        :param subjects_in_plan:
        :return:
        """
        values = []
        value = 0
        for i in range(0, len(days)):
            values.append(1)
            subjects_how_long, first_hour, last_hour = 0, 24, 0
            list_of_subjects_in_one_day = self.get_events_from_one_day(subjects_in_plan, i+1)
            for subject in list_of_subjects_in_one_day:
                if subject.whenStart.hour < first_hour:
                    first_hour = subject.whenStart.hour
                if subject.whenFinnish.hour > last_hour:
                    last_hour = subject.whenFinnish.hour
                subjects_how_long += subject.how_long
            if not list_of_subjects_in_one_day:
                values[i] -= 1
            else:
                values[i] += last_hour - first_hour - subjects_how_long
            value += values[i]

        return value

    def get_events_from_one_day(self, subjects_in_plan, day_int):
        subjects_in_one_day = []
        for subject in subjects_in_plan:
            if subject.dayOfWeek == day_int:
                subjects_in_one_day.append(subject)
        return subjects_in_one_day

    def show(self):
        for events in self.subjects_in_plans.values():
            print("+++------------+++")
            for event in events:
                print(event)

    # DO NOT USE IT!!!
    def save_result(self):
        Plan.objects.all().delete()
        ScheduledSubject.objects.all().delete()
        for plan in self.plans:
            plan.save()
        for sch_subject_list in self.subjects_in_plans:
            sch_subject_list[0].plan.save()
            for sch_subject in sch_subject_list:
                sch_subject.save()

    @staticmethod
    def show_objects(objects):
        for obj in objects:
            print(str(obj))

    @staticmethod
    def show_subjects(scheduled_subjects):
        for sch in scheduled_subjects:
            print(str(sch) + ", " + str(sch.whenStart) + ", " + str(sch.whenFinnish) + ", day:" + str(sch.dayOfWeek)
                  + ", how_long: " + str(sch.how_long))
