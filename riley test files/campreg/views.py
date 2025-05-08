from django.shortcuts import render, redirect
from .forms import FamilyForm, PrimaryContactForm, LoginForm, CampChoiceForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Camp, WaitingList, Individual, Family
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'campreg/home.html')

@login_required(login_url="/users/login/")
def register(request):
    if request.method == 'POST':
        individual_form = PrimaryContactForm(request.POST)
        family_form = FamilyForm(request.POST)
        camp_form = CampChoiceForm(request.POST)

        if individual_form.is_valid() and family_form.is_valid() and camp_form.is_valid():
            user_email = individual_form.cleaned_data["email"]

            # Save the primary contact
            primary = individual_form.save()

            # Save the family
            family = family_form.save(commit=False)
            family.primary_contact = primary
            family.save()
            family.members.add(primary)

            # Save children
            child_index = 0
            while True:
                prefix = f"child_{child_index}_"
                key = prefix + "first_name"
                if key not in request.POST:
                    break  # No more children

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

            # Enroll or waitlist
            selected_camp = camp_form.cleaned_data["camp"]
            if selected_camp.registered_families.count() < selected_camp.max_capacity:
                selected_camp.registered_families.add(family)
                camp_status = "registered"
            else:
                WaitingList.objects.create(family=family, camp=selected_camp)
                camp_status = "waitlisted"
            '''
            # Send confirmation email
           if selected_camp.registered_families.count() < selected_camp.max_capacity:
                selected_camp.registered_families.add(family)

                send_mail(
                    "Regent Summer Camp Registration Confirmation",
                    "Your registration for the Regent University Summer Camp has been confirmed!\n\nVisit 127.0.0.1:8000/home for details.",
                    settings.EMAIL_HOST_USER,
                    [user_email]
                )
            else:
                WaitingList.objects.create(family=family, camp=selected_camp)

                send_mail(
                    "Regent Summer Camp Waitlist Notification",
                    "The camp you selected is currently full, and you have been added to the waitlist.\n\nWe will notify you if a spot becomes available.",
                    settings.EMAIL_HOST_USER,
                   [user_email]
                )
            '''

            return redirect('registration_success')
        else:
            print("Form errors:", individual_form.errors, family_form.errors, camp_form.errors)
    else:
        individual_form = PrimaryContactForm()
        family_form = FamilyForm()
        camp_form = CampChoiceForm()

    return render(request, 'campreg/camp_register.html', {
        'individual_form': individual_form,
        'family_form': family_form,
        'camp_form': camp_form
    })

def registration_success(request):
    return render(request, 'campreg/success.html')

def promote_next_waitlisted_family(camp):
    next_waitlisted = WaitingList.objects.filter(camp=camp).order_by('date_added').first()
    if next_waitlisted:
        camp.registered_families.add(next_waitlisted.family)
        next_waitlisted.delete()

        # TEMP: Print for dev testing
        print(f"Promoted {next_waitlisted.family} from waitlist to camp: {camp.name}")

@login_required
def remove_family_from_camp(request, camp_id, family_id):
    camp = get_object_or_404(Camp, id=camp_id)
    family = get_object_or_404(Family, id=family_id)

    if family in camp.registered_families.all():
        camp.registered_families.remove(family)
        print(f"Removed {family} from {camp.name}")
        promote_next_waitlisted_family(camp)
    else:
        print(f"{family} was not registered in {camp.name}")

    return redirect('home')  # Or anywhere useful