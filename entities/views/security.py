forbidden = "/entities/forbidden/"


def test_user_is_student(user):
    return user.student


def test_user_is_teacher(user):
    return user.teacher


def test_user_is_admin(user):
    return user.admin
