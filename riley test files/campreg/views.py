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
from django.contrib import messages

def home(request):
    camps = Camp.objects.filter(archived=False).order_by('start_date')

    for camp in camps:
        camp.enrolled = sum(
            f.members.exclude(id=f.primary_contact.id).count()
            for f in camp.registered_families.all()
        )
        camp.waitlist_count = WaitingList.objects.filter(camp=camp).count()

    return render(request, 'campreg/home.html', {'camps': camps})


@login_required(login_url="/users/login/")
def register(request):
    user = request.user
    individual = Individual.objects.filter(user=user).first()
    family = Family.objects.filter(primary_contact=individual).first() if individual else None
    children = family.members.exclude(id=family.primary_contact.id) if family else []

    if family and Camp.objects.filter(registered_families=family).exists():
        messages.warning(request, "You're already registered for a camp.")
        return redirect('users:account')

    if request.method == 'POST':
        individual_form = PrimaryContactForm(request.POST, instance=individual)
        family_form = FamilyForm(request.POST, instance=family)
        camp_form = CampChoiceForm(request.POST)

        if individual_form.is_valid() and family_form.is_valid() and camp_form.is_valid():
            selected_camp = camp_form.cleaned_data['camp']

            primary = individual_form.save(commit=False)
            primary.user = user
            primary.save()

            family = family_form.save(commit=False)
            family.primary_contact = primary
            family.save()

            family.members.clear()
            family.members.add(primary)

            # Process existing children marked for deletion
            for child in children:
                delete_flag = request.POST.get(f'child_{child.id}_delete', '')
                if delete_flag == "delete":
                    family.members.remove(child)
                    child.delete()
                else:
                    family.members.add(child)

            # Process new children
            child_index = 0
            while True:
                prefix = f"child_{child_index}_"
                if not request.POST.get(prefix + "first_name"):
                    break

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

            current_total = sum(
                f.members.exclude(id=f.primary_contact.id).count()
                for f in selected_camp.registered_families.all()
            )
            registering_now = family.members.exclude(id=family.primary_contact.id).count()

            user_email = family.primary_contact.email

            if current_total + registering_now <= selected_camp.max_capacity:
                selected_camp.registered_families.add(family)
                print(f"Registered {family} to {selected_camp.name}")
                
                send_mail("Regent Summer Camp Registration Confirmation",f"Hello {family.primary_contact.first_name},\n\nYour application to participate in {selected_camp.name} running from {selected_camp.start_date} to {selected_camp.end_date} has been approved.\nFor more information, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[user_email])
                children_email_check = family.members.exclude(id=family.primary_contact.id) if family else []
                for c in children_email_check:
                    if c.email:
                        send_mail("Regent Summer Camp Registration Confirmation",f"Hello {c.first_name},\n\nYour registration for {selected_camp.name} running from {selected_camp.start_date} to {selected_camp.end_date} has been confirmed. \nFor more information, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[c.email])
            else:
                existing_wait = WaitingList.objects.filter(family=family, camp=selected_camp).first()
                if not existing_wait:
                    WaitingList.objects.create(family=family, camp=selected_camp)
                    print(f"{family} added to waitlist for {selected_camp.name}")
                    send_mail("Regent Summer Camp Waitlist",f"Hello {family.primary_contact.first_name},\n\n{selected_camp.name} running from {selected_camp.start_date} to {selected_camp.end_date} is full.\n\nYour application has been processed, and you have been added to the waitlist. If space becomes available for you, you will be registered automatically and an email will be sent to inform you. \nFor more information, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[user_email])
                else:
                    print(f"{family} already on waitlist for {selected_camp.name}")

            return redirect('registration_success')

        else:
            print("Form errors:", individual_form.errors, family_form.errors, camp_form.errors)
    else:
        individual_form = PrimaryContactForm(instance=individual)
        family_form = FamilyForm(instance=family)
        camp_form = CampChoiceForm()

    return render(request, 'campreg/camp_register.html', {
        'individual_form': individual_form,
        'family_form': family_form,
        'camp_form': camp_form,
        'children': children
    })

def registration_success(request):
    return render(request, 'campreg/success.html')

@login_required
def remove_family_from_camp(request, camp_id, family_id):
    camp = get_object_or_404(Camp, id=camp_id)
    family = get_object_or_404(Family, id=family_id)

    if family in camp.registered_families.all():
        camp.registered_families.remove(family)

        # Delete all children (not the primary)
        for member in family.members.exclude(id=family.primary_contact.id):
            family.members.remove(member)
            member.delete()

        promote_next_waitlisted_family(camp)

    else:
        print(f"{family} was not registered in {camp.name}")

    return redirect('home')  # Or anywhere useful

@login_required
def remove_child(request, child_id):
    user = request.user
    individual = Individual.objects.filter(user=user).first()
    family = Family.objects.filter(primary_contact=individual).first()

    if family:
        child = get_object_or_404(Individual, id=child_id)
        if child in family.members.all() and child != family.primary_contact:
            family.members.remove(child)
            child.delete()
            print(f"Removed child {child} from {family}")

    return redirect('register')  # or wherever your registration page lives

