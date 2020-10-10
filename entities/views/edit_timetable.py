from datetime import time, datetime
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from ..models import Student, Teacher, Plan, ScheduledSubject, Room
from ..algorithm import ImprovementHelper
from django.http import HttpResponse
from .security import *
from .utilities import *


@user_passes_test(test_user_is_admin, login_url="/entities/forbidden/")
def show_edit_timetable(request):
    plans = Plan.objects.all()
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