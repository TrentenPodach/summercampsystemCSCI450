from django.contrib import admin
from .models import Individual, Family, Account, Camp, WaitingList, MailingList

admin.site.register(Individual)
admin.site.register(Family)
admin.site.register(Account)
admin.site.register(Camp)
admin.site.register(WaitingList)
admin.site.register(MailingList)