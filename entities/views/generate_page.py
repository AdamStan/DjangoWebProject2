from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from ..models import Student
from ..improvement import make_improvement
from plans.runner import CreatePlanManager
from ..models import FieldOfStudy
from multiprocessing import Lock
from .security import *

main_lock = Lock()


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_generate_page(request, fail_message="", s_message=""):
    return render(request, 'admin/generate.html', {"fail_message": fail_message, "s_message": s_message})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def action_generate(request):
    global main_lock
    main_lock.acquire()
    fail_message = ""
    s_message = ""
    try:
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
                cpm.create_plan_asynch(winterOrSummer=FieldOfStudy.SUMMER, how_many_plans=int(how_many_groups),
                                       min_hour=int(min_hour), max_hour=int(max_hour))
                cpm.save_the_best_result()
            else:
                # create_plans_without_delete
                cpm.create_plan_asynch_without_deleting(min_hour=int(min_hour), max_hour=int(max_hour))
                cpm.save_the_best_result()

            if not cpm.the_best_result:
                fail_message = "Something went wrong, please try again"
            else:
                s_message = "Everything went well, check plans in AllPlans tab"
        return show_generate_page(request, fail_message, s_message)
    finally:
        main_lock.release()


@user_passes_test(test_user_is_admin, login_url=forbidden)
def action_improve(request):
    global main_lock
    main_lock.acquire()

    number_of_generations = request.POST.get('number_of_generation')
    make_improvement(int(number_of_generations))
    s_message = "Algorithm made improvement to the plans"

    main_lock.release()

    return show_generate_page(request, s_message=s_message)


@user_passes_test(test_user_is_admin, login_url=forbidden)
def action_new_semester(request):
    global main_lock
    main_lock.acquire()

    students = Student.objects.all()
    for student in students:
        if student.semester == student.fieldOfStudy.howManySemesters and not student.isFinished:
            student.isFinished = True
        elif student.semester < student.fieldOfStudy.howManySemesters:
            student.semester += 1
        student.save()
    s_message = "New semester has been started"

    main_lock.release()
    return show_generate_page(request, s_message=s_message)