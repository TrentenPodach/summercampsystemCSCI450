from django.shortcuts import render, redirect
from .forms import FamilyForm, IndividualForm, LoginForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

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

            user_email = individual_form.cleaned_data["email"]

            primary = individual_form.save()
            family = family_form.save(commit=False)
            family.primary_contact = primary
            family.save()
            family.members.add(primary)
         
            send_mail("Regent Summer Camp Registration Confirmation","Your application to participate in the Regent University Summer Camp has been approved. \nFor more information, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[user_email])

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


