import traceback
from multiprocessing import Pool
from entities.models import Teacher, Room, FieldOfStudy, Plan, ScheduledSubject
from .algorithm import OnePlanGenerator

def run_it_in_shell():
    cpm = CreatePlanManager()
    cpm.create_plan_asynch_without_deleting()
    cpm.save_the_best_result()


class CreatePlanManager():
    def __init__(self):
        self.the_best_result = None
        self.results = []

    def create_plan(self, winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3, teachers=None, rooms=None, fields_of_study=None,
                    min_hour=8, max_hour=19):
        # teachers = Teacher.objects.all()
        # rooms = Room.objects.all()
        # fields_of_study = FieldOfStudy.objects.all()
        from django.db import connection
        connection.close()
        result = {"Exception"}
        try:
            plans = OnePlanGenerator.create_empty_plans(fields_of_study, how_many_plans, winterOrSummer)
            # OnePlanGenerator.show_objects(plans)
            # in test purpose only!!!
            first_plan = OnePlanGenerator(teachers, plans, rooms)
            result = first_plan.generate_plan(min_hour, max_hour)
        except Exception as e:
            print(e)
            import traceback
            traceback.print_tb(e.__traceback__)
        return result

    def create_plans_without_deleting_plans(self, teachers, rooms, plans, min_hour, max_hour, scheduled_subjects_list):
        result = {"Exception"}
        from django.db import connection
        connection.close()
        try:
            # OnePlanGenerator.show_objects(plans)
            # in test purpose only!!!
            first_plan = OnePlanGenerator(teachers=teachers, plans=plans, rooms=rooms, scheduled_subjects_in_plans=scheduled_subjects_list)
            result = first_plan.generate_plan(min_hour, max_hour)
        except Exception as ex:
            print(ex)
            import traceback
            traceback.print_tb(ex.__traceback__)
            print("Exception was thrown")
        return result

    def create_plan_asynch(self, winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8, max_hour=19):
        pool = Pool(processes = 4)
        list_with_arguments = []
        teachers = list(Teacher.objects.all())
        rooms = list(Room.objects.all())
        fields_of_study = list(FieldOfStudy.objects.all())
        for i in range(10):
            list_with_arguments.append((winterOrSummer, how_many_plans, teachers, rooms,
                                        fields_of_study, min_hour, max_hour))
        print("-> STARTS RUNNING ASYNCH")
        self.results = pool.starmap(self.create_plan, list_with_arguments)
        print(self.results)

    def create_plan_asynch_without_deleting(self, min_hour=8, max_hour=19):
        pool = Pool(processes=4)
        teachers = list(Teacher.objects.all())
        rooms = list(Room.objects.all())
        plans = list(Plan.objects.all())
        scheduled_subjects_list = []
        for plan in plans:
            bullshit = plan.fieldOfStudy.faculty
            scheduled_subjects = OnePlanGenerator.create_scheduled_subjects(plan, 15)
            scheduled_subjects_list.append(scheduled_subjects)
        list_with_arguments = []
        for i in range(10):
            list_with_arguments.append((teachers, rooms, plans, min_hour, max_hour, scheduled_subjects_list))
        print("-> STARTS RUNNING ASYNCH WITHOUT deleting")
        self.results = pool.starmap(self.create_plans_without_deleting_plans, list_with_arguments)
        print(self.results)

    def find_the_best_result(self):
        print("----- Show results -----")
        the_best_result = None
        for result in self.results:
            if the_best_result and len(result) == 2:
                if the_best_result[1] > result[1]:
                    the_best_result = result
            elif len(result) == 2:
                the_best_result = result
        print("The_best_result")
        print(result)
        return the_best_result

    def save_the_best_result(self):
        from django.db import connection
        connection.close()
        result_to_save = self.find_the_best_result()
        if result_to_save:
            plans = result_to_save[0].plans
            sch_subject_plans = result_to_save[0].subjects_in_plans
            ScheduledSubject.objects.all().delete()
            Plan.objects.all().delete()
            # SAVE
            for plan in plans:
                plan.save()
            for i in range(len(plans)):
                title = sch_subject_plans[i][0].plan.title
                plan = Plan.objects.get(title=title)
                for sch_subject in sch_subject_plans[i]:
                    sch_subject.plan = plan
                    sch_subject.save()
            self.the_best_result = result_to_save

