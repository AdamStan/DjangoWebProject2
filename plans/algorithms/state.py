from datetime import time

from entities.models import ScheduledSubject, Room, Teacher
from .algorithms_helper import get_events_by_day, check_action_can_be_done


class Environment:

    def __init__(self, plans, scheduled_subjects, strategy, teachers, rooms,
                 min_hour=8, max_hour=19, days=[1, 2, 3, 4, 5]):
        self.strategy = strategy
        self.plans = plans
        self.flat_scheduled_subjects = scheduled_subjects.copy()
        self.scheduled_subjects = dict()
        for plan in plans:
            scheduled_subjects_dict = dict()
            for day in days:
                scheduled_subjects_dict[day] = list()
            self.scheduled_subjects[plan.title] = scheduled_subjects_dict
        self.teachers = teachers
        self.rooms = rooms

        self.sch_subjects_rooms = dict()
        for room in rooms:
            scheduled_subjects_in_room = dict()
            for day in days:
                scheduled_subjects_in_room[day] = list()
            self.sch_subjects_rooms[room.id] = scheduled_subjects_in_room

        self.sch_subjects_teachers = dict()
        for teacher in teachers:
            scheduled_subjects_for_teacher = dict()
            for day in days:
                scheduled_subjects_for_teacher[day] = list()
            self.sch_subjects_teachers[teacher.user.id] = scheduled_subjects_for_teacher

        # other parameters
        self.min_hour = min_hour
        self.max_hour = max_hour
        self.days = days

    def make_action(self, action):
        plan = action.plan
        scheduled_subject = action.schedule_subject

        if scheduled_subject.type == ScheduledSubject.LECTURE:
            self.do_action_for_other_lectures(action)
        else:
            self.store_action(action, scheduled_subject, plan.title)

    def get_cost_of_action(self, action):
        plan = action.plan
        subjects_in_plan = self.scheduled_subjects[plan.title]
        cost = self.strategy.get_value_of_plan_after_action(subjects_in_plan, action)
        return cost

    def get_scheduled_subjects(self):
        return self.scheduled_subjects

    def get_available_actions(self, plan, scheduled_subject):
        available_actions = list()
        teachers_for_sch = Teacher.objects.filter(subject=scheduled_subject.subject)
        rooms_for_sch = Room.objects.filter(room_type=scheduled_subject.type)

        actions = self.prepare_actions(plan, scheduled_subject, teachers_for_sch, rooms_for_sch)
        for action in actions:
            subjects_from_plan = self.scheduled_subjects[plan.title]
            subjects_for_teacher = self.sch_subjects_teachers[action.teacher.user.id]
            subjects_for_room = self.sch_subjects_rooms[action.room.id]
            if check_action_can_be_done(action, subjects_from_plan)  \
                    and check_action_can_be_done(action, subjects_for_teacher) \
                    and check_action_can_be_done(action, subjects_for_room):
                available_actions.append(action)

        return available_actions

    def prepare_actions(self, plan, scheduled_subject, teachers_for_sch, rooms_for_sch):
        actions = []
        for day in self.days:
            for hour in range(self.min_hour, self.max_hour):
                for room in rooms_for_sch:
                    for teacher in teachers_for_sch:
                        actions.append(Action(plan, scheduled_subject, hour, day, teacher, room))
        return actions

    def do_action_for_other_lectures(self, action):
        lectures = dict()
        subject = action.schedule_subject.subject
        for sch_subject in self.flat_scheduled_subjects:
            if sch_subject.subject == subject and sch_subject.type == ScheduledSubject.LECTURE:
                lectures[sch_subject.plan.title] = sch_subject

        for plan_title, lecture in lectures.items():
            self.store_action(action, lecture, plan_title)

    def store_action(self, action, scheduled_subject, plan_title):
        scheduled_subject.dayOfWeek = action.day
        scheduled_subject.whenStart = action.time
        scheduled_subject.whenFinnish = time(action.time.hour + scheduled_subject.how_long, 0, 0)

        scheduled_subject.teacher = action.teacher
        self.sch_subjects_teachers[action.teacher.user.id][action.day].append(scheduled_subject)

        scheduled_subject.room = action.room
        self.sch_subjects_rooms[action.room.id][action.day].append(scheduled_subject)

        self.scheduled_subjects[plan_title][action.day].append(scheduled_subject)


class Action:

    def __init__(self, plan, will_scheduled_subject, hour, day, teacher, room):
        self.plan = plan
        self.schedule_subject = will_scheduled_subject
        self.time = time(hour, 0, 0)
        self.day = day
        self.teacher = teacher
        self.room = room
