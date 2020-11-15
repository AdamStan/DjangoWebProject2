from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from plans.report_generator import BasicAlgorithmReport
from plans.runner import provide_creator
from ..models import FieldOfStudy, Student
from multiprocessing import Lock
from .security import *
from plans import AllParameters

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
        # basic parameters
        min_hour = request.POST.get("first_hour")
        max_hour = request.POST.get("last_hour")
        semester_type = request.POST.get("semester_type")
        how_many_groups = request.POST.get("how_many_groups")
        delete_on = request.POST.get('if_delete')
        algorithm_name = request.POST.get("algorithm")

        number_of_generation = request.POST.get('number_of_generation')
        number_of_crossover = request.POST.get('number_of_crossover')
        number_of_mutation = request.POST.get('number_of_mutation')

        if max_hour == "" or min_hour == "" or semester_type == "None" or how_many_groups == "" or algorithm_name == "":
            fail_message = "Plans cannot be create with this values "
        else:
            print(delete_on)
            print(algorithm_name)
            parameters = AllParameters(number_of_generation=int(number_of_generation),
                                       number_of_mutation=float(number_of_mutation),
                                       number_of_crossover=float(number_of_crossover))
            plan_creator = provide_creator(algorithm_name=algorithm_name, plan_parameters=parameters)
            print(plan_creator)
            if delete_on:
                plan_creator.create_plan_async(winter_or_summer=FieldOfStudy.SUMMER,
                                               how_many_plans=int(how_many_groups),
                                               min_hour=int(min_hour), max_hour=int(max_hour))
            else:
                plan_creator.create_plan_async_without_deleting(min_hour=int(min_hour), max_hour=int(max_hour))

            if not plan_creator.the_best_result:
                fail_message = "Something went wrong, please try again"
            else:
                s_message = "Everything went well, check plans in AllPlans tab"
            other_info = {"fail_message": fail_message, "success_message": s_message}
            # TODO: time!!!
            report_creator = BasicAlgorithmReport(time=100, result_value=plan_creator.the_best_result[1],
                                                  quality_function_name=plan_creator.__class__.__name__,
                                                  other_info_dict=other_info)
            report_creator.create_report()
        return show_generate_page(request, fail_message, s_message)
    finally:
        main_lock.release()


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
