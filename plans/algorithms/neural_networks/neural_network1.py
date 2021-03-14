import logging
from tensorflow import keras
import random
from entities.models import FieldOfStudy, Teacher, Room, Plan, ScheduledSubject
from plans.algorithms.algorithms_helper import check_action_can_be_done, create_scheduled_subjects, create_empty_plans
from plans.algorithms.neural_networks.neural_network_algorithm import NNPlanGeneratorAlgorithmBase
from plans.algorithms.neural_networks.neural_network_concatenation3input import \
    NeuralNetworkThreeInputConcatenationRunner


class NeuralNetworkForOneInput(NNPlanGeneratorAlgorithmBase):
    model = keras.models.load_model("plans/algorithms/neural_networks/model-1-input-the-best-score.h5")

    def __init__(self, teachers, rooms, plans,
                 scheduled_subjects_in_plans, min_hour=8, max_hour=19):
        super(NeuralNetworkForOneInput, self).__init__(teachers, rooms, plans, scheduled_subjects_in_plans, min_hour=8,
                                                       max_hour=19)

    def set_scheduled_subject(self, environment):
        self.logger.log(logging.INFO, "Starting scheduling using NN - 1 input")

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

                available_actions = list()
                all_actions = environment.prepare_actions(plan, sch_subject, [teacher], [room])
                for action in all_actions:
                    subjects_from_plan = environment.scheduled_subjects[plan.title]
                    subjects_for_teacher = environment.sch_subjects_teachers[action.teacher.user.id]
                    subjects_for_room = environment.sch_subjects_rooms[action.room.id]
                    if check_action_can_be_done(action, subjects_from_plan) \
                            and check_action_can_be_done(action, subjects_for_teacher) \
                            and check_action_can_be_done(action, subjects_for_room):
                        available_actions.append(action)
                the_best_action = self.get_action_from_NN(available_actions)
                environment.make_action(the_best_action)

    def get_action_from_NN(self, available_actions):
        available_hours = list()
        for action in available_actions:
            available_hours.append([action.day, action.time.hour,
                                    action.time.hour + action.schedule_subject.how_long])
        for _ in range(len(available_hours), 55):
            available_hours.append([0, 0, 0])
        output = NeuralNetworkForOneInput.model.predict([available_hours])
        index_max = 0
        for i in range(len(output[0])):
            if output[0][index_max] < output[0][i]:
                index_max = i
        return available_actions[index_max]


class NeuralNetworkOneInputRunner:
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

        algorithm = NeuralNetworkForOneInput(teachers, rooms, plans, plans_scheduled_subjects, min_hour, max_hour)
        self.the_best_result = algorithm.create_plan()
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

        algorithm = NeuralNetworkForOneInput(teachers, rooms, plans, scheduled_subject, min_hour, max_hour)
        self.the_best_result = algorithm.create_plan()
        algorithm.save_result()


class NeuralNetworkRunner:
    def __init__(self, type_of_neural_network):
        self.type_of_neural_network = type_of_neural_network
        self.the_best_result = None

    def create_plan_async(self, winter_or_summer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8, max_hour=19):
        if self.type_of_neural_network == 1:
            runner = NeuralNetworkOneInputRunner()
            runner.create_plan_async(winter_or_summer, how_many_plans, min_hour, max_hour)
        elif self.type_of_neural_network == 2:
            runner = NeuralNetworkThreeInputConcatenationRunner()
            runner.create_plan_async(winter_or_summer, how_many_plans, min_hour, max_hour)
        elif self.type_of_neural_network == 3:
            # TODO: add neural network with LSTM!!!
            raise Exception("3rd type not supported yet !!!")
        else:
            raise Exception("There is no type for " + str(self.type_of_neural_network) + "!!!")
        self.the_best_result = runner.the_best_result
        print(self.type_of_neural_network)

    def create_plan_async_without_deleting(self, min_hour=8, max_hour=19):
        if self.type_of_neural_network == 1:
            runner = NeuralNetworkOneInputRunner()
            runner.create_plan_async_without_deleting(min_hour, max_hour)
        elif self.type_of_neural_network == 2:
            runner = NeuralNetworkThreeInputConcatenationRunner()
            runner.create_plan_async_without_deleting(min_hour, max_hour)
        elif self.type_of_neural_network == 3:
            # TODO: add neural network with LSTM!!!
            raise Exception("3rd type not supported yet !!!")
        else:
            raise Exception("There is no type for " + str(self.type_of_neural_network) + "!!!")
        self.the_best_result = runner.the_best_result
        print(self.type_of_neural_network)


