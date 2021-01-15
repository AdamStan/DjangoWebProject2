import sys

from .algorithms_helper import check_action_can_be_done


class ValueOfPlanStrategy1:

    def get_value_of_plan(self, subjects_by_days):
        value = 0
        for day, subjects in subjects_by_days.items():
            if len(subjects) == 0:
                continue
            value += 1
            how_long_subjects_take = 0
            min_hour = sys.maxsize
            max_hour = -sys.maxsize
            for subject in subjects:
                how_long_subjects_take += subject.how_long
                if min_hour > subject.whenStart.hour:
                    min_hour = subject.whenStart.hour
                if max_hour < subject.whenFinnish.hour:
                    max_hour = subject.whenFinnish.hour
            value += max_hour - min_hour - how_long_subjects_take

        return value

    def get_value_of_plan_after_action(self, subjects_by_days, action):
        value = 0
        # check if action is legal
        if check_action_can_be_done(action, subjects_by_days):
            # calculate the value
            for day, subjects in subjects_by_days.items():
                subject_added = None
                if day == action.day:
                    subject_added = action.schedule_subject
                if len(subjects) == 0 and subject_added is None:
                    continue
                value += 1
                how_long_subjects_take = 0
                min_hour = sys.maxsize
                max_hour = -sys.maxsize
                for subject in subjects:
                    how_long_subjects_take += subject.how_long
                    if min_hour > subject.whenStart.hour:
                        min_hour = subject.whenStart.hour
                    if max_hour < subject.whenFinnish.hour:
                        max_hour = subject.whenFinnish.hour

                if subject_added:
                    how_long_subjects_take += subject_added.how_long
                    if min_hour > action.time.hour:
                        min_hour = action.time.hour
                    finish_time = action.time.hour + action.schedule_subject.how_long
                    if max_hour < finish_time:
                        max_hour = finish_time

                value += max_hour - min_hour - how_long_subjects_take
        return value
