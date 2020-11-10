from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from entities.models import Student
from multiprocessing import Lock
from .security import *
from .utilities import *


main_lock = Lock()

""" ::: VIEWS FOR ADMINS ::: """

# TODO: split shows to files -> in views directory
def show_student_plans(request):
    plans = Plan.objects.all()
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
    teachers = Teacher.objects.all()
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
