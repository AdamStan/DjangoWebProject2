from django.test import TestCase
from django.test import Client
from ..views import *
from .test_entities import AbstractTestEntities

"""
https://docs.djangoproject.com/en/2.1/topics/testing/tools/ - how to create tests
It tests all functions in entities\views.py
"""


class TestViews(AbstractTestEntities):
    
    def test_create_table(self):
        dict_example = create_table_example()
        value = None
        if dict_example["values"]:
            value = "List is not empty"
        self.assertIsNone(value)

    def test_create_table_example(self):
        plans = get_plans()
        self.assertIsNotNone(plans[0])

    def test_create_table_for_room(self):
        plan = Plan.objects.all()[0]
        values, plan_name_db = create_table(plan.id)
        self.assertNotEqual( [], values["values"] )
        self.assertEqual("CS1_01", plan_name_db, "This is not plan we are looking for")

    def test_create_table_for_teacher(self):
        teacher = Teacher.objects.all()[0]
        values, plan_title = create_table_for_teacher(teacher.user.id)
        self.assertNotEqual( [], values["values"] )
        self.assertEqual(teacher.user.name + " " + teacher.user.surname, plan_title)

    def test_show_choose_plan(self):
        self.client.login(username="student_1", password="password123")
        response = self.client.get('/entities/studentplan/')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)
        self.client.logout()

    def test_show_edit_timetable_as_student(self):
        self.client.login(username="student_1", password="password123")
        response = self.client.get('/entities/edittimetables/')
        self.assertEqual(response.status_code, AbstractTestEntities.status_forbidden)
        self.client.logout()

    def test_show_edit_timetable_as_admin(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get('/entities/edittimetables')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)
        self.client.logout()

    def test_show_forbidden(self):
        response = self.client.get('/entities/forbidden/')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)

    def test_show_generate_page(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get('/entities/generate/')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)
        self.client.logout()

    def test_show_rooms_plans(self):
        response = self.client.get('/entities/timetables/room')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)

    def test_show_student_plan(self):
        self.client.login(username="student_1", password="password123")
        response = self.client.get('/entities/studentplan/')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)
        self.client.logout()

    def test_show_student_plans(self):
        response = self.client.get('/entities/timetables/student')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)

    def test_show_teacher_plan(self):
        self.client.login(username="teacher_x", password="teacher_user",)
        response = self.client.get('/entities/teacherplan/')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)
        self.client.logout()

    def test_show_teacher_plans(self):
        response = self.client.get('/entities/timetables/teacher')
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)

    # TESTS FOR SHOW_PLANS: POST REQUESTS
    def test_show_student_plans_get_plan(self):
        plan = Plan.objects.get(title="CS1_01")
        response = self.client.post('/entities/timetables/student', {"plan_id": plan.id})
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)

    def test_show_teacher_plans_get_plan(self):
        teacher = Teacher.objects.get(user__username="teacher_x")
        response = self.client.post('/entities/timetables/teacher', {"plan_id": teacher.user.id})
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)

    def test_show_room_plans_get_plan(self):
        room = Room.objects.get(id="r001")
        response = self.client.post('/entities/timetables/room', {"plan_id": room.id})
        self.assertEqual(response.status_code, AbstractTestEntities.status_ok)
