from .models import ScheduledSubject, Plan, FieldOfStudy, Subject, Room, Teacher, Student
from random import randint, choice
from datetime import time
from django.db import transaction
'''
3 functions:
check it can be with other subjects in plans 
check it can be with other teacher's subjects
check it can be with other room's subjects
'''


class ImprovementHelper():
    bachelor_semesters = [1, 2, 3, 4, 5, 6, 7]
    master_semesters = [1, 2, 3]
    only_master_semesters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    @staticmethod
    def check_subject_to_subject_time(sch_sub, scheduled_subjects):
        """
        Checks that subjects can start and finish on generated hour
        :param sch_sub:
        :param scheduled_subjects:
        :return: None
        """
        scheduled_subjects_in_plan = scheduled_subjects.filter(plan=sch_sub.plan)
        for scheduled in scheduled_subjects_in_plan:
            if scheduled.dayOfWeek == sch_sub.dayOfWeek and scheduled.whenStart != None:
                difference_between_starts = abs(sch_sub.whenStart.hour - scheduled.whenStart.hour)
                difference_between_ends = abs(sch_sub.whenFinnish.hour - scheduled.whenFinnish.hour)
                if difference_between_starts + difference_between_ends >= sch_sub.how_long + scheduled.how_long:
                    continue
                else:
                    return False
            else:
                continue
        return True

    @staticmethod
    def check_subject_to_subject_time_exclude(sch_sub, scheduled_subjects):
        scheduled_subjects_in_plan = scheduled_subjects.filter(plan=sch_sub.plan).exclude(id=sch_sub.id)
        return ImprovementHelper.check_subject_to_subject_time(sch_sub, scheduled_subjects_in_plan)

    @staticmethod
    def check_teacher_can_teach_exclude_lectures(lecture, teacher):
        subjects_in_plan = ScheduledSubject.objects.all().filter(teacher=teacher)\
            .exclude(subject__name=lecture[0].subject.name, type=lecture[0].type)
        for scheduled in subjects_in_plan:
            if scheduled.dayOfWeek == lecture[0].dayOfWeek:
                difference_between_starts = abs(lecture[0].whenStart.hour - scheduled.whenStart.hour)
                difference_between_ends = abs(lecture[0].whenFinnish.hour - scheduled.whenFinnish.hour)
                if (difference_between_starts + difference_between_ends) >= (
                        lecture[0].how_long + scheduled.how_long):
                    continue
                else:
                    return False
            else:
                continue
        return True

    @staticmethod
    def check_room_is_not_taken_exclude_lectures(lecture, room):
        subjects_in_this_room = ScheduledSubject.objects.all().filter(room=room)\
            .exclude(subject__name=lecture[0].subject.name, type=lecture[0].type)
        for s in subjects_in_this_room:
            if s.dayOfWeek == lecture[0].dayOfWeek and lecture[0].whenStart:
                difference_between_starts = abs(lecture[0].whenStart.hour - s.whenStart.hour)
                difference_between_ends = abs(lecture[0].whenFinnish.hour - s.whenFinnish.hour)
                if (difference_between_starts + difference_between_ends) >= (lecture[0].how_long + s.how_long):
                    continue
                else:
                    return False
            else:
                continue
        return True

    @staticmethod
    def search_first_not_null_hour(lectures_list):
        i = 0
        for sub in lectures_list:
            if sub.whenStart:
                return i
            i += 1
        return None

    @staticmethod
    def search_first_not_null_room(lectures_list):
        i = 0
        for sub in lectures_list:
            if sub.room:
                return i
            i += 1
        return None

    @staticmethod
    def check_teacher_can_teach(scheduled_subject, teacher):
        subjects_in_plan = ScheduledSubject.objects.all().filter(teacher=teacher)
        for scheduled in subjects_in_plan:
            if scheduled.dayOfWeek == scheduled_subject.dayOfWeek:
                difference_between_starts = abs(scheduled_subject.whenStart.hour - scheduled.whenStart.hour)
                difference_between_ends = abs(scheduled_subject.whenFinnish.hour - scheduled.whenFinnish.hour)
                if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + scheduled.how_long):
                    continue
                else:
                    return False
            else:
                continue
        return True

    @staticmethod
    def check_teacher_can_teach_exclude(scheduled_subject, teacher):
        subjects_in_plan = ScheduledSubject.objects.all().filter(teacher=teacher).exclude(id=scheduled_subject.id)
        for scheduled in subjects_in_plan:
            if scheduled.dayOfWeek == scheduled_subject.dayOfWeek:
                difference_between_starts = abs(scheduled_subject.whenStart.hour - scheduled.whenStart.hour)
                difference_between_ends = abs(scheduled_subject.whenFinnish.hour - scheduled.whenFinnish.hour)
                if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + scheduled.how_long):
                    continue
                else:
                    return False
            else:
                continue
        return True

    @staticmethod
    def check_room_is_not_taken(scheduled_subject, room):
        subjects_in_this_room = ScheduledSubject.objects.all().filter(room=room)
        for s in subjects_in_this_room:
            if s.dayOfWeek == scheduled_subject.dayOfWeek and scheduled_subject.whenStart != None:
                difference_between_starts = abs(scheduled_subject.whenStart.hour - s.whenStart.hour)
                difference_between_ends = abs(scheduled_subject.whenFinnish.hour - s.whenFinnish.hour)
                if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + s.how_long):
                    continue
                else:
                    return False
            else:
                continue
        return True

    @staticmethod
    def check_room_is_not_taken_exclude(scheduled_subject, room):
        subjects_in_this_room = ScheduledSubject.objects.all().filter(room=room).exclude(id=scheduled_subject.id)
        for s in subjects_in_this_room:
            if s.dayOfWeek == scheduled_subject.dayOfWeek and scheduled_subject.whenStart != None:
                difference_between_starts = abs(scheduled_subject.whenStart.hour - s.whenStart.hour)
                difference_between_ends = abs(scheduled_subject.whenFinnish.hour - s.whenFinnish.hour)
                if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + s.how_long):
                    continue
                else:
                    return False
            else:
                continue
        return True

    @transaction.atomic
    def create_plans(self, number_of_groups=3, semester=1, min_hour=8, max_hour=19):
        sid = transaction.savepoint()
        # in this moment we have to create plans
        try:
            self.create_skeleton(number_of_group=number_of_groups, semester=semester)
            self.create_first_plan(min_hour=min_hour, max_hour=max_hour)

            transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            print(str(e))
            raise e


    @transaction.atomic
    def create_plans_without_delete(self, number_of_groups=3, semester=1, min_hour=8, max_hour=19):
        sid = transaction.savepoint()
        # in this moment we have to create plans
        try:
            ImprovementHelper.clean_hours_and_teacher()
            self.create_first_plan(min_hour=min_hour, max_hour=max_hour)

            transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            print(str(e))
            raise e

    @staticmethod
    def clean_hours_and_teacher():
        for ss in ScheduledSubject.objects.all():
            ss.dayOfWeek = None
            ss.whenStart = None
            ss.whenFinnish = None
            ss.teacher = None
            ss.room = None
            ss.save()

    @staticmethod
    def show_scheduled_subjects(scheduled_subjects):
        for ss in scheduled_subjects:
            print(ss.subject.name + " " + str(ss.whenStart) + " " + str(ss.dayOfWeek) + " " + ss.plan.title +
                  "p_id_" + str(ss.plan.id) + " " + str(ss.teacher) + " " + str(ss.room))

