from django import forms
from .models import Individual, Family, User, Camp

class IndividualForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = Individual
        fields = ['first_name', 'last_name', 'date_of_birth', 'email']

class PrimaryContactForm(IndividualForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the email field required and customize the error message
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({
            'required': 'required',
            'oninvalid': "this.setCustomValidity('Please enter an email for the primary contact.')",
            'oninput': "this.setCustomValidity('')"
        })


class FamilyForm(forms.ModelForm):
    family_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Family
        # Don't show primary_contact or members in the form
        exclude = ['primary_contact', 'members']

class CampChoiceForm(forms.Form):
    camp = forms.ModelChoiceField(
        queryset=Camp.objects.all(),
        empty_label="Select a camp",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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
        
