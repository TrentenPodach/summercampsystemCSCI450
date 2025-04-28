from django import forms
from .models import Individual, Family, User

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ['first_name', 'last_name', 'date_of_birth', 'email']

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        # Don't show primary_contact or members in the form
        exclude = ['primary_contact', 'members']

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    #Password will show dots instead of characters
    class Meta:
        model = User
        fields = ['username']
        #constraints = [] #Skip the username uniqueness check
    #def clean_username(self):
        #Skip the username uniqueness check
        #return self.cleaned_data.get("username")
        
