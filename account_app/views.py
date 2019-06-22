from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from account_app.forms import UserForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(type(user))
        if user is not None:
            auth.login(request,user)
            print("\nUSER logged in\n")
            return redirect('homepage')
        else:
            return render(request,'login.html', {'error':"Invalid login details given"})
    else:
        return render(request,'login.html')


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.first_name = user_form.cleaned_data['FirstName']
            user.last_name = user_form.cleaned_data['LastName']
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            registered = True
            return redirect('homepage')
    else:
        user_form = UserForm()
    args = {'form' : user_form, 'errors': user_form.errors.items()}
    return render(request, 'signup.html', args)



@login_required
def logout(request):
    auth.logout(request)
    return redirect('homepage')
