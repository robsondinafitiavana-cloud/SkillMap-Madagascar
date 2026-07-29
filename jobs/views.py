from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from companies.models import CompanyProfile
from students.models import StudentProfile
from notifications.utils import notify
from .models import Job
from .forms import JobForm


def job_list(request):
    """Liste des offres visibles par les étudiants, avec recherche multicritère."""
    qs = Job.objects.filter(is_active=True, deadline__gte=timezone.now().date()).select_related('company')

    q = request.GET.get('q', '').strip()
    contract_type = request.GET.get('contract_type', '').strip()
    city = request.GET.get('city', '').strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(required_skills__name__icontains=q)).distinct()
    if contract_type:
        qs = qs.filter(contract_type=contract_type)
    if city:
        qs = qs.filter(city__icontains=city)

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj, 'filters': {'q': q, 'contract_type': contract_type, 'city': city},
        'contract_choices': Job.CONTRACT_CHOICES,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    Job.objects.filter(pk=pk).update(views_count=job.views_count + 1)
    already_applied = False
    if request.user.is_authenticated and getattr(request.user, 'is_student', False):
        student = StudentProfile.objects.filter(user=request.user).first()
        if student:
            already_applied = job.applications.filter(student=student).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'already_applied': already_applied})


@login_required
def company_job_list(request):
    company = get_object_or_404(CompanyProfile, user=request.user)
    return render(request, 'jobs/company_job_list.html', {'jobs': company.jobs.all()})


@login_required
def job_create(request):
    company = get_object_or_404(CompanyProfile, user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            form.save_m2m()
            # Notifier les étudiants dont une compétence correspond à l'offre
            skill_ids = list(job.required_skills.values_list('id', flat=True))
            if skill_ids:
                matched_students = StudentProfile.objects.filter(
                    student_skills__skill_id__in=skill_ids
                ).distinct()
                for s in matched_students[:100]:
                    notify(s.user, 'NEW_JOB', f"Nouvelle offre correspondant à votre profil : {job.title}",
                           link=f"/offres/{job.pk}/")
            messages.success(request, "Offre publiée avec succès.")
            return redirect('jobs:company_job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Publier'})


@login_required
def job_edit(request, pk):
    company = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(Job, pk=pk, company=company)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Offre mise à jour.")
            return redirect('jobs:company_job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Modifier'})


@login_required
def job_delete(request, pk):
    company = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(Job, pk=pk, company=company)
    job.delete()
    messages.success(request, "Offre supprimée.")
    return redirect('jobs:company_job_list')
