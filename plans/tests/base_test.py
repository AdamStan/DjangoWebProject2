from accounts.add_data import add_data as add_account_data
from entities.add_data import add_entities

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
