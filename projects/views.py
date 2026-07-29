from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from students.models import StudentProfile
from .models import Project
from .forms import ProjectForm


@login_required
def project_list(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'projects/project_list.html', {'projects': student.projects.all()})


@login_required
def project_create(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = student
            project.save()
            messages.success(request, "Projet ajouté.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def project_edit(request, pk):
    student = get_object_or_404(StudentProfile, user=request.user)
    project = get_object_or_404(Project, pk=pk, student=student)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet mis à jour.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'action': 'Modifier'})


@login_required
def project_delete(request, pk):
    student = get_object_or_404(StudentProfile, user=request.user)
    project = get_object_or_404(Project, pk=pk, student=student)
    project.delete()
    messages.success(request, "Projet supprimé.")
    return redirect('projects:project_list')
