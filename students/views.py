from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import StudentProfile, Experience
from .forms import StudentProfileForm, ExperienceForm
from .scoring import compute_employability_score
from .cv_pdf import generate_cv_pdf


def _get_student(request):
    return get_object_or_404(StudentProfile, user=request.user)


def leaderboard(request):
    """Classement public des étudiants selon leur score d'employabilité.

    Seuls les profils publics sont pris en compte (comme pour l'annuaire),
    et on précharge (prefetch_related) toutes les relations utilisées par
    compute_employability_score pour éviter des centaines de petites
    requêtes SQL (1 requête par relation au lieu d'1 par étudiant).
    """
    students = StudentProfile.objects.filter(portfolio_public=True).prefetch_related(
        'student_skills', 'projects', 'certificates', 'experiences',
    )

    ranked = [(student, compute_employability_score(student)) for student in students]
    ranked.sort(key=lambda pair: pair[1]['total'], reverse=True)

    paginator = Paginator(ranked, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'students/leaderboard.html', {'page_obj': page_obj})


def student_directory(request):
    """Annuaire public des étudiants : accessible à tous (recruteurs comme
    simples visiteurs), sans avoir besoin d'être connecté. Seuls les profils
    dont l'étudiant a activé "portfolio public" apparaissent ici.
    """
    students = StudentProfile.objects.filter(portfolio_public=True).order_by('-created_at')

    q = request.GET.get('q', '').strip()
    if q:
        students = students.filter(department__icontains=q) | students.filter(university__icontains=q)

    # Pagination : 12 profils par page pour rester léger, même avec une
    # base de plusieurs centaines d'étudiants.
    paginator = Paginator(students, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'students/student_directory.html', {
        'page_obj': page_obj, 'q': q,
    })


@login_required
def profile_view(request):
    """Page 'Mon profil', dans l'esprit d'un profil Facebook/Instagram :
    bannière, avatar, statistiques en un coup d'œil, puis les sections
    (compétences, projets, certificats, expériences) avec un accès rapide
    à leur gestion. Un bouton permet de voir exactement ce qu'une entreprise
    voit (le portfolio public), et un autre d'ouvrir le formulaire d'édition.
    """
    student = _get_student(request)
    score = compute_employability_score(student)
    return render(request, 'students/profile_view.html', {
        'student': student,
        'score': score,
        'nb_skills': student.student_skills.count(),
        'nb_projects': student.projects.count(),
        'nb_certificates': student.certificates.count(),
        'nb_experiences': student.experiences.count(),
    })


@login_required
def profile_edit(request):
    student = _get_student(request)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            # Comme sur Facebook : après modification, on revient sur la
            # page de profil plutôt que de rester sur le formulaire.
            return redirect('students:profile_view')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'students/profile_edit.html', {'form': form, 'student': student})


@login_required
def experience_list(request):
    student = _get_student(request)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.student = student
            exp.save()
            messages.success(request, "Expérience ajoutée.")
            return redirect('students:experience_list')
    else:
        form = ExperienceForm()
    return render(request, 'students/experience_list.html', {
        'form': form, 'experiences': student.experiences.all(),
    })


@login_required
def experience_delete(request, pk):
    student = _get_student(request)
    exp = get_object_or_404(Experience, pk=pk, student=student)
    exp.delete()
    messages.success(request, "Expérience supprimée.")
    return redirect('students:experience_list')


def portfolio_public(request, slug):
    student = get_object_or_404(StudentProfile, slug=slug)
    # Un visiteur externe ne voit le portfolio que s'il est public ; le
    # propriétaire, lui, peut toujours prévisualiser SON PROPRE profil,
    # même s'il n'a pas encore activé "portfolio public" (utile pour
    # vérifier le rendu avant de le rendre visible aux entreprises).
    is_owner = request.user.is_authenticated and request.user == student.user
    if not student.portfolio_public and not is_owner:
        raise Http404("Ce portfolio n'est pas public.")
    score = compute_employability_score(student)
    return render(request, 'students/portfolio_public.html', {
        'student': student, 'score': score, 'is_owner': is_owner,
    })


@login_required
def download_cv(request):
    student = _get_student(request)
    buffer = generate_cv_pdf(student)
    filename = f"CV_{student.first_name}_{student.last_name}.pdf".replace(' ', '_')
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
