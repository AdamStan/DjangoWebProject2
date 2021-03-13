from accounts.add_data import add_data as add_account_data
from entities.add_data import add_entities

from django.test import TestCase


class BaseTest(TestCase):
    def setUp(self):
        add_account_data()
        add_entities()
