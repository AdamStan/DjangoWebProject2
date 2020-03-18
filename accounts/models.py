from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import datetime
# Create your models here.
from django.contrib.auth.models import User
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, active=True, is_student=False, is_teacher=False, is_admin=False, name=None, surname=None, sname = None):
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have password")
        user_instance = User()
        user_instance.username = username
        user_instance.set_password(password)
        user_instance.is_active = active
        user_instance.student = is_student
        user_instance.teacher = is_teacher
        user_instance.admin = is_admin
        if is_admin:
            user_instance.staff = True
        user_instance.name = name
        user_instance.second_name = sname
        user_instance.surname = surname
        user_instance.save()
        return user_instance

    def create_student(self, username, password=None, active=True, name=None, sname=None, surname=None):
        user_instance = self.create_user(
            username= username,
            password= password,
            active = active,
            is_student = True,
            name = name,
            sname= sname,
            surname = surname,
        )
        return user_instance

    def create_teacher(self, username, password=None, active=True, name=None, sname=None, surname=None):
        user_instance = self.create_user(
            username=username,
            password=password,
            active=active,
            is_teacher=True,
            name=name,
            sname= sname,
            surname=surname
        )
        return user_instance

    def create_superuser(self, username, password=None, active=True, name=None, snmae=None, surname=None):
        user_instance = self.create_user(
            username=username,
            password=password,
            active=active,
            is_admin=True,
            name=name,
            sname=snmae,
            surname=surname
        )
        return user_instance

class User(AbstractBaseUser):
    username = models.CharField(max_length=64, unique=True, default='USER_WITH_NONAME')
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=32, default=None)
    second_name = models.CharField(max_length=32, default=None, null=True)
    surname = models.CharField(max_length=64, default=None)
    whenCreated = models.DateField(default=datetime.date.today)
    #types of users:
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =  ['name', 'surname']

    def __str__(self):
        return self.name + ', ' + self.surname

    def get_full_name(self):
        return

    def get_short_name(self):
        return

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_student(self):
        return self.student

    @property
    def is_teacher(self):
        return self.teacher

    @property
    def is_admin(self):
        return self.admin