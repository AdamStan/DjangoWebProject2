from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyAccountUpdate
from .models import User
# Create your views here.


def show_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html',{'form':form})


def show_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    return redirect('homepage')


@login_required
def show_my_profile(request):
    user = request.user
    s_message = None
    fail_message = None
    if request.POST:
        action = request.POST.get("action")
        if action == "Update":
            username = request.POST.get('username')
            name = request.POST.get('name')
            second_name = request.POST.get('second_name')
            surname = request.POST.get('surname')
            user.username = username
            user.name = name
            user.second_name = second_name
            user.surname = surname
            user.save()
            print("Update")
        elif action == "Change":
            print("Change")
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            confirm_new_password =request.POST.get('confirm_new_password')
            print(new_password)
            print(password)
            if user.check_password(password):
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    s_message = "Your password was changed with success"
                    user.save()
                else:
                    fail_message = "Your passwords don't match"
            else:
                fail_message = "Your password don't match"

    return render(request, 'myprofile.html', {'current_user': user, "s_message": s_message,
                                              "fail_message": fail_message} )
