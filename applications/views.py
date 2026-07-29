from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from companies.models import CompanyProfile
from jobs.models import Job
from students.models import StudentProfile
from notifications.utils import notify
from .models import Application
from .forms import ApplicationForm


@login_required
def apply_to_job(request, job_pk):
    student = get_object_or_404(StudentProfile, user=request.user)
    job = get_object_or_404(Job, pk=job_pk)

    if Application.objects.filter(student=student, job=job).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect('jobs:job_detail', pk=job.pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.job = job
            application.save()
            notify(
                job.company.user, 'NEW_APPLICATION',
                f"{student.full_name} a postulé à l'offre « {job.title} »",
                link=f"/candidatures/entreprise/{job.pk}/",
            )
            messages.success(request, "Candidature envoyée avec succès.")
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = ApplicationForm()
    return render(request, 'applications/apply_form.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'applications/my_applications.html', {
        'applications': student.applications.select_related('job', 'job__company').all(),
    })


@login_required
def job_applications(request, job_pk):
    company = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(Job, pk=job_pk, company=company)
    return render(request, 'applications/job_applications.html', {
        'job': job, 'applications': job.applications.select_related('student').all(),
    })


@login_required
def update_application_status(request, pk, new_status):
    company = get_object_or_404(CompanyProfile, user=request.user)
    application = get_object_or_404(Application, pk=pk, job__company=company)
    if new_status in dict(Application.STATUS_CHOICES):
        application.status = new_status
        application.save()
        notify(
            application.student.user, 'APPLICATION_STATUS',
            f"Votre candidature pour « {application.job.title} » est maintenant : {application.get_status_display()}",
            link='/candidatures/mes-candidatures/',
        )
        messages.success(request, "Statut de la candidature mis à jour.")
    return redirect('applications:job_applications', job_pk=application.job.pk)
