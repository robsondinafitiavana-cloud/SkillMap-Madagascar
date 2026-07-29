from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from students.models import StudentProfile
from .models import Certificate
from .forms import CertificateForm


@login_required
def certificate_list(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'certificates/certificate_list.html', {'certificates': student.certificates.all()})


@login_required
def certificate_create(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.student = student
            cert.save()
            messages.success(request, "Certificat ajouté.")
            return redirect('certificates:certificate_list')
    else:
        form = CertificateForm()
    return render(request, 'certificates/certificate_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def certificate_delete(request, pk):
    student = get_object_or_404(StudentProfile, user=request.user)
    cert = get_object_or_404(Certificate, pk=pk, student=student)
    cert.delete()
    messages.success(request, "Certificat supprimé.")
    return redirect('certificates:certificate_list')
