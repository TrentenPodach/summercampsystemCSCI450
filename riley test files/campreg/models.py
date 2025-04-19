from django.db import models
from django.contrib.auth.models import User

class Individual(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Family(models.Model):
    family_name = models.CharField(max_length=100)
    primary_contact = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name='primary_for_family')
    members = models.ManyToManyField(Individual, related_name='families')

    def __str__(self):
        return self.family_name

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.OneToOneField(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Camp(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    max_capacity = models.IntegerField()
    registered_families = models.ManyToManyField(Family, blank=True)

    def __str__(self):
        return self.name

class WaitingList(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.family} - {self.camp}"

class MailingList(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email