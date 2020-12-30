import logging
import sys

from entities.models import FieldOfStudy, Plan, Teacher, Room, ScheduledSubject
from .algorithms_helper import create_empty_plans, create_scheduled_subjects
from .state import Environment
from .value_strategies import ValueOfPlanStrategy1


class GraphAlgorithm:
    logger = logging.getLogger("GraphAlgorithm")

    def __init__(self, teachers, rooms, plans, scheduled_subjects_in_plans, min_hour=8, max_hour=19):
        """
        @param teachers: a list of teachers from queryset
        @param rooms: a list of rooms from queryset
        @param plans: a list of plans
        @param scheduled_subjects_in_plans: dictionary with plan.title as a key and list of scheduled_subjects as a
                                            value
        @param min_hour: when lesson can start
        @param max_hour: when lesson can end
        """
        self.rooms = rooms
        self.teachers = teachers
        self.plans = plans
        self.scheduled_subjects = scheduled_subjects_in_plans
        # parameters
        self.min_hour = min_hour
        self.max_hour = max_hour

    def create_plan(self):
        self.logger.log(logging.INFO, "Starting creating plan with graph algorithm")
        all_scheduled_subjects = list()
        for subjects_list in self.scheduled_subjects.values():
            all_scheduled_subjects += subjects_list
        environment_sch_subjects = Environment(self.plans, all_scheduled_subjects, ValueOfPlanStrategy1(),
                                               self.teachers, self.rooms, self.min_hour, self.max_hour)
        self.set_scheduled_subject(environment_sch_subjects)

    def set_scheduled_subject(self, environment):
        self.logger.log(logging.INFO, "Settings lessons to plans")

        for plan in self.plans:
            scheduled_subjects_in_plan = self.scheduled_subjects[plan.title]
            for sch_subject in scheduled_subjects_in_plan:
                # Lecture can be set earlier
                if sch_subject.whenStart is not None:
                    continue
                available_actions = environment.get_available_actions(plan, sch_subject)
                the_lower_cost = sys.maxsize
                the_best_action = None
                for action in available_actions:
                    cost = environment.get_cost_of_action(action)
                    if the_lower_cost > cost:
                        the_lower_cost = cost
                        the_best_action = action
                if the_best_action is None:
                    raise Exception("There is no best action, plan may be full!")
                environment.make_action(the_best_action)

    # def set_teachers(self, environment):
    #     # TODO: make it like in set sch subjects
    #     for plan in self.plans:
    #         scheduled_subjects_in_plan = self.scheduled_subjects[plan.title]
    #         for sch_subject in scheduled_subjects_in_plan:
    #             # Lecture can be set earlier
    #             if sch_subject.teacher is not None:
    #                 continue
    #             teachers = environment.get_available_teachers(plan, sch_subject)
    #             if len(teachers) < 1:
    #                 raise Exception("There is no teacher to set, every teacher for subject has a class in this time!")
    #             environment.set_teacher()
    #     pass
    #
    # def set_rooms(self):
    #     # TODO: make it like in set sch subjects
    #     pass


class GraphAlgorithmRunner:

    def __init__(self):
        self.the_best_result = None

    def create_plan_async(self, winter_or_summer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8, max_hour=19):
        teachers = list(Teacher.objects.all())
        rooms = list(Room.objects.all())
        fields_of_study = list(FieldOfStudy.objects.all())
        plans = create_empty_plans(fields_of_study, how_many_plans, winter_or_summer)
        plans_scheduled_subjects = dict()

        for plan in plans:
            scheduled_subjects = create_scheduled_subjects(plan)
            plans_scheduled_subjects[plan.title] = scheduled_subjects

        algorithm = GraphAlgorithm(teachers, rooms, plans, plans_scheduled_subjects, min_hour, max_hour)
        algorithm.create_plan()

    def create_plan_async_without_deleting(self, min_hour=8, max_hour=19):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        plans = Plan.objects.all()
        scheduled_subject = ScheduledSubject.objects.all()
        algorithm = GraphAlgorithm(teachers, rooms, plans, scheduled_subject, min_hour, max_hour)
        algorithm.create_plan()

    def save_the_best_result(self):
        logging.log(level=logging.INFO, msg="Algorithm not supported!")
