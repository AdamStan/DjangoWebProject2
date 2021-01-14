from entities.models import Plan, Subject, ScheduledSubject


def create_empty_plans(fields_of_study, how_many_plans, winter_or_summer):
    plans = []

    for field in fields_of_study:
        if field.whenDoesItStarts == winter_or_summer:
            sm = 1
        else:
            sm = 2
        for sem in range(sm, field.howManySemesters + 1, 2):
            for i in range(1, how_many_plans + 1):
                title_of_plan = field.name + str(sem) + "_" + str(i) + "|" + field.degree
                plans.append(Plan(title=title_of_plan, fieldOfStudy=field, semester=sem))
    return plans


def create_scheduled_subjects(plan, weeks=15):
    subjects = Subject.objects.filter(fieldOfStudy=plan.fieldOfStudy, semester=plan.semester)
    list_of_scheduled_subjects = []
    for subject in subjects:
        bullshit = subject.fieldOfStudy.faculty
        if subject.lecture_hours and subject.lecture_hours > 0:
            list_of_scheduled_subjects.append(
                ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LECTURE,
                                    how_long=int(subject.lecture_hours / weeks))
            )
        if subject.laboratory_hours and subject.laboratory_hours > 0:
            list_of_scheduled_subjects.append(
                ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LABORATORY,
                                    how_long=int(subject.laboratory_hours / weeks))
            )
    return list_of_scheduled_subjects


def show_objects(objects):
    for obj in objects:
        print(str(obj))


def show_subjects(scheduled_subjects):
    for sch in scheduled_subjects:
        print(str(sch) + ", " + str(sch.whenStart) + ", " + str(sch.whenFinnish) + ", day:" + str(sch.dayOfWeek)
                + ", how_long: " + str(sch.how_long))


def check_action_can_be_done(action, subjects_by_day):
    # search the subject from plan
    if len(subjects_by_day[action.day]) > 0:
        for subject_in_plan in subjects_by_day[action.day]:
            difference_between_starts = abs(action.time.hour - subject_in_plan.whenStart.hour)
            difference_between_ends = abs(action.time.hour + action.schedule_subject.how_long -
                                          subject_in_plan.whenFinnish.hour)
            if (difference_between_starts + difference_between_ends) \
                    < (action.schedule_subject.how_long + subject_in_plan.how_long):
                return False
    return True


def get_events_by_day(subjects_in_plan):
    """
    @param subjects_in_plan: a list or other iterable
    @return: dictionary with a day as a key and a list of scheduled_subjects as a value
    """
    days = [0, 1, 2, 3, 4, 5, 6]
    subjects_by_days = dict()
    for day in days:
        subjects_by_days[day] = list()
        for subject in subjects_in_plan:
            if subject.dayOfWeek == day:
                subjects_by_days[day].append(subject)
    return subjects_by_days


def check_room_can_be_set(sch_subject, scheduled_subjects_in_room):
    for event in scheduled_subjects_in_room:
        difference_between_starts = abs(event.whenStart.hour - sch_subject.whenStart.hour)
        difference_between_ends = abs(event.whenFinnish.hour - sch_subject.whenFinnish.hour)
        is_the_same_day = event.dayOfWeek == sch_subject.dayOfWeek
        if is_the_same_day and \
                (difference_between_starts + difference_between_ends) < (event.how_long + sch_subject.how_long):
            return False

    return True


def check_teacher_can_teach(sch_subject, teachers_subjects):
    for event in teachers_subjects:
        difference_between_starts = abs(event.whenStart.hour - sch_subject.whenStart.hour)
        difference_between_ends = abs(event.whenFinnish.hour - sch_subject.whenFinnish.hour)
        is_the_same_day = event.dayOfWeek == sch_subject.dayOfWeek
        if is_the_same_day and \
                (difference_between_starts + difference_between_ends) < (event.how_long + sch_subject.how_long):
            return False

    return True


def check_hour_is_available(hour, scheduled_subjects, how_long):
    for event in scheduled_subjects:
        difference_between_starts = abs(event.whenStart.hour - hour)
        difference_between_ends = abs(event.whenFinnish.hour - hour)
        if (difference_between_starts + difference_between_ends) < (event.how_long + how_long):
            return False

    return True
