from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'salary', 'contract_type',
            'required_skills', 'city', 'deadline', 'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'required_skills': forms.CheckboxSelectMultiple(),
        }
