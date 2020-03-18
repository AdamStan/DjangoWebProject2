from django import forms
from .models import *


class CreateBuilding(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'


class CreateFaculty(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'


class CreateFieldOfStudy(forms.ModelForm):
    class Meta:
        model = FieldOfStudy
        fields = '__all__'


class CreatePlan(forms.ModelForm):
    class Meta:
        model = Plan
        fields = '__all__'


class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class CreateScheduledSubject(forms.ModelForm):
    class Meta:
        model = ScheduledSubject
        fields = ['room', 'teacher']


class CreateSubject(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

