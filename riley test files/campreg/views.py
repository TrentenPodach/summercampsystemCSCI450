from django.shortcuts import render, redirect
from .forms import FamilyForm, PrimaryContactForm, LoginForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Individual


def home(request):
    return render(request, 'campreg/home.html')

@login_required(login_url="/users/login/")
def register(request):
    if request.method == 'POST':
        individual_form = PrimaryContactForm(request.POST)
        family_form = FamilyForm(request.POST)

        if individual_form.is_valid() and family_form.is_valid():
            user_email = individual_form.cleaned_data["email"]

            # Save the primary contact
            primary = individual_form.save()

            # Save the family
            family = family_form.save(commit=False)
            family.primary_contact = primary
            family.save()
            family.members.add(primary)

           # === Process children ===
            child_index = 0
            while True:
                prefix = f"child_{child_index}_"
                key = prefix + "first_name"
                if key not in request.POST:
                    break  # No more children submitted

                first = request.POST.get(prefix + "first_name")
                last = request.POST.get(prefix + "last_name")
                dob = request.POST.get(prefix + "dob")
                email = request.POST.get(prefix + "email")

                if first and last and dob:
                    child = Individual(
                        first_name=first,
                        last_name=last,
                        date_of_birth=dob,
                        email=email if email else None
                    )
                    child.save()
                    family.members.add(child)

                child_index += 1

            # Send confirmation email
            send_mail(
                "Regent Summer Camp Registration Confirmation",
                "Your application to participate in the Regent University Summer Camp has been approved.\nFor more information, visit 127.0.0.1:8000/home",
                settings.EMAIL_HOST_USER,
                [user_email]
            )

            return redirect('registration_success')
        else:
            print("Form errors:", individual_form.errors, family_form.errors)
    else:
        individual_form = PrimaryContactForm()
        family_form = FamilyForm()

    return render(request, 'campreg/camp_register.html', {
        'individual_form': individual_form,
        'family_form': family_form
    })


def registration_success(request):
    return render(request, 'campreg/success.html')


