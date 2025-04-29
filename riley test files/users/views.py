from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CreateUserForm, CreateLoginForm

# Create your views here.

def register_view(request):
    if request.method == "POST":
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            login(request, register_form.save())
            return redirect('register')
    else:
        register_form = CreateUserForm()
    return render(request, "users/register.html", { "register_form": register_form })

def login_view(request):
    if request.method == "POST":
        login_form = CreateLoginForm(data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect('register') #Temporarily using 'register' since that is the only other finished non-admin page
    else:
        login_form = CreateLoginForm()
    return render(request, "users/login.html", {"login_form": login_form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('register')