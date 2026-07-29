"""
Vues du tableau de bord.

Chaque utilisateur a UN SEUL tableau de bord, mais son contenu change selon
son rôle (étudiant / entreprise / administrateur) : c'est la vue `home` qui
fait ce routage en regardant `request.user.role` (défini dans accounts.models.User),
puis délègue à la fonction correspondante.
"""
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from accounts.models import User
from applications.models import Application
from certificates.models import Certificate
from companies.models import CompanyProfile
from jobs.models import Job
from projects.models import Project
from students.models import StudentProfile
from students.scoring import compute_employability_score


def landing(request):
    if request.user.is_authenticated:
        return home(request)
    stats = {
        'nb_students': StudentProfile.objects.count(),
        'nb_companies': CompanyProfile.objects.count(),
        'nb_jobs': Job.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/landing.html', {'stats': stats})


@login_required
def home(request):
    user = request.user
    if user.is_student:
        return student_dashboard(request)
    if user.is_company:
        return company_dashboard(request)
    if user.is_admin_role or user.is_superuser:
        return admin_dashboard(request)
    return render(request, 'dashboard/no_role.html')


def student_dashboard(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    score = compute_employability_score(student)

    skills_by_category = {}
    for s in student.student_skills.select_related('skill'):
        cat = s.skill.get_category_display()
        skills_by_category[cat] = skills_by_category.get(cat, 0) + 1

    applications = student.applications.select_related('job').all()
    status_counts = {'PENDING': 0, 'ACCEPTED': 0, 'REJECTED': 0}
    for a in applications:
        status_counts[a.status] += 1

    context = {
        'student': student,
        'score': score,
        'score_remainder': round(100 - score['total'], 1),
        'nb_skills': student.student_skills.count(),
        'nb_projects': student.projects.count(),
        'nb_certificates': student.certificates.count(),
        'nb_applications': applications.count(),
        'recent_notifications': request.user.notifications.all()[:5],
        'skills_chart_labels': json.dumps(list(skills_by_category.keys())),
        'skills_chart_data': json.dumps(list(skills_by_category.values())),
        'status_chart_labels': json.dumps(['En attente', 'Acceptée', 'Refusée']),
        'status_chart_data': json.dumps([status_counts['PENDING'], status_counts['ACCEPTED'], status_counts['REJECTED']]),
    }
    return render(request, 'dashboard/student_dashboard.html', context)


def company_dashboard(request):
    company = get_object_or_404(CompanyProfile, user=request.user)
    jobs = company.jobs.all()
    applications = Application.objects.filter(job__company=company)

    status_counts = {'PENDING': 0, 'ACCEPTED': 0, 'REJECTED': 0}
    for a in applications:
        status_counts[a.status] += 1

    context = {
        'company': company,
        'nb_jobs': jobs.count(),
        'nb_active_jobs': jobs.filter(is_active=True).count(),
        'nb_applications': applications.count(),
        'nb_profiles_viewed': company.profiles_viewed_count,
        'recent_notifications': request.user.notifications.all()[:5],
        'recent_jobs': jobs[:5],
        'status_chart_labels': json.dumps(['En attente', 'Acceptée', 'Refusée']),
        'status_chart_data': json.dumps([status_counts['PENDING'], status_counts['ACCEPTED'], status_counts['REJECTED']]),
    }
    return render(request, 'dashboard/company_dashboard.html', context)


@login_required
def admin_dashboard(request):
    context = {
        'nb_users': User.objects.count(),
        'nb_students': User.objects.filter(role=User.Role.STUDENT).count(),
        'nb_companies_users': User.objects.filter(role=User.Role.COMPANY).count(),
        'nb_companies': CompanyProfile.objects.count(),
        'nb_jobs': Job.objects.count(),
        'nb_applications': Application.objects.count(),
        'nb_projects': Project.objects.count(),
        'nb_certificates': Certificate.objects.count(),
        'pending_validation': StudentProfile.objects.filter(user__is_validated=False).select_related('user')[:10],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def validate_profile(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    target.is_validated = True
    target.save(update_fields=['is_validated'])
    from notifications.utils import notify
    notify(target, 'PROFILE_VALIDATED', "Votre profil a été validé par l'administrateur.")
    from django.contrib import messages
    from django.shortcuts import redirect
    messages.success(request, f"Profil de {target.username} validé.")
    return redirect('dashboard:admin_dashboard')
