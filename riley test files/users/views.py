from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .forms import CreateUserForm, CreateLoginForm, CreateFamilyEditForm
from campreg.forms import IndividualForm
from campreg.models import Individual, Family, Camp, WaitingList

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
'''
def promote_next_waitlisted_family(camp):
    next_waitlisted = WaitingList.objects.filter(camp=camp).order_by('date_added').first()
    if next_waitlisted:
        camp.registered_families.add(next_waitlisted.family)
        waitlist_email = next_waitlisted.family.primary_contact.email
        send_mail("Regent Summer Camp Registration Confirmation","Space has opened in the camp and you have been moved from the waitlist and registered. \nFor more information, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[waitlist_email])
        children = next_waitlisted.family.members.exclude(id=next_waitlisted.family.primary_contact.id) if next_waitlisted.family else []
        for c in children:
            if c.email:
                send_mail("Regent Summer Camp Registration Confirmation","Your registration for the Regent University Summer Camp has been confirmed. \nFor more information, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[c.email])
        next_waitlisted.delete()
        print(f"Promoted {next_waitlisted.family} to {camp.name}")
'''
@login_required
def remove_camp_registration(request, camp_id):
    user = request.user
    try:
        individual = Individual.objects.get(user=user)
        family = Family.objects.get(primary_contact=individual)
        camp = Camp.objects.get(id=camp_id)

        if family in camp.registered_families.all():
            # Remove from camp
            camp.registered_families.remove(family)

            # Remove non-primary children
            for member in family.members.exclude(id=family.primary_contact.id):
                family.members.remove(member)
                member.delete()

            # Promote from waitlist
            promote_next_waitlisted_family(camp)

            print(f"{family} removed from {camp.name}")
    except (Individual.DoesNotExist, Family.DoesNotExist, Camp.DoesNotExist):
        print("Could not remove registration: object not found.")

    return redirect('users:account')

def promote_next_waitlisted_family(camp):
    waitlist = WaitingList.objects.filter(camp=camp).order_by('date_added')

    for entry in waitlist:
        family = entry.family
        children = family.members.exclude(id=family.primary_contact.id)
        child_count = children.count()

        current_enrolled = sum(
            f.members.exclude(id=f.primary_contact.id).count()
            for f in camp.registered_families.all()
        )
        available_spots = max(0, camp.max_capacity - current_enrolled)

        if child_count <= available_spots:
            # Register the family
            camp.registered_families.add(family)

            # Send email to primary contact
            waitlist_email = family.primary_contact.email
            children_list = ""
            for child in children:
                if child == children.first():
                    children_list += child.first_name
                else:
                    children_list += f", " + child.first_name
            send_mail(
                "Regent Summer Camp Waitlist Update",
                f"Hello {family.primary_contact.first_name},\n\n"
                f"Space has opened up and {children_list} have been moved from the waitlist and registered for {camp.name} "
                f"running from {camp.start_date} to {camp.end_date}.\n"
                f"For more information, visit 127.0.0.1:8000/home",
                settings.EMAIL_HOST_USER,
                [waitlist_email]
            )

            # Email each child (if email is provided)
            for c in children:
                if c.email:
                    send_mail(
                        "Regent Summer Camp Registration Confirmation",
                        f"Hello {c.first_name},\n\n"
                        f"Your registration for the {camp.name} running from {camp.start_date} to {camp.end_date} "
                        f"has been confirmed.\n"
                        f"For more information, visit 127.0.0.1:8000/home",
                        settings.EMAIL_HOST_USER,
                        [c.email]
                    )

            entry.delete()
            print(f"Promoted {family} to {camp.name}")
        else:
            print(f"Skipped promotion: {family} has {child_count} children but only {available_spots} spots remain.")

@login_required
def remove_waitlist_entry(request, camp_id):
    user = request.user
    individual = Individual.objects.filter(user=user).first()
    family = Family.objects.filter(primary_contact=individual).first()

    if family:
        WaitingList.objects.filter(camp_id=camp_id, family=family).delete()
        print(f"Removed {family} from waitlist for camp ID {camp_id}")

    return redirect('users:account')