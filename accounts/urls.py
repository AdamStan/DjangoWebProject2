from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.show_login, name='login'),
    path('logout/', views.show_logout, name='logout'),
    path('myprofile/', views.show_my_profile, name='myprofile'),
]
