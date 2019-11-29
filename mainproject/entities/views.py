from datetime import time, datetime
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import Student, Teacher, Plan, ScheduledSubject, Room
from .algorithm import ImprovementHelper
from .improvement import make_improvement
from django.http import HttpResponse
import json
from plans.runner import CreatePlanManager
from .models import FieldOfStudy
from multiprocessing import Lock

forbidden = "/entities/forbidden/"
main_lock = Lock()


class SubjectExample:
    id = 0
    name = ""
    whenStart = 0
    how_long = 0
    day = "monday"
    def toJSON(self):
        return json.dumps(self.__dict__)


class TeacherBox:
    id = 0
    title = ""

""" --- TESTS FOR USER --- """
def test_user_is_student(user):
    return user.student


def test_user_is_teacher(user):
    return user.teacher


def test_user_is_admin(user):
    return user.admin


def create_table_example():
    values = []
    return {'values': values}

def get_plans():
    plans = Plan.objects.all()
    return plans

def create_table(plan_id):
    plan = Plan.objects.get(id=plan_id)
    subjects = ScheduledSubject.objects.filter(plan=plan).order_by('dayOfWeek')
    values = []
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday",]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        teacher_name = ""
        if ss.teacher:
            teacher_name = ss.teacher.user.name + " " + ss.teacher.user.surname
        buff.name = ss.subject.name + " " + ss.type + " " + teacher_name
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())

    return {"values": values}, plan.title


def get_teachers():
    teacher = Teacher.objects.all()
    return teacher


def create_table_for_teacher(teacher_id):
    teacher = Teacher.objects.get(user_id=teacher_id)
    subjects = ScheduledSubject.objects.filter(teacher=teacher).order_by('dayOfWeek')
    values = []
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", ]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        buff.name = ss.subject.name + " " + ss.type + " " + ss.plan.title
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())
    plan_title = teacher.user.name + " " + teacher.user.surname
    return {"values": values}, plan_title


def get_plans_for_rooms():
    rooms = Room.objects.all()
    return rooms


def create_table_for_room(room_id):
    room = Room.objects.get(id=room_id)
    subjects = ScheduledSubject.objects.filter(room=room).order_by('dayOfWeek')
    values = []
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", ]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        teacher_name = ss.teacher.user.name + " " + ss.teacher.user.surname
        buff.name = ss.subject.name + " " + ss.type + " " + ss.plan.title + " " + teacher_name
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())

    return {"values": values}, room.id

""" ::: VIEWS FOR ADMINS ::: """


def show_student_plans(request):
    plans = get_plans()
    plan_title = ""
    message = None
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        try:
            parameters, plan_title = create_table(value)
        except:
            parameters = create_table_example()
            message = "Timetables are not correctly initialized"
    else:
        parameters = create_table_example()

    return render(request, 'admin/timetables.html', {"values": parameters['values'], "plans": plans,
                                                     "plan_title": plan_title, "type": "student", "message": message})


def show_teachers_plans(request):
    teachers = get_teachers()
    plan_title = "Example"
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        parameters, plan_title = create_table_for_teacher(value)
    else:
        parameters = create_table_example()

    teachers_boxes = []
    for t in teachers:
        teachers_boxes.append(TeacherBox())
        teachers_boxes[-1].id = t.user.id
        teachers_boxes[-1].title = t.user.surname + ", " + t.user.name
    return render(request, 'admin/timetables.html', {"values": parameters['values'], "plans": teachers_boxes , "plan_title":plan_title, "type": "teacher"})


def show_rooms_plans(request):
    plans = get_plans_for_rooms()
    plan_title = "Example"
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        parameters, plan_title = create_table_for_room(value)
    else:
        parameters = create_table_example()
    return render(request, 'admin/timetables.html',{"values": parameters['values'], "plans": plans, "plan_title": plan_title, "type":"room"})


