from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from campreg.models import Camp, Family, WaitingList
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import CampForm, CampPostForm, CampPost
from django.core.mail import send_mail
from django.conf import settings



# Step 5: Custom check to allow only staff
def is_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def dashboard(request):
    active_camps = Camp.objects.filter(archived=False)
    archived_camps = Camp.objects.filter(archived=True)

    for camp_list in (active_camps, archived_camps):
        for camp in camp_list:
            enrolled = sum(
                f.members.exclude(id=f.primary_contact.id).count()
                for f in camp.registered_families.all()
            )
            camp.enrolled_children = enrolled

            waitlisted = sum(
                entry.family.members.exclude(id=entry.family.primary_contact.id).count()
                for entry in WaitingList.objects.filter(camp=camp)
            )
            camp.waitlisted_children = waitlisted
            camp.available_spots = max(0, camp.max_capacity - enrolled)

    return render(request, 'staff/dashboard.html', {
        'active_camps': active_camps,
        'archived_camps': archived_camps,
        'total_families': Family.objects.count(),
        'total_waitlisted': WaitingList.objects.count()
    })

@user_passes_test(is_staff)
def view_camp(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    families = camp.registered_families.all()
    waitlisted = WaitingList.objects.filter(camp=camp).order_by('date_added')

    # Add `.children` to each registered family
    for family in families:
        family.children = family.members.exclude(id=family.primary_contact.id)

    # Add `.children` and `.child_count` to each waitlist entry
    for entry in waitlisted:
        children = entry.family.members.exclude(id=entry.family.primary_contact.id)
        entry.children = children
        entry.child_count = children.count()

    total_children = sum(family.children.count() for family in families)
    post_form = CampPostForm()

    return render(request, 'staff/camp_overview.html', {
        'camp': camp,
        'families': families,
        'waitlisted': waitlisted,
        'post_form': post_form
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

@user_passes_test(is_staff)
def remove_family_from_camp(request, camp_id, family_id):
    camp = get_object_or_404(Camp, id=camp_id)
    family = get_object_or_404(Family, id=family_id)

    if request.method == 'POST' and family in camp.registered_families.all():
        camp.registered_families.remove(family)

        for member in family.members.exclude(id=family.primary_contact.id):
            family.members.remove(member)
            member.delete()

    return redirect('staff:camp_overview', camp_id=camp.id)

@user_passes_test(is_staff)
def archive_camp(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)

    if request.method == 'POST':
        camp.archived = True
        camp.save()
    
    return redirect('staff:camp_overview', camp_id=camp.id)

@user_passes_test(is_staff)
def unarchive_camp(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)

    if request.method == 'POST':
        camp.archived = False
        camp.save()
    
    return redirect('staff:camp_overview', camp_id=camp.id)

@user_passes_test(is_staff)
def create_camp(request):
    if request.method == 'POST':
        camp_form = CampForm(request.POST)
        post_form = CampPostForm(request.POST)

        if camp_form.is_valid() and post_form.is_valid():
            camp = camp_form.save(commit=False)
            for fam in Family.objects.all():
                update_user = fam.primary_contact
                user_email = update_user.email
                send_mail("Regent Summer Camp Registration Confirmation",f"Hello {update_user.first_name},\n\nA new camp, {camp.name}, has been created.\nFor more information or to register, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[user_email])
            camp.save()

            # Save post only if title or content provided
            if post_form.cleaned_data['title'] or post_form.cleaned_data['content']:
                post = post_form.save(commit=False)
                post.camp = camp
                post.save()

            return redirect('staff:dashboard')
    else:
        camp_form = CampForm()
        post_form = CampPostForm()

    return render(request, 'staff/create_camp.html', {
        'camp_form': camp_form,
        'post_form': post_form
    })

@user_passes_test(is_staff)
def add_camp_post(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)

    if request.method == 'POST':
        form = CampPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.camp = camp

            for fam in Family.objects.all():
                update_user = fam.primary_contact
                user_email = update_user.email
                send_mail("Regent Summer Camp Registration Confirmation",f"Hello {update_user.first_name},\n\nA new post, {post.title}, has been created.\nFor more information or to see the post, visit 127.0.0.1:8000/home", settings.EMAIL_HOST_USER,[user_email])

            post.save()
            return redirect('staff:camp_overview', camp_id=camp.id)
    else:
        form = CampPostForm()

    return render(request, 'staff/add_post.html', {'form': form, 'camp': camp})

@user_passes_test(lambda u: u.is_staff)
def delete_camp_post(request, post_id):
    post = get_object_or_404(CampPost, id=post_id)
    camp_id = post.camp.id

    if request.method == 'POST':
        post.delete()
        return redirect('home')  # or redirect to camp_overview if needed

    return redirect('home')