from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from students.models import StudentProfile
from .models import Skill, StudentSkill
from .forms import StudentSkillForm, SkillCreateForm


@login_required
def skill_list(request):
    """Page 'Mes compétences' de l'étudiant : ajouter/mettre à jour une
    compétence choisie dans le référentiel, avec son niveau."""
    student = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = StudentSkillForm(request.POST)
        if form.is_valid():
            # update_or_create : si la compétence est déjà présente, on met
            # juste à jour le niveau au lieu de créer un doublon.
            StudentSkill.objects.update_or_create(
                student=student, skill=form.cleaned_data['skill'],
                defaults={'level': form.cleaned_data['level']},
            )
            messages.success(request, "Compétence enregistrée.")
            return redirect('skills:skill_list')
    else:
        form = StudentSkillForm()
    return render(request, 'skills/skill_list.html', {
        'form': form, 'student_skills': student.student_skills.select_related('skill').all(),
    })


@login_required
def skill_delete(request, pk):
    student = get_object_or_404(StudentProfile, user=request.user)
    obj = get_object_or_404(StudentSkill, pk=pk, student=student)
    obj.delete()
    messages.success(request, "Compétence supprimée.")
    return redirect('skills:skill_list')


@login_required
def skill_catalog(request):
    """Référentiel global des compétences, ouvert à TOUS les utilisateurs
    connectés (étudiants ET entreprises).

    Si une compétence n'existe pas encore (ex. un nouvel outil, un nouveau
    langage), n'importe quel utilisateur peut l'ajouter ici : elle devient
    alors immédiatement disponible pour les étudiants (dans "Mes compétences")
    et pour les entreprises (dans les compétences requises d'une offre).
    """
    if request.method == 'POST':
        form = SkillCreateForm(request.POST)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f"Compétence « {skill.name} » ajoutée au référentiel.")
            return redirect('skills:skill_catalog')
    else:
        form = SkillCreateForm()

    skills_by_category = {}
    for skill in Skill.objects.all():
        skills_by_category.setdefault(skill.get_category_display(), []).append(skill)

    return render(request, 'skills/skill_catalog.html', {
        'form': form, 'skills_by_category': skills_by_category,
    })
