from django import forms
from campreg.models import Camp

class CampForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ['name', 'start_date', 'end_date', 'max_capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
