import logging
from tensorflow import keras
import random
from entities.models import FieldOfStudy, Teacher, Room, Plan, ScheduledSubject
from plans.algorithms.algorithms_helper import check_action_can_be_done, create_scheduled_subjects, create_empty_plans
from plans.algorithms.neural_networks.neural_network_algorithm import NNPlanGeneratorAlgorithmBase


class NeuralNetworkForThreeInputConcatenation(NNPlanGeneratorAlgorithmBase):
    model = keras.models.load_model("plans/algorithms/neural_networks/model-3-input1.h5")

    def __init__(self, teachers, rooms, plans,
                 scheduled_subjects_in_plans, min_hour=8, max_hour=19):
        super(NeuralNetworkForThreeInputConcatenation, self).__init__(
            teachers, rooms, plans, scheduled_subjects_in_plans,
            min_hour=8, max_hour=19)

    def set_scheduled_subject(self, environment):
        self.logger.log(logging.INFO, "Starting scheduling using NN - 3 input")
        for plan in self.plans:
            scheduled_subjects_in_plan = self.scheduled_subjects[plan.title]
            for sch_subject in scheduled_subjects_in_plan:
                # Lecture can be set earlier
                if sch_subject.whenStart is not None:
                    continue
                teachers_for_sch = Teacher.objects.filter(subject=sch_subject.subject)
                rooms_for_sch = Room.objects.filter(room_type=sch_subject.type)
                teacher = random.choice(teachers_for_sch)
                room = random.choice(rooms_for_sch)

                available_actions_for_plan = []
                available_actions_for_teacher = []
                available_actions_for_room = []
                all_actions = environment.prepare_actions(plan, sch_subject, [teacher], [room])
                for action in all_actions:
                    subjects_from_plan = environment.scheduled_subjects[plan.title]
                    subjects_for_teacher = environment.sch_subjects_teachers[action.teacher.user.id]
                    subjects_for_room = environment.sch_subjects_rooms[action.room.id]
                    if check_action_can_be_done(action, subjects_from_plan):
                        available_actions_for_plan.append(action)
                    if check_action_can_be_done(action, subjects_for_teacher):
                        available_actions_for_teacher.append(action)
                    if check_action_can_be_done(action, subjects_for_room):
                        available_actions_for_room.append(action)
                the_best_action = self.get_action_from_NN(available_actions_for_plan, available_actions_for_teacher,
                                                          available_actions_for_room)
                environment.make_action(the_best_action)

    def get_action_from_NN(self, actions_for_plan, actions_for_teacher, actions_for_room):
        available_hours_plan = self.get_time_list(actions_for_plan)
        available_hours_teacher = self.get_time_list(actions_for_teacher)
        available_hours_room = self.get_time_list(actions_for_room)
        output = NeuralNetworkForThreeInputConcatenation.model.predict([available_hours_plan,
                                                           available_hours_teacher,
                                                           available_hours_room])
        index_max = 0
        for i in range(len(output[0])):
            if output[0][index_max] < output[0][i]:
                index_max = i
        return actions_for_plan[index_max]

    def get_time_list(self, actions):
        available_hours = list()
        for action in actions:
            available_hours.append(action.day)
            available_hours.append(action.time.hour)
            available_hours.append(action.time.hour + action.schedule_subject.how_long)
        return available_hours


class NeuralNetworkThreeInputConcatenationRunner:
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

        algorithm = NeuralNetworkForThreeInputConcatenation(teachers, rooms, plans, plans_scheduled_subjects, min_hour, max_hour)
        algorithm.create_plan()

        self.the_best_result = "result", algorithm.value_of_plans()
        algorithm.save_result()

    def create_plan_async_without_deleting(self, min_hour=8, max_hour=19):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        plans = Plan.objects.all()
        scheduled_subject = ScheduledSubject.objects.all()

        for subject in scheduled_subject:
            subject.whenStart = None
            subject.whenFinnish = None
            subject.teacher = None
            subject.room = None
            subject.dayOfWeek = None

        algorithm = NeuralNetworkForThreeInputConcatenation(teachers, rooms, plans, scheduled_subject, min_hour, max_hour)
        algorithm.create_plan()
