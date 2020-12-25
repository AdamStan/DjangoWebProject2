# TODO: create plan with improvements!!!
import logging
from entities.models import FieldOfStudy, Plan, Teacher, Room, ScheduledSubject
from .algorithms_helper import create_empty_plans, create_scheduled_subjects


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
        pass


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
