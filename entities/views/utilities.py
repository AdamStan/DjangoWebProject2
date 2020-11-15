from entities.models import Teacher, Plan, ScheduledSubject, Room
import json

class SubjectExample:
    id = 0
    name = ""
    whenStart = 0
    how_long = 0
    day = "monday"
    def toJSON(self):
        return json.dumps(self.__dict__)


class TeacherBox:
    id = 0
    title = ""

# TODO: Move help functions to diff files!!
def create_table_example():
    values = []
    return {'values': values}


def create_table(plan_id):
    plan = Plan.objects.get(id=plan_id)
    subjects = ScheduledSubject.objects.filter(plan=plan).order_by('dayOfWeek')
    values = []
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday",]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        teacher_name = ""
        if ss.teacher:
            teacher_name = ss.teacher.user.name + " " + ss.teacher.user.surname
        buff.name = ss.subject.name + " " + ss.type + " " + teacher_name
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())

    return {"values": values}, plan.title


def create_table_for_teacher(teacher_id):
    teacher = Teacher.objects.get(user_id=teacher_id)
    subjects = ScheduledSubject.objects.filter(teacher=teacher).order_by('dayOfWeek')
    values = []
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", ]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        buff.name = ss.subject.name + " " + ss.type + " " + ss.plan.title
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())
    plan_title = teacher.user.name + " " + teacher.user.surname
    return {"values": values}, plan_title


def get_plans_for_rooms():
    rooms = Room.objects.all()
    return rooms


def create_table_for_room(room_id):
    room = Room.objects.get(id=room_id)
    subjects = ScheduledSubject.objects.filter(room=room).order_by('dayOfWeek')
    values = []
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", ]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        teacher_name = ss.teacher.user.name + " " + ss.teacher.user.surname
        buff.name = ss.subject.name + " " + ss.type + " " + ss.plan.title + " " + teacher_name
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())

    return {"values": values}, room.id