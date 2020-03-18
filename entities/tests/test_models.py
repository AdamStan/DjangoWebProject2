from django.test import TestCase
from datetime import time
from ..models import Faculty, FieldOfStudy, Subject, Building, Room, Plan, ScheduledSubject

"""
We use to check equality function compare to!
"""
class CheckModelsEquals(TestCase):

    def setUp(self):
        self.faculty = Faculty(name="WEEIA")
        self.field_of_study = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                           degree=FieldOfStudy.BACHELOR, howManySemesters=2,
                                           whenDoesItStarts=FieldOfStudy.WINTER)

    def test_check_faculty_are_not_equal(self):
        faculty1 = Faculty(name="WEEIA", description="Wydzial elektroniki, elektrotechniki, informaytki itd")
        faculty2 = Faculty(name="WM", description="Wydzial mechaniczny")
        self.assertFalse(faculty1.compare_to(faculty2), msg="Faculties should not be equal")

    def test_check_faculty_are_equal(self):
        faculty1 = Faculty(name="WEEIA")
        faculty2 = Faculty(name="WEEIA")
        self.assertTrue(faculty1.compare_to(faculty2),
                        msg="There are the same faculties, but compare_to returns false")

    def test_check_fieldsOfStudy_are_equal(self):
        field_of_study1 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=7,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        field_of_study2 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=7,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        self.assertTrue(field_of_study1.compare_to(field_of_study2),
                        msg="Fields are the same, but comapre_to() returns false")

    def test_check_fieldsOfStudy_are_not_equal(self):
        field_of_study1 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=2,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        field_of_study2 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=7,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        self.assertFalse(field_of_study1.compare_to(field_of_study2), msg="Fields are equal")

    def test_check_subjects_are_equal(self):
        subject1 = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        subject2 = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        self.assertTrue(subject1.compare_to(subject2), msg="Subjects are not equal!")

    def test_check_subjects_are_not_equal(self):
        subject1 = Subject(name="SubjectName123", fieldOfStudy=self.field_of_study, semester=6)
        subject2 = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        self.assertFalse(subject1.compare_to(subject2), msg="Subjects are equal!")

    def test_check_buildings_are_equal(self):
        building1 = Building(name="name",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        building2 = Building(name="name",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        self.assertTrue(building1.compare_to(building2), msg="Buildings are not equal!")

    def test_check_building_are_not_equal(self):
        building1 = Building(name="name1",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        building2 = Building(name="name2",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        self.assertFalse(building1.compare_to(building2), msg="Buildings are equal!")

    def test_check_rooms_are_equal(self):
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room1 = Room(id="b10_12",building=building,room_type=Room.LECTURE)
        room2 = Room(id="b10_12",building=building,room_type=Room.LECTURE)
        self.assertEqual(room1, room2, "Rooms are not equal!")

    def test_rooms_are_not_equal(self):
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room1 = Room(id="b10_12", building=building, room_type=Room.LECTURE)
        room2 = Room(id="b10_13", building=building, room_type=Room.LECTURE)
        self.assertNotEqual(room1, room2, "Rooms are equal!")

    def test_plans_are_equal(self):
        plan1 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        plan2 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        self.assertTrue(plan1.compare_to(plan2), msg="Plans are not equal!")

    def test_plans_are_not_equal(self):
        plan1 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        plan2 = Plan(title="CS2_02", fieldOfStudy=self.field_of_study, semester=2)
        self.assertFalse(plan1.compare_to(plan2), msg="Plans are equal!")

    def test_scheduled_subject_are_equal(self):
        subject = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        plan = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room = Room(id="b10_12", building=building, room_type=Room.LECTURE)
        event1 = ScheduledSubject(subject=subject, plan=plan, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        event2 = ScheduledSubject(subject=subject, plan=plan, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        self.assertTrue(event1.compare_to(event2), msg="Scheduled Subjects are not equal!")

    def test_scheduled_subject_are_not_equal(self):
        subject = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        plan1 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        plan2 = Plan(title="CS2_02", fieldOfStudy=self.field_of_study, semester=2)
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room = Room(id="b10_12", building=building, room_type=Room.LECTURE)
        event1 = ScheduledSubject(subject=subject, plan=plan1, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        event2 = ScheduledSubject(subject=subject, plan=plan2, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        self.assertFalse(event1.compare_to(event2), msg="Scheduled Subjects are equal!")

