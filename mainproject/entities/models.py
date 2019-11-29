from django.db import models
from django.db.models import Max
import json
from accounts.models import User # it works, really

var_on_delete = models.SET_NULL = True


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default=None, null=True)

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.name

    def compare_to(self, other):
        return self.name == other.name and \
               self.description == other.description


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=64)
    faculty = models.ForeignKey(Faculty, on_delete=var_on_delete, default=None)
    BACHELOR = '1st'
    MASTER = '2nd'
    UNIFORM_MASTER_DEGREE = 'only-master'
    DEGREE_CHOICES = (
        (BACHELOR, 'bachelor'),
        (MASTER, 'master'),
        (UNIFORM_MASTER_DEGREE, 'only-master')
    )
    degree = models.CharField(max_length=12, choices=DEGREE_CHOICES, default=BACHELOR)
    howManySemesters = models.IntegerField(default=0)
    type = models.CharField(max_length=32, default='full-time')
    WINTER = "W"
    SUMMER = "S"
    SEMESTER_TYPES = {
        (WINTER, 'winter'),
        (SUMMER, 'summer')
    }
    whenDoesItStarts = models.CharField(
        max_length=1,
        choices=SEMESTER_TYPES,
        default=WINTER
    )

    # def compare_to(self, other):
    #     return self.name == other.name and \
    #            self.faculty == other.faculty and \
    #            self.degree == other.degree and \
    #            self.type == other.type and \
    #            self.howManySemesters == other.howManySemesters and \
    #            self.whenDoesItStarts == other.whenDoesItStarts
    #
    # def __hash__(self):
    #     return hash(self.name) + hash(self.faculty) + hash(self.degree) + hash(self.type) \
    #            + hash(self.howManySemesters) + hash(self.whenDoesItStarts)

    def compare_to(self, other):
        return self.name == other.name and \
               self.faculty.compare_to(other.faculty) and \
               self.degree == other.degree and \
               self.type == other.type and \
               self.howManySemesters == other.howManySemesters and \
               self.whenDoesItStarts == other.whenDoesItStarts

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.name + ", " + str(self.faculty) + ", " + self.degree


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='professor_to_user')
    faculty = models.ForeignKey(Faculty, on_delete=var_on_delete)

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.user.name + ', ' + self.user.surname


class Subject(models.Model):
    name = models.CharField(max_length=128)
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete, default=None)
    semester = models.IntegerField(default=None)
    teachers = models.ManyToManyField(Teacher)
    lecture_hours = models.IntegerField(default=None, null=True)
    laboratory_hours = models.IntegerField(default=None, null=True)

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.name + ", " + self.fieldOfStudy.name

    def compare_to(self, other):
        return self.name == other.name and \
               self.fieldOfStudy.compare_to(other.fieldOfStudy) and \
               self.semester == other.semester


class Building(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    numberOfBuilding = models.CharField(max_length=8)
    postalCode = models.CharField(max_length=8)

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.name + ", " + self.street + ", " + self.city + ", " + self.numberOfBuilding + ", " + self.postalCode

    def compare_to(self, other):
        return self.name == other.name and \
               self.street == other.street and \
               self.city == other.city and \
               self.numberOfBuilding == other.numberOfBuilding and \
               self.postalCode == other.postalCode


class Room(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    building = models.ForeignKey(Building, on_delete=var_on_delete, null=True)
    LECTURE = "LEC"
    LABORATORY = "LAB"
    TYPE_OF_ROOMS = (
        (LECTURE, 'Lecture'),
        (LABORATORY, 'Laboratory'),
    )
    room_type = models.CharField(
        max_length=3,
        choices=TYPE_OF_ROOMS,
        default=None,
        null=True,
    )

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return str(self.id) + " " + str(self.room_type)

    def compare_to(self, other):
        return self.id == other.id


class Plan(models.Model):
    title = models.CharField(max_length=32)
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete, default=None)
    semester = models.IntegerField(default=1)

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.title + ", " + self.fieldOfStudy.name + ", " + str(self.semester)

    def compare_to(self, other):
        return self.title == other.title and \
               self.fieldOfStudy.compare_to(other.fieldOfStudy) and \
               self.semester == other.semester


class ScheduledSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=var_on_delete, default=None)
    LECTURE = "LEC"
    LABORATORY = "LAB"
    TYPE_CHOICES = (
        (LECTURE, 'Lecture'),
        (LABORATORY, 'Laboratory'),
    )
    type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=None,
        null=True
    )
    whenStart = models.TimeField(default=None, null=True)
    whenFinnish = models.TimeField(default=None, null=True)
    dayOfWeek = models.IntegerField(default=None, null=True)
    how_long = models.IntegerField(default=None, null=True)
    plan = models.ForeignKey(Plan, on_delete=var_on_delete, default=None)
    room = models.ForeignKey(Room, on_delete=var_on_delete, default=None, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=var_on_delete, default=None, null=True)

    def toJSON(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.plan.title + ", " + self.subject.name + ", " + self.type

    def compare_to(self, other):
        return self.subject.compare_to(other.subject) and \
               self.plan.compare_to(other.plan) and \
               self.whenStart == other.whenStart and \
               self.whenFinnish == other.whenFinnish and \
               self.dayOfWeek == other.dayOfWeek


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_to_user')
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete)
    semester = models.IntegerField(default=1)
    plan = models.ForeignKey(Plan, on_delete=var_on_delete, default=None, null=True)
    indexNumber = models.IntegerField(unique=True, default=1)
    isFinished = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name + " " + self.user.surname + ", " + str(self.indexNumber)

    def toJSON(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def add_student(student):
        max_index = Student.objects.all().aggregate(Max('indexNumber'))
        student.indexNumber = max_index
        student.save()
