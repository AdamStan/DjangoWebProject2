class QualityPlanFunction:
    def __init__(self, subjects_in_plans):
        """
        @type subjects_in_plans: list of list of scheduled subjects
        """
        self.subjects_in_plans = subjects_in_plans

    def calculate_value(self):
        value = 0
        for sch_subject_list in self.subjects_in_plans:
            value += self.value_for_plan(sch_subject_list)
        return value

    def value_for_plan(self, subjects_in_plan, days=[1, 2, 3, 4, 5]):
        """
        formula: days - empty days +  (end - start - all how long)
        :param subjects_in_plan:
        :return:
        """
        values = []
        value = 0
        for i in range(0, len(days)):
            values.append(1)
            subjects_how_long, first_hour, last_hour = 0, 24, 0
            list_of_subjects_in_one_day = self.get_events_from_one_day(subjects_in_plan, i + 1)
            for subject in list_of_subjects_in_one_day:
                if subject.whenStart.hour < first_hour:
                    first_hour = subject.whenStart.hour
                if subject.whenFinnish.hour > last_hour:
                    last_hour = subject.whenFinnish.hour
                subjects_how_long += subject.how_long
            if not list_of_subjects_in_one_day:
                values[i] -= 1
            else:
                values[i] += last_hour - first_hour - subjects_how_long
            value += values[i]

        return value

    def get_events_from_one_day(self, subjects_in_plan, day_int):
        subjects_in_one_day = []
        for subject in subjects_in_plan:
            if subject.dayOfWeek == day_int:
                subjects_in_one_day.append(subject)
        return subjects_in_one_day


class QualityPlanFunction2:
    # TODO: create new quality function for plans
    pass
