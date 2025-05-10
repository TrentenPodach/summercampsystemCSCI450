from django import forms
from campreg.models import Camp, CampPost

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

class CampPostForm(forms.ModelForm):
    class Meta:
        model = CampPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your announcement...'}),
        }