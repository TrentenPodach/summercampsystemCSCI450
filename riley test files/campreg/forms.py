from django import forms
from .models import Individual, Family

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ['first_name', 'last_name', 'date_of_birth', 'email']

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        # Don't show primary_contact or members in the form
        exclude = ['primary_contact', 'members']
