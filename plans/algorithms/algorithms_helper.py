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


def create_scheduled_subjects(plan, weeks):
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