def show_forbidden(request):
    return render(request, 'forbidden.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_generate_page(request):
    main_lock.acquire()
    fail_message = ""
    s_message = ""
    try:
        if request.method == 'POST':
            if request.POST.get('action') == "generate":
                min_hour = request.POST.get("first_hour")
                max_hour = request.POST.get("last_hour")
                semester_type = request.POST.get("semester_type")
                how_many_groups = request.POST.get("how_many_groups")
                delete_on = request.POST.get('if_delete')
                if max_hour == "" or min_hour == "" or semester_type == "None" or how_many_groups == "":
                    fail_message = "Plans cannot be create with this values "
                else:
                    print(delete_on)
                    # try:
                    cpm = CreatePlanManager()
                    if delete_on:
                        cpm.create_plan_asynch(winterOrSummer=FieldOfStudy.SUMMER, how_many_plans=int(how_many_groups), min_hour=int(min_hour), max_hour=int(max_hour))
                        cpm.save_the_best_result()
                    else:
                        # create_plans_without_delete
                        cpm.create_plan_asynch_without_deleting(min_hour=int(min_hour), max_hour=int(max_hour))
                        cpm.save_the_best_result()

                    if not cpm.the_best_result:
                        fail_message = "Something went wrong, please try again"
                    else:
                        s_message = "Everything went well, check plans in AllPlans tab"

            elif request.POST.get('action') == "improve":
                number_of_generations = request.POST.get('number_of_generation')
                make_improvement(int(number_of_generations))
                s_message = "Algorithm made improvement to the plans"
            elif request.POST.get('action') == "add_new_semestr":
                students = Student.objects.all()
                for student in students:
                    if student.semester == student.fieldOfStudy.howManySemesters and not student.isFinished:
                        student.isFinished = True
                    elif student.semester < student.fieldOfStudy.howManySemesters:
                        student.semester += 1
                    student.save()
                s_message = "New semester has been started"
        return render(request, 'admin/generate.html', {"fail_message": fail_message, "s_message": s_message})
    finally:
        main_lock.release()

@user_passes_test(test_user_is_admin, login_url="/entities/forbidden/")
def show_edit_timetable(request):
    plans = get_plans()
    plan_title = ""
    value = 0
    message = None
    s_message = None
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'search':
            value = request.POST.get('plan_id', None)
            print("Which value was taken: " + value)
            try:
                parameters, plan_title = create_table(value)
            except:
                parameters = create_table_example()
                message = "Subjects in plans are not scheduled!"

        elif action == "delete":
            print("delete")
            sch_subject_id = request.POST.get('event_id')
            sch_subject = ScheduledSubject.objects.filter(id=sch_subject_id)[0]
            print(sch_subject)
            value = sch_subject.plan.id
            sch_subject.delete()
            parameters, plan_title = create_table(value)
        elif action == "Update":
            room_id = request.POST.get('room_id')
            teacher_id = request.POST.get('teacher_id')
            object_id = request.POST.get('object_id')
            new_room = Room.objects.get(id=room_id)
            new_teacher = Teacher.objects.get(user_id=teacher_id)
            sch_subject = ScheduledSubject.objects.get(id=object_id)
            subjects = ScheduledSubject.objects.filter(plan=sch_subject.plan)
            sch_subject.room = new_room
            sch_subject.teacher = new_teacher
            if sch_subject.type == "LEC":
                sch_subjects_to_edit = ScheduledSubject.objects.filter(subject=sch_subject.subject, type="LEC")
                case1 = True
                # check all in there plans
                for ss in sch_subjects_to_edit:
                    subjects = ScheduledSubject.objects.filter(plan=ss.plan)
                    case1 = case1 and ImprovementHelper.check_subject_to_subject_time_exclude(ss, subjects)
                # check teacher can teach and exclude other lectures
                case2 = ImprovementHelper.check_teacher_can_teach_exclude_lectures(sch_subjects_to_edit,
                                                                                   teacher=sch_subject.teacher)
                case3 = ImprovementHelper.check_room_is_not_taken_exclude_lectures(sch_subjects_to_edit,
                                                                                   room=sch_subject.room)
                if case1 and case2 and case3:
                    for ss in sch_subjects_to_edit:
                        ss.save()
            elif sch_subject.type == "LAB":
                case1 = ImprovementHelper.check_subject_to_subject_time_exclude(sch_subject, subjects)
                case2 = ImprovementHelper.check_teacher_can_teach_exclude(sch_subject, teacher=sch_subject.teacher)
                case3 = ImprovementHelper.check_room_is_not_taken_exclude(sch_subject, room=sch_subject.room)
                if case1 and case2 and case3:
                    sch_subject.save()
            parameters, plan_title = create_table(sch_subject.plan.id)
            s_message = "Class was successfully updated"
        else:
            event_id=request.POST.get('event_d[event][id]',False)
            start_hour=request.POST.get('event_d[event][start]', False)
            end_hour=request.POST.get('event_d[event][end]', False)
            print("Dane z ajaxa: " + event_id + ' ' + start_hour + ' ' + end_hour )
            day_of_week = datetime(int(end_hour[0:4]), int(end_hour[5:7]), int(end_hour[8:10]))
            start_hour = time(int(start_hour[11:13]), 0, 0)
            end_hour = time(int(end_hour[11:13]), 0, 0)
            subject_to_edit = ScheduledSubject.objects.get(id=int(event_id))
            if subject_to_edit.type == "LAB":
                subjects = ScheduledSubject.objects.filter(plan=subject_to_edit.plan)
                subject_to_edit.whenStart = start_hour
                subject_to_edit.whenFinnish = end_hour
                subject_to_edit.dayOfWeek = day_of_week.weekday() + 1
                case1 = ImprovementHelper.check_subject_to_subject_time_exclude(subject_to_edit, subjects)
                case2 = ImprovementHelper.check_teacher_can_teach_exclude(subject_to_edit, teacher=subject_to_edit.teacher)
                case3 = ImprovementHelper.check_room_is_not_taken_exclude(subject_to_edit, room=subject_to_edit.room)
                if case1 and case2 and case3:
                    subject_to_edit.save()
                    return HttpResponse('')
                else:
                    raise Exception("I cannot set this subject to database, conflict with other plan")
            elif subject_to_edit.type == "LEC":
                diff_lectures = ScheduledSubject.objects.filter(subject=subject_to_edit.subject, type=subject_to_edit.type)
                case1 = True
                for sch_subject in diff_lectures:
                    subjects = ScheduledSubject.objects.filter(plan=sch_subject.plan)
                    sch_subject.whenStart = start_hour
                    sch_subject.whenFinnish = end_hour
                    sch_subject.dayOfWeek = day_of_week.weekday() + 1
                    case1 = case1 and ImprovementHelper.check_subject_to_subject_time_exclude(sch_subject, subjects)

                case2 = ImprovementHelper.check_teacher_can_teach_exclude_lectures(diff_lectures, teacher=sch_subject.teacher)
                case3 = ImprovementHelper.check_room_is_not_taken_exclude_lectures(diff_lectures, room=sch_subject.room)

                if case1 and case2 and case3:
                    for sch_subject in diff_lectures:
                        sch_subject.save()
                    return HttpResponse('')
                else:
                    print(str(case1) + " " + str(case2) + " " + str(case3))
                    raise Exception("I cannot set this subject to database, conflict with other plans")
    else:
        parameters = { "values": [] }
    return render(request, 'admin/edit_timetables.html',{"values": parameters['values'], "actual_plan":value,
                                                         "plans": plans, "plan_title":plan_title, "message": message, "s_message": s_message})

""" ::: VIEWS FOR STUDENT AND TEACHER ONLY ::: """


@user_passes_test(test_user_is_teacher, login_url=forbidden)
def show_teacher_plan(request):
    user_id = request.user.id
    parameters, plan_title = create_table_for_teacher(user_id) # add user_id
    return render(request, 'teacher/myplan.html', { "values": parameters['values'], "plan_title": plan_title })


@user_passes_test(test_user_is_student, login_url=forbidden)
def show_student_plan(request):
    try:
        student_id = request.user.id
        student = Student.objects.get(user_id=student_id)
        if student.plan is None:
            return render(request, 'error_page.html', {"message": "You didn't choose plan, yet"})
        parameters, plan_title = create_table(student.plan.id)
        return render(request, 'teacher/myplan.html', { "values": parameters['values'], "plan_title": plan_title })
    except Exception:
        return render(request, 'error_page.html', {
            "message": "Your student account doesn't exists, contact with administrator"})

@user_passes_test(test_user_is_student, login_url=forbidden)
def show_choose_plan(request):
    student_id = request.user.id
    student = Student.objects.get(user_id=student_id) # add student id
    plans = Plan.objects.filter(fieldOfStudy = student.fieldOfStudy, semester = student.semester)
    #temp_field = FieldOfStudy.objects.get(id=7)
    #plans = Plan.objects.filter(fieldOfStudy=temp_field, semester=1)
    plan_id = plans.first().id
    parameters, plan_title = create_table(plans.first().id)

    message = ""
    if request.POST:
        action = request.POST.get('action_name', None)
        print(action)
        if action == "search":
            plan_id = request.POST.get('plan_id', None)
            print("show plan " + str(plan_id))
            parameters, plan_title = create_table(plan_id)
        elif action == "add":
            plan_id = request.POST.get('which_plan', None)
            print("add student")
            parameters, plan_title = create_table(plan_id)
            student_buff = Student.objects.get(user_id=student_id)
            student_buff.plan = plans.get(id=plan_id)
            student_buff.save()
            message = "You were added to this plan"
        elif action == "delete":
            print("delete student")
            student_buff = Student.objects.get(user_id=student_id)
            student_buff.plan = None
            student_buff.save()
            message = "You were deleted from your plan, now you don't have a group"

    print(parameters)
    return render(request, 'student/myplans.html',
                  {"values": parameters['values'], "plans": plans, "plan_title": plan_title, "which_plan": plan_id, "message": message})
