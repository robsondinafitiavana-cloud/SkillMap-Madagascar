from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from students.models import StudentProfile
from students.scoring import compute_employability_score
from .models import CompanyProfile
from .forms import CompanyProfileForm


def _get_company(request):
    return get_object_or_404(CompanyProfile, user=request.user)


@login_required
def profile_edit(request):
    company = _get_company(request)
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil entreprise mis à jour.")
            return redirect('companies:profile_edit')
    else:
        form = CompanyProfileForm(instance=company)
    return render(request, 'companies/profile_edit.html', {'form': form, 'company': company})


def company_directory(request):
    """Annuaire public des entreprises partenaires : consultable par tout le
    monde (étudiants comme simples visiteurs), sans connexion nécessaire.
    """
    companies = CompanyProfile.objects.all().order_by('company_name')

    q = request.GET.get('q', '').strip()
    if q:
        companies = companies.filter(company_name__icontains=q) | companies.filter(sector__icontains=q)

    paginator = Paginator(companies, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'companies/company_directory.html', {
        'page_obj': page_obj, 'q': q,
    })


def company_public_detail(request, pk):
    """Fiche publique d'une entreprise (visible par les étudiants et le
    grand public) : présentation + liste de ses offres actives.
    """
    company = get_object_or_404(CompanyProfile, pk=pk)
    active_jobs = company.jobs.filter(is_active=True)
    return render(request, 'companies/company_public_detail.html', {
        'company': company, 'active_jobs': active_jobs,
    })


@login_required
def search_candidates(request):
    """Recherche intelligente réservée aux entreprises : compétence,
    université, ville, filière, niveau, avec classement automatique par
    pertinence (score d'employabilité) et pagination.
    """
    qs = StudentProfile.objects.all()

    q_skill = request.GET.get('skill', '').strip()
    q_university = request.GET.get('university', '').strip()
    q_city = request.GET.get('city', '').strip()
    q_department = request.GET.get('department', '').strip()
    q_level = request.GET.get('level', '').strip()

    if q_skill:
        qs = qs.filter(student_skills__skill__name__icontains=q_skill).distinct()
    if q_university:
        qs = qs.filter(university__icontains=q_university)
    if q_city:
        qs = qs.filter(city__icontains=q_city)
    if q_department:
        qs = qs.filter(department__icontains=q_department)
    if q_level:
        qs = qs.filter(level=q_level)

    # On calcule le score de chaque candidat pour les classer par pertinence.
    # (Fait en Python après la requête SQL car le score dépend de plusieurs
    # tables liées ; acceptable pour le volume d'une plateforme académique.)
    results = [(student, compute_employability_score(student)) for student in qs]
    results.sort(key=lambda pair: pair[1]['total'], reverse=True)

    paginator = Paginator(results, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'companies/search_candidates.html', {
        'page_obj': page_obj,
        'filters': {
            'skill': q_skill, 'university': q_university, 'city': q_city,
            'department': q_department, 'level': q_level,
        },
        'level_choices': StudentProfile.LEVEL_CHOICES,
    })


@login_required
def candidate_detail(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    score = compute_employability_score(student)
    company = CompanyProfile.objects.filter(user=request.user).first()
    if company:
        CompanyProfile.objects.filter(pk=company.pk).update(
            profiles_viewed_count=company.profiles_viewed_count + 1
        )
    return render(request, 'companies/candidate_detail.html', {'student': student, 'score': score})
