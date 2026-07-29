from django import forms
from .models import Certificate


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'organization', 'issue_date', 'file', 'image']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
        }
