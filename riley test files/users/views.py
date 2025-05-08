from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CreateUserForm, CreateLoginForm, CreateFamilyEditForm
from campreg.forms import IndividualForm
from campreg.models import Individual, Family
from django.core.mail import send_mail
from django.conf import settings
from campreg.models import Camp, WaitingList

# Create your views here.

def account_view(request):
    user = request.user

    try:
        individual = Individual.objects.get(user=user)
        family = Family.objects.get(primary_contact=individual)
    except (Individual.DoesNotExist, Family.DoesNotExist):
        individual = None
        family = None

    if request.method == 'POST':
        individual_form = IndividualForm(request.POST, instance=individual)
        if individual_form.is_valid():
            individual_form.save()
            return redirect("home")
    else:
        individual_form = IndividualForm(instance=individual)

    members = family.members.exclude(id=family.primary_contact.id) if family else []
    registered_camps = Camp.objects.filter(registered_families=family) if family else []
    waitlisted_camps = WaitingList.objects.filter(family=family) if family else []

    return render(request, 'users/account.html', {
        'individual_form': individual_form,
        'family': family,
        'members': members,
        'registered_camps': registered_camps,
        'waitlisted_camps': waitlisted_camps
    })


def registration_success(request):
    return render(request, 'campreg/success.html')

def register_view(request):
    if request.method == "POST":
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            #account = request.user
            user_email = register_form.cleaned_data["email"]
            print("Before save.")
            login(request, register_form.save())
            print("Sending email...")           
            send_mail("Regent Summer Camp Registration Confirmation","Your application to participate in the Regent University Summer Camp has been approved. \nFor more information, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[user_email])
            print("Email sent!")

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