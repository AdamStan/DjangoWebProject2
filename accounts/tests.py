from django.test import TestCase
from .models import User
from .views import show_login, show_logout, show_my_profile
# Create your tests here.
# there will be creating users
class UserTest(TestCase):
    def setUp(self):
        self.username_student="student_x"
        self.username_teacher="teacher_x"
        self.username_admin="admin_x"

        User.objects.create_superuser(
            username=self.username_admin,
            password="haslo123",
            name="admin_name",
            surname="admin_surname"
        )
        User.objects.create_teacher(
            username=self.username_teacher,
            password="teacher_user",
            name="Jan",
            surname="Kowalski"
        )
        User.objects.create_student(
            username=self.username_student,
            password="student_user",
            name="Katarzyna",
            surname="Popowska"
        )

    def test_admins(self):
        admin = User.objects.get(username=self.username_admin)
        self.assertEqual(admin.username, 'admin_x')
        self.assertEqual(admin.admin, True)
        self.assertEqual(admin.staff, True)

    def test_teachers(self):
        teacher = User.objects.get(username=self.username_teacher)
        self.assertEqual(teacher.teacher, True)
        self.assertEqual(teacher.staff, False)

    def test_students(self):
        student = User.objects.get(username=self.username_student)
        self.assertEqual(student.student, True)
        self.assertEqual(student.staff, False)


class ViewsTest(TestCase):
    def test_show_my_profile(self):
        pass

    def test_show_login(self):
        pass

    def test_show_logout(self):
        pass