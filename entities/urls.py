from django.contrib import admin
from django.urls import path, re_path
from . import models_views
from . import views

app_name = 'entities'

urlpatterns = [
    path('timetables/student', views.show_student_plans, name='timetables_student'),
    path('timetables/teacher', views.show_teachers_plans, name='timetables_teacher'),
    path('timetables/room', views.show_rooms_plans, name='timetables_room'),
    path('edittimetables', views.show_edit_timetable, name='edittimetables'),
    path('studentplans/', views.show_choose_plan, name='studentplans'),
    path('studentplan/', views.show_student_plan, name="studentplan"),
    path('teacherplan/', views.show_teacher_plan, name='teacherplan'),
    path('generate/', views.show_generate_page, name='generate'),
    path('forbidden/', views.show_forbidden, name='forbidden'),
]

tab_models_urls = [
    path('admin/models/', models_views.show_intro_edit_models, name='models'),
    path('admin/models/building', models_views.show_building, name='model_building'),
    path('admin/models/faculty', models_views.show_faculty, name='model_faculty'),
    path('admin/models/fieldofstudy', models_views.show_fieldofstudy, name='model_field_of_study'),
    path('admin/models/plan', models_views.show_plan, name='model_plan'),
    path('admin/models/room', models_views.show_room, name='model_room'),
    path('admin/models/scheduledsubject', models_views.show_scheduledsubject, name='model_scheduledsubject'),
    path('admin/models/subject', models_views.show_subject, name='model_subject'),
    path('admin/models/student', models_views.show_student, name='model_student'),
    path('admin/models/teacher', models_views.show_teacher, name='model_teacher'),
    path('admin/models/user', models_views.show_user, name='model_user'),
    path('admin/models/teacher_to_subject', models_views.show_teacher_to_subject, name="model_teachertosubject")
]

urlpatterns += tab_models_urls
