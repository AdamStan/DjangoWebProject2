import logging
from tensorflow import keras
import random
from entities.models import FieldOfStudy, Teacher, Room, Plan, ScheduledSubject
from plans.algorithms.algorithms_helper import check_action_can_be_done, create_scheduled_subjects, create_empty_plans
from plans.algorithms.neural_networks.neural_network_algorithm import NNPlanGeneratorAlgorithmBase
import numpy as np


class NeuralNetworkForThreeInputConcatenation(NNPlanGeneratorAlgorithmBase):
    model = keras.models.load_model("plans/algorithms/neural_networks/model-three-input.h5")

    def __init__(self, teachers, rooms, plans,
                 scheduled_subjects_in_plans, min_hour=8, max_hour=19):
        super(NeuralNetworkForThreeInputConcatenation, self).__init__(
            teachers, rooms, plans, scheduled_subjects_in_plans,
            min_hour=min_hour, max_hour=max_hour)
        self.days = [1, 2, 3, 4, 5]
        self.all_available_hours = [
            self.create_all_available_hours(1),
            self.create_all_available_hours(2),
            self.create_all_available_hours(3)
        ]

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
        available_hours_plan = self.get_time_list_normal_order(actions_for_plan)
        available_hours_teacher = self.get_time_list_normal_order(actions_for_teacher)
        available_hours_room = self.get_time_list_normal_order(actions_for_room)
        # print(available_hours_plan)
        full_options = []
        full_options.extend(available_hours_plan)
        full_options.extend(available_hours_teacher)
        full_options.extend(available_hours_room)

        # available_hours_plan = np.array(available_hours_plan).reshape(1, 165)
        # available_hours_teacher = np.array(available_hours_teacher).reshape(1, 165)
        # available_hours_room = np.array(available_hours_room).reshape(1, 165)
        full_options = np.array(full_options).reshape(1, 165*3)
        output = NeuralNetworkForThreeInputConcatenation.model.predict(full_options)
        index_max = 0
        for i in range(len(output[0])):
            if output[0][index_max] < output[0][i]:
                index_max = i
        # print("Actions av: " + str(len(actions_for_plan)))
        # print("Action taken: " + str(index_max))
        # if index_max > len(actions_for_plan):
        #     print("set breakpoint here")
        # print(available_hours_plan[index_max*3:index_max*3+3])
        return actions_for_plan[index_max]

    def get_time_list_normal_order(self, actions):
        available_hours = list()
        all_possibilities = self.get_av_hours(actions[0].schedule_subject)
        for action in actions:
            available_hours.append(action.day)
            available_hours.append(action.time.hour)
            available_hours.append(action.time.hour + action.schedule_subject.how_long)
        while len(all_possibilities) > len(available_hours):
            available_hours.append(0)
        return available_hours

    def get_time_list(self, actions):
        all_possibilities = self.get_av_hours(actions[0].schedule_subject)
        available_hours = list()
        for action in actions:
            available_hours.append(action.day)
            available_hours.append(action.time.hour)
            available_hours.append(action.time.hour + action.schedule_subject.how_long)
        ptm_index = 0
        new_plan_to_manipulate = []
        for i in range(0, len(all_possibilities), 3):
            if all_possibilities[i] == available_hours[ptm_index] and \
                    all_possibilities[i + 1] == available_hours[ptm_index + 1] and \
                    all_possibilities[i + 2] == available_hours[ptm_index + 2]:
                new_plan_to_manipulate.append(available_hours[ptm_index])
                new_plan_to_manipulate.append(available_hours[ptm_index + 1])
                new_plan_to_manipulate.append(available_hours[ptm_index + 2])
                ptm_index += 3
                if ptm_index >= len(available_hours):
                    break
            else:
                new_plan_to_manipulate.append(0)
                new_plan_to_manipulate.append(0)
                new_plan_to_manipulate.append(0)
        while len(all_possibilities) > len(new_plan_to_manipulate):
            new_plan_to_manipulate.append(0)
        return new_plan_to_manipulate

    def create_all_available_hours(self, how_long):
        available_data = []
        for d in self.days:
            for h in range(self.min_hour, self.max_hour):
                available_data.extend([d, h, h + how_long])
        return available_data

    def get_av_hours(self, sch_subject):
        return self.all_available_hours[sch_subject.how_long - 1]


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

        self.the_best_result = "result", algorithm.value_of_plans()
        algorithm.save_result()
