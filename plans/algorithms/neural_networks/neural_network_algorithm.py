import logging
from entities.models import ScheduledSubject, Plan
from plans.algorithms.state import Environment
from plans.algorithms.value_strategies import ValueOfPlanStrategy1


class NNPlanGeneratorAlgorithmBase:

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
        self.logger = logging.getLogger("[NeuralNetwork][ALGO]")
        self.strategy = ValueOfPlanStrategy1()

    def create_plan(self):
        self.logger.log(logging.INFO, "Starting creating plan with graph algorithm")
        all_scheduled_subjects = list()
        for subjects_list in self.scheduled_subjects.values():
            all_scheduled_subjects += subjects_list
        environment_sch_subjects = Environment(self.plans, all_scheduled_subjects, self.strategy,
                                               self.teachers, self.rooms, self.min_hour, self.max_hour)
        self.set_scheduled_subject(environment_sch_subjects)

        self.save_result()

    def set_scheduled_subject(self, environment):
        raise Exception("set_scheduled_subject not implemented!")

    def save_result(self):
        ScheduledSubject.objects.all().delete()
        Plan.objects.all().delete()
        for plan in self.plans:
            plan.save()
        for plan_sch_subjects in self.scheduled_subjects.values():
            for sch_subject in plan_sch_subjects:
                sch_subject.save()
