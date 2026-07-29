from django import forms
from .models import StudentProfile, Experience


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'photo', 'first_name', 'last_name', 'phone', 'address', 'city',
            'university', 'department', 'level', 'bio', 'linkedin_url',
            'github_url', 'portfolio_public',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'organization', 'description', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
