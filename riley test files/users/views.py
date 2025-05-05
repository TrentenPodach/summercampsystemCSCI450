from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CreateUserForm, CreateLoginForm, CreateFamilyEditForm
from campreg.forms import IndividualForm
from campreg.models import Individual, Family
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def account_view(request):
    account = request.user
    #individual_form = IndividualForm(instance=account)
    #accountFam = Family.objects.get(id=user_id)
    #family_edit_form = CreateFamilyEditForm(id=user_id)


    if request.method == 'POST':
        individual_form = IndividualForm(request.POST, instance=account)
        #family_edit_form = CreateFamilyEditForm(request.POST)

        #print("POST DATA:", request.POST)

        if individual_form.is_valid(): #and family_edit_form.is_valid():
            print("Forms are valid")
            individual_form.save()
            return redirect("home")
            #Save the data

        else:
            print("Errors:")
            print(individual_form.errors)
            #print(family_edit_form.errors)
    else:
        individual_form = IndividualForm(instance=account)
        #family_edit_form = CreateFamilyEditForm()

    return render(request, 'users/account.html', {
        'individual_form': individual_form,
        #'family_form': family_edit_form
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