from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from students.models import StudentProfile
from companies.models import CompanyProfile
from .forms import StudentRegisterForm, CompanyRegisterForm, SkillMapAuthenticationForm


class StudentRegisterView(CreateView):
    form_class = StudentRegisterForm
    template_name = 'accounts/register_student.html'
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        StudentProfile.objects.create(
            user=self.object,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            university=form.cleaned_data['university'],
            department=form.cleaned_data['department'],
        )
        login(self.request, self.object)
        return response


class CompanyRegisterView(CreateView):
    form_class = CompanyRegisterForm
    template_name = 'accounts/register_company.html'
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        CompanyProfile.objects.create(
            user=self.object,
            company_name=form.cleaned_data['company_name'],
            sector=form.cleaned_data['sector'],
        )
        login(self.request, self.object)
        return response


class SkillMapLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = SkillMapAuthenticationForm
    redirect_authenticated_user = True


class SkillMapLogoutView(LogoutView):
    next_page = 'accounts:login'


def choose_role(request):
    return render(request, 'accounts/choose_role.html')
