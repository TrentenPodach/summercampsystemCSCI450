from django.shortcuts import render, redirect
from .forms import FamilyForm, IndividualForm, LoginForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'campreg/home.html')

@login_required(login_url="/users/login/")
def register(request):
    if request.method == 'POST':
        individual_form = IndividualForm(request.POST)
        family_form = FamilyForm(request.POST)

        print("POST DATA:", request.POST)

        if individual_form.is_valid() and family_form.is_valid():
            print("Forms are valid")

            primary = individual_form.save()
            family = family_form.save(commit=False)
            family.primary_contact = primary
            family.save()
            family.members.add(primary)

            return redirect('registration_success')
        else:
            print("Errors:")
            print(individual_form.errors)
            print(family_form.errors)
    else:
        individual_form = IndividualForm()
        family_form = FamilyForm()

    return render(request, 'campreg/camp_register.html', {
        'individual_form': individual_form,
        'family_form': family_form
    })

def registration_success(request):
    return render(request, 'campreg/success.html')


def user_register_view(request):
    if request.method == "POST":
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')
    else:
        register_form = UserCreationForm()
    return render(request, "campreg/userregister.html", { "register_form": register_form })

def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            messages.success(request, "Logged in successfully.")
            return redirect('home')
    else:
        login_form = AuthenticationForm()
    return render(request, "campreg/login.html", {"login_form": login_form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('home')
    return redirect('home')


