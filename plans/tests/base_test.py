from accounts.add_data import add_data as add_account_data
from entities.add_data import add_entities
from ..algorithms.algorithms_helper import get_events_by_day, check_scheduled_subjects_in_plans, \
    group_subjects_by_teachers, \
    group_subjects_by_rooms, check_scheduled_subjects_with_lectures

from django.test import TestCase


class BaseTest(TestCase):
    def setUp(self):
        add_account_data()
        add_entities()


def list_to_dict(values):
    new_dict = dict()
    for index in range(len(values)):
        new_dict[index + 1] = values[index]
    return new_dict


def check_conflicts_in_result_dict(generator_with_scheduled_subjects):
    """
    @param generator_with_scheduled_subjects: - contains dict named scheduled_subjects !
    @return: True if conflicts exists, False if there is no conflicts
    """
    # check conflicts in all plan
    for sch_subject_list in generator_with_scheduled_subjects.scheduled_subjects.values():
        # get subject by days and use function to check conflicts for that
        sch_by_days = get_events_by_day(sch_subject_list)
        are_correct = check_scheduled_subjects_in_plans(sch_by_days)
        if not are_correct:
            return True
    # check conflicts for teachers
    teachers_subjects = group_subjects_by_teachers(generator_with_scheduled_subjects.scheduled_subjects)
    # get subject by days and use function to check conflicts for that
    are_correct = check_scheduled_subjects_with_lectures(teachers_subjects)
    if not are_correct:
        return True
    # check conflicts for rooms
    rooms_subjects = group_subjects_by_rooms(generator_with_scheduled_subjects.scheduled_subjects)
    # get subject by days and use function to check conflicts for that
    are_correct = check_scheduled_subjects_with_lectures(rooms_subjects)
    if not are_correct:
        return True
    return False
