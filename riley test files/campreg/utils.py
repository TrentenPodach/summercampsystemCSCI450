from .models import WaitingList

def promote_next_waitlisted_family(camp):
    next_waitlisted = WaitingList.objects.filter(camp=camp).order_by('date_added').first()
    if next_waitlisted:
        # Promote to the camp
        camp.registered_families.add(next_waitlisted.family)
        next_waitlisted.delete()

        # Optional: Email them
        user_email = next_waitlisted.family.primary_contact.email
        if user_email:
            send_mail(
                "You're Off the Waitlist!",
                f"A spot has opened up in the {camp.name} camp and your registration is now confirmed!",
                settings.EMAIL_HOST_USER,
                [user_email]
            )