from .models import *
from accounts.models import User
from django.db import transaction

@transaction.atomic
def add_entities():
    sid = transaction.savepoint()
    try:
        faculty1 = Faculty(name="EEIA")
        faculty1.save()
        teachers = User.objects.filter(teacher=True)
        teachers_list = []
        for t in teachers:
            teachers_list.append(Teacher(user=t, faculty=faculty1))
            teachers_list[-1].save()
        field_of_study1 = FieldOfStudy(name="Computer Science", degree = FieldOfStudy.BACHELOR, faculty=faculty1,
                                       howManySemesters=7, whenDoesItStarts=FieldOfStudy.WINTER)
        field_of_study2 = FieldOfStudy(name="Computer Science", degree = FieldOfStudy.MASTER, faculty=faculty1,
                                       howManySemesters=3, whenDoesItStarts=FieldOfStudy.SUMMER)
        field_of_study1.save()
        field_of_study2.save()

        subject_list = []
        # 1st semester - field_of_study1
        subject_list.append(Subject(name="Mathematics 1", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Safety at Work and Ergonomics", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Physics", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Introduction to Computer Science", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Scripting Languages", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Algorithms and Data Structures", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        # 2nd semester - field_of_study1
        subject_list.append(Subject(name="Mathematics 2", semester=2, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Programming and Data Structures", semester=2, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Electrical Circuits and Measurements", semester=2,fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Modern Physics", semester=2,fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Scripting Languages 2", semester=2,fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Java Fundamentals", semester=2,fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        # 3rd semester - field_of_study1
        subject_list.append(Subject(name="Electronics Fundamentals", semester=3, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Digital Systems", semester=3, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Object Oriented Programming in C++", semester=3, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Databases", semester=3, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Mathematics 3", semester=3, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Image Processing", semester=3, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        # 4th semester - field_of_study1
        subject_list.append(Subject(name="Numerical Methods", semester=4, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Computer Architecture", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Interactive Web Applications", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Software Engineering", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Team Project", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="GUI Programming", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        # 5th semester - field_of_study1
        subject_list.append(Subject(name="Economics", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Operating Systems", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Computer Networks", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Computer Aided Design", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Embedded Systems", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Computer Graphics", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        # 6th semester - field_of_study1
        subject_list.append(Subject(name="Operating Systems 2", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Artificial Intelligence Fundamentals", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Physics", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Introduction to Computer Science", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Computer Network Administration", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Network Programming", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        # 7th semester - field_of_study1
        subject_list.append(Subject(name="Artificial Intelligence", semester=7, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Final Project Seminar", semester=7, fieldOfStudy=field_of_study1))
        subject_list.append(Subject(name="Industrial Placement", semester=7, fieldOfStudy=field_of_study1))
        subject_list.append(Subject(name="Intellectual Property Protection", semester=7, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Health and Safety", semester=7, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
        # 1st semester - field_of_study2
        subject_list.append(Subject(name="Database Servers", semester=1, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Computing Methods and Optimization", semester=1, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Advanced Object Programming in Java",semester=1,fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Modelling and Analysis of Information Systems",semester=1, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Problem Based Workshop",semester=1,fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Database Administration",semester=1,fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        # 2nd semester - field_of_study2
        subject_list.append(Subject(name="Mathematical Linguistics", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Effective Java Programming", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Compiler Construction", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Advanced Networking Technology", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Computational Intelligence", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Economics, Management and Law", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        # 3rd semester - field_of_study2
        subject_list.append(Subject(name="Scientific Computing", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Recent Advances in Computer Science", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Final Project Seminar", semester=3, fieldOfStudy=field_of_study2))
        subject_list.append(Subject(name="Cloud Architecture and Virtualisation", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
        subject_list.append(Subject(name="Final Project", semester=3, fieldOfStudy=field_of_study2))
        subject_list.append(Subject(name="User Interface Programming", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))

        #counter = 0
        for sub in subject_list:
            sub.save()
        #    for x in range(counter, counter+2):
        #        sub.teachers.add(teachers_list[x])
        #        if x >= len(teachers_list):
        #            counter = 0

        plan_list = []
        # 1th semester
        plan_list.append(Plan(title="CS1_01", fieldOfStudy=field_of_study1, semester=1))
        plan_list.append(Plan(title="CS1_02", fieldOfStudy=field_of_study1, semester=1))
        plan_list.append(Plan(title="CS1_03", fieldOfStudy=field_of_study1, semester=1))
        # 3rd semester
        plan_list.append(Plan(title="CS3_01", fieldOfStudy=field_of_study1, semester=3))
        plan_list.append(Plan(title="CS3_02", fieldOfStudy=field_of_study1, semester=3))
        plan_list.append(Plan(title="CS3_03", fieldOfStudy=field_of_study1, semester=3))
        # 5th semester
        plan_list.append(Plan(title="CS5_01", fieldOfStudy=field_of_study1, semester=5))
        plan_list.append(Plan(title="CS5_02", fieldOfStudy=field_of_study1, semester=5))
        plan_list.append(Plan(title="CS5_03", fieldOfStudy=field_of_study1, semester=5))
        # 7th semester
        plan_list.append(Plan(title="CS7_01", fieldOfStudy=field_of_study1, semester=7))
        plan_list.append(Plan(title="CS7_02", fieldOfStudy=field_of_study1, semester=7))
        plan_list.append(Plan(title="CS7_03", fieldOfStudy=field_of_study1, semester=7))
        # 2nd semester
        plan_list.append(Plan(title="CS2_01_2", fieldOfStudy=field_of_study2, semester=2))
        plan_list.append(Plan(title="CS2_02_2", fieldOfStudy=field_of_study2, semester=2))
        plan_list.append(Plan(title="CS2_03_2", fieldOfStudy=field_of_study2, semester=2))

        for p in plan_list:
            p.save()

        scheduled_subject_list = []

        for p in plan_list:
            subjects = Subject.objects.filter(fieldOfStudy=p.fieldOfStudy, semester=p.semester)
            for sub in subjects:
                if sub.lecture_hours != None and sub.lecture_hours > 0:
                    scheduled_subject_list.append(
                        ScheduledSubject(subject=sub, plan=p, type=ScheduledSubject.LECTURE)
                    )
                if sub.laboratory_hours != None and sub.laboratory_hours > 0:
                    scheduled_subject_list.append(
                        ScheduledSubject(subject=sub, plan=p, type=ScheduledSubject.LABORATORY)
                    )

        for ss in scheduled_subject_list:
            ss.save()

        building = Building(
            name="MainBuilding",
            city="Łódź",
            street="ul. Napoleaona",
            numberOfBuilding='12a',
            postalCode='90-023',
        )
        building.save()
        room_list = []

        room_list.append(Room(id='r001', building=building, room_type=Room.LABORATORY))
        room_list.append(Room(id='r002', building=building, room_type=Room.LECTURE))
        room_list.append(Room(id='r003', building=building, room_type=Room.LABORATORY))
        room_list.append(Room(id='r004', building=building, room_type=Room.LECTURE))
        room_list.append(Room(id='r005', building=building, room_type=Room.LABORATORY))
        room_list.append(Room(id='r006', building=building, room_type=Room.LECTURE))
        room_list.append(Room(id='r007', building=building, room_type=Room.LABORATORY))
        room_list.append(Room(id='r008', building=building, room_type=Room.LECTURE))
        room_list.append(Room(id='r009', building=building, room_type=Room.LABORATORY))
        room_list.append(Room(id='r010', building=building, room_type=Room.LECTURE))
        room_list.append(Room(id='r011', building=building, room_type=Room.LABORATORY))
        room_list.append(Room(id='r012', building=building, room_type=Room.LECTURE))
        room_list.append(Room(id='r013', building=building, room_type=Room.LABORATORY))
        room_list.append(Room(id='r014', building=building, room_type=Room.LABORATORY))

        for r in room_list:
            r.save()

        transaction.savepoint_commit(sid)
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print(str(e))
    # additional add functions
    add_students()
    add_many_to_many()

@transaction.atomic
def add_students():
    sid = transaction.savepoint()
    try:
        # dangerous piece of code:
        field_of_study = FieldOfStudy.objects.all()
        field = None
        for f in field_of_study:
            field = f
            break
        students = User.objects.filter(student=True)
        student_list = []
        i = 1
        for std in students:
            student_list.append(Student(user=std, fieldOfStudy=field, semester=1, indexNumber=i))
            i += 1
            student_list[-1].save()

        transaction.savepoint_commit(sid)
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print(str(e))


def add_many_to_many(amount = 6):
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()

    teachers_list = []
    for t in teachers:
        teachers_list.append(t)

    counter = 0
    for sub in subjects:
        for x in range(counter, counter + amount):
            sub.teachers.add(teachers_list[x])
        if counter >= len(teachers_list) - amount:
            counter = 0
        else:
            counter += amount
        sub.save()


def add_more_laboratories():
    building = Building.objects.all()[0]
    room1 = Room(id='r016', building=building, room_type=Room.LABORATORY)
    room2 = Room(id='r017', building=building, room_type=Room.LABORATORY)
    room1.save()
    room2.save()