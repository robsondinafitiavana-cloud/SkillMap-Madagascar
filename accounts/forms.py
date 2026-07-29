from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, label="Prénom")
    last_name = forms.CharField(max_length=100, label="Nom")
    university = forms.CharField(max_length=150, initial="Inside University", label="Université")
    department = forms.CharField(max_length=150, label="Filière")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user


class CompanyRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=150, label="Nom de l'entreprise")
    sector = forms.CharField(max_length=150, required=False, label="Secteur d'activité")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.Role.COMPANY
        if commit:
            user.save()
        return user


class SkillMapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
