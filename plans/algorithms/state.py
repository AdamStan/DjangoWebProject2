import sys
from datetime import time

from .algorithms_helper import get_events_by_day, check_action_can_be_done


class State:
    def __init__(self, plans):
        self.plans = plans


class Environment:

    def __init__(self, plans, scheduled_subjects, strategy, min_hour=8, max_hour=19, days=[1, 2, 3, 4, 5]):
        self.strategy = strategy
        self.plans = plans
        self.not_scheduled_subjects = scheduled_subjects.copy()
        self.scheduled_subjects = dict()
        for plan in plans:
            scheduled_subjects_dict = dict()
            for day in days:
                scheduled_subjects_dict[day] = list()
            self.scheduled_subjects[plan.title] = scheduled_subjects_dict
        # other parameters
        self.min_hour = min_hour
        self.max_hour = max_hour
        self.days = days

    def make_action(self, action):
        plan = action.plan
        subjects_in_plan_by_day = self.scheduled_subjects[plan.title]
        scheduled_subject = action.schedule_subject
        scheduled_subject.dayOfWeek = action.day
        scheduled_subject.whenStart = action.time
        scheduled_subject.whenFinnish = time(action.time.hour + scheduled_subject.how_long, 0, 0)
        subjects_in_plan_by_day[action.day].append(scheduled_subject)

    def get_cost_of_action(self, action):
        plan = action.plan
        subjects_in_plan = self.scheduled_subjects[plan.title]
        cost_before_for_debugging = self.strategy.get_value_of_plan(subjects_in_plan)
        cost = self.strategy.get_value_of_plan_after_action(subjects_in_plan, action)
        return cost

    def get_scheduled_subjects(self):
        return self.scheduled_subjects

    def get_available_actions(self, plan, scheduled_subject):
        actions = list()
        available_actions = list()
        for day in self.days:
            for hour in range(self.min_hour, self.max_hour):
                actions.append(Action(plan, scheduled_subject, hour, day))

        for action in actions:
            subjects_from_plan = self.scheduled_subjects[plan.title]
            if check_action_can_be_done(action, subjects_from_plan):
                available_actions.append(action)

        return available_actions

class Action:

    def __init__(self, plan, will_scheduled_subject, hour, day):
        self.plan = plan
        self.schedule_subject = will_scheduled_subject
        self.time = time(hour, 0, 0)
        self.day = day
