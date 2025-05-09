from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from campreg.models import Camp, Family, WaitingList
from django.shortcuts import get_object_or_404


# Step 5: Custom check to allow only staff
def is_staff(user):
    return user.is_authenticated and user.is_staff

# Staff-only dashboard view
@user_passes_test(is_staff)
def dashboard(request):
    camps = Camp.objects.all()
    total_families = Family.objects.count()
    total_waitlisted = WaitingList.objects.count()

    for camp in camps:
        enrolled = 0
        for family in camp.registered_families.all():
            enrolled += family.members.exclude(id=family.primary_contact.id).count()
        camp.enrolled_children = enrolled

        # Count all waitlisted children
        waitlisted = 0
        for entry in WaitingList.objects.filter(camp=camp):
            waitlisted += entry.family.members.exclude(id=entry.family.primary_contact.id).count()
        camp.waitlisted_children = waitlisted

        camp.available_spots = max(0, camp.max_capacity - camp.enrolled_children)

    return render(request, 'staff/dashboard.html', {
        'camps': camps,
        'total_families': total_families,
        'total_waitlisted': total_waitlisted
    })

@user_passes_test(is_staff)
def view_camp(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    families = camp.registered_families.all()
    waitlisted = WaitingList.objects.filter(camp=camp).order_by('date_added')

    # Add `.children` to each family
    for family in families:
        family.children = family.members.exclude(id=family.primary_contact.id)

    for entry in waitlisted:
        entry.children = entry.family.members.exclude(id=entry.family.primary_contact.id)

    return render(request, 'staff/camp_overview.html', {
        'camp': camp,
        'families': families,
        'waitlisted': waitlisted,
    })


@user_passes_test(is_staff)
def promote_waitlist(request, camp_id, family_id):
    camp = get_object_or_404(Camp, id=camp_id)
    family = get_object_or_404(Family, id=family_id)

    # Check if the family is on the waitlist
    entry = WaitingList.objects.filter(camp=camp, family=family).first()
    if entry:
        # Remove from waitlist and add to camp
        entry.delete()
        camp.registered_families.add(family)

    return redirect('staff:camp_overview', camp_id=camp.id)

@user_passes_test(is_staff)
def remove_waitlist(request, camp_id, family_id):
    camp = get_object_or_404(Camp, id=camp_id)
    family = get_object_or_404(Family, id=family_id)

    # Just remove from waitlist
    WaitingList.objects.filter(camp=camp, family=family).delete()

    return redirect('staff:camp_overview', camp_id=camp.id)
