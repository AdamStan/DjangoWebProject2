from .models import User

'''
This is a function for adding example data to database
'''
def add_data():
    # -- admins --
    User.objects.create_superuser(
        username="admin123",
        password="haslo123",
        name="admin_name",
        surname="admin_surname"
    )
    # -- teachers --
    User.objects.create_teacher(
        username="teacher1",
        password="teacher_user",
        name="Jan",
        surname="Kowalski"
    )
    User.objects.create_teacher(
        username="teacher2",
        password="teacher_user",
        name="Anna",
        surname="Kowalska"
    )
    User.objects.create_teacher(
        username="teacher3",
        password="teacher_user",
        name="Andrzej",
        surname="Nowak"
    )
    User.objects.create_teacher(
        username="teacher4",
        password="teacher_user",
        name="Arleta",
        surname="Gałga"
    )
    User.objects.create_teacher(
        username="teacher5",
        password="teacher_user",
        name="Marzena",
        surname="Domańska"
    )
    User.objects.create_teacher(
        username="teacher6",
        password="teacher_user",
        name="Maria",
        surname="Szczerska"
    )
    # -- students --
    User.objects.create_student(
        username="student1",
        password="student_user",
        name="Adam",
        surname="Stańczyk"
    )
    User.objects.create_student(
        username="student2",
        password="student_user",
        name="Michał",
        surname="Wielosiński"
    )
    User.objects.create_student(
        username="student3",
        password="student_user",
        name="Jaroslaw",
        surname="Tusk"
    )
    User.objects.create_student(
        username="student4",
        password="student_user",
        name="Donald",
        surname="Kaczyński"
    )
    User.objects.create_student(
        username="student5",
        password="student_user",
        name="Beata",
        surname="Kopacz",
    )
    User.objects.create_student(
        username="student6",
        password="student_user",
        name="Ewa",
        surname="Szydlo",
    )
    User.objects.create_student(
        username="student7",
        password="student_user",
        name="Beata",
        surname="Kopacz"
    )
    User.objects.create_student(
        username="student8",
        password="student_user",
        name="Piotr",
        surname="Stolarski",
    )
    User.objects.create_student(
        username="student9",
        password="student_user",
        name="Maciej",
        sname="Andrzej",
        surname="Rudnik"
    )
    User.objects.create_student(
        username="student10",
        password="student_user",
        name="Mariusz",
        sname="Józef",
        surname="Poniatowski"
    )
    User.objects.create_student(
        username="student11",
        password="student_user",
        name="Anna",
        sname="Maria",
        surname="Górniak"
    )
    User.objects.create_student(
        username="student12",
        password="student_user",
        name="Edyta",
        surname="Jopek"
    )
    User.objects.create_student(
        username="student13",
        password="student_user",
        name="Arkadiusz",
        surname="Musiał"
    )
    User.objects.create_student(
        username="student14",
        password="student_user",
        name="Tomasz",
        surname="Malarz"
    )
    User.objects.create_student(
        username="student15",
        password="student_user",
        name="Katarzyna",
        surname="Popowska"
    )
    add_more_teachers()

def add_more_teachers():
    # -- teachers --
    User.objects.create_teacher(
        username="teacher7",
        password="teacher_user",
        name="Andrzej",
        surname="Krzywonos"
    )
    User.objects.create_teacher(
        username="teacher8",
        password="teacher_user",
        name="Beata",
        sname="Maria",
        surname="Opania"
    )
    User.objects.create_teacher(
        username="teacher9",
        password="teacher_user",
        name="Weronika",
        surname="Rutkowska"
    )
    User.objects.create_teacher(
        username="teacher10",
        password="teacher_user",
        name="Maciej",
        surname="Cerski"
    )
    User.objects.create_teacher(
        username="teacher11",
        password="teacher_user",
        name="Grazyna",
        surname="Kulesza"
    )
    User.objects.create_teacher(
        username="teacher12",
        password="teacher_user",
        name="Czesława",
        surname="Juryzdyńska"
    )
    User.objects.create_teacher(
        username="teacher13",
        password="teacher_user",
        name="Piotr",
        sname="Paweł",
        surname="Opolski"
    )
    User.objects.create_teacher(
        username="teacher14",
        password="teacher_user",
        name="Paulina",
        surname="Gajos"
    )
    User.objects.create_teacher(
        username="teacher15",
        password="teacher_user",
        name="Michał",
        surname="Gronkiewicz"
    )
    User.objects.create_teacher(
        username="teacher16",
        password="teacher_user",
        name="Ewa",
        sname="Anna",
        surname="Trojan"
    )
    User.objects.create_teacher(
        username="teacher17",
        password="teacher_user",
        name="Andżelika",
        surname="Domańska"
    )
    User.objects.create_teacher(
        username="teacher18",
        password="teacher_user",
        name="Maria",
        surname="Lubomirska"
    )