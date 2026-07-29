from django import forms
from .models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['logo', 'company_name', 'sector', 'address', 'city', 'phone', 'website', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
