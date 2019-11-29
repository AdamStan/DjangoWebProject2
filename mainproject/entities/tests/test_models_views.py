from django.test import TestCase
from ..models import *
from accounts.models import User
from datetime import time
from .test_entities import AbstractTestEntities
from ..urls import tab_models_urls

STATUS_REDIRECT = 302


class TestViewModelAdmin(TestCase):
    def setUp(self):
        user_admin = User.objects.create_superuser(
            username="admin", password="admin",
            name="adm", surname="adm_surname"
        )
        user_admin.save()
        self.client.login(username="admin", password="admin")

    def tearDown(self):
        self.client.logout()

    def test_all_models_views_admin(self):
        for url in tab_models_urls:
            response = self.client.get("/entities/" + url.pattern.__str__())
            self.assertEqual(response.status_code, AbstractTestEntities.status_ok)


class TestViewModelStudent(TestCase):
    def setUp(self):
        user_student = User.objects.create_student(
            username="student", password="student",
            name="std", surname="std"
        )
        user_student.save()
        self.client.login(username="student", password="student")

    def test_all_models_views_student(self):
        for url in tab_models_urls:
            response = self.client.get("/entities/" + url.pattern.__str__())
            self.assertEqual(response.status_code, STATUS_REDIRECT)


