# use https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model/
# as template
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.contrib.auth import authenticate

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name','surname','username',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('This username is taken')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords don\'t match')
        return password # doesn't matter cp or password, both are the same

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='password_confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('This username is taken')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords don\'t match')
        return password  # doesn't matter cp or password, both are the same

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'second_name', 'surname')

    def clean_password(self):
        return self.initial["password"]

class MyAccountUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password', 'name','second_name', 'surname']