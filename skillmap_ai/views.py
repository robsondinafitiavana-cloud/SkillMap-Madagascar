"""
Vues du Conseiller de carrière IA.

    advisor        -> page principale : classement des métiers, explication,
                       radar de compétences, plan de progression
    simulate_api   -> endpoint JSON appelé par le bouton "Simuler mon
                       évolution" (rafraîchit le score sans recharger la page,
                       même principe que le polling de la messagerie)
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from skills.models import Skill
from students.models import StudentProfile

from .engine import compute_career_matches
from .explainer import generate_explanation
from .roadmap import build_roadmap
from .simulator import simulate_evolution


def _get_student_or_none(request):
    if not getattr(request.user, 'is_student', False):
        return None
    return StudentProfile.objects.filter(user=request.user).first()


@login_required
def advisor(request):
    student = _get_student_or_none(request)
    if student is None:
        return HttpResponseForbidden("Le conseiller de carrière est réservé aux étudiants.")

    matches = compute_career_matches(student)
    top_matches = matches[:5]
    other_matches = matches[5:]
    explanation = generate_explanation(matches)
    roadmap = build_roadmap(matches[0]) if matches else None

    # Radar de compétences : niveau moyen de l'étudiant par catégorie
    # (Langage, Framework, Réseaux...), sur une échelle de 0 à 4.
    student_skills = student.student_skills.select_related('skill').all()
    levels_by_category = {}
    for ss in student_skills:
        cat = ss.skill.get_category_display()
        levels_by_category.setdefault(cat, []).append(ss.level)
    radar_labels = list(levels_by_category.keys())
    radar_data = [round(sum(v) / len(v), 1) for v in levels_by_category.values()]

    # Liste des compétences manquantes pour le métier n°1, proposées comme
    # cases à cocher dans le panneau "Simuler mon évolution".
    simulable_skills = matches[0]['missing_required'] + matches[0]['missing_recommended'] if matches else []

    return render(request, 'skillmap_ai/advisor.html', {
        'student': student,
        'top_matches': top_matches,
        'other_matches': other_matches,
        'explanation': explanation,
        'roadmap': roadmap,
        'radar_labels': json.dumps(radar_labels),
        'radar_data': json.dumps(radar_data),
        'simulable_skills': simulable_skills,
    })


@login_required
@require_POST
def simulate_api(request):
    """Endpoint JSON : reçoit une liste d'IDs de compétences envisagées (et
    un booléen "nouveau projet"), retourne le score avant/après."""
    student = _get_student_or_none(request)
    if student is None:
        return HttpResponseForbidden()

    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Requête invalide.'}, status=400)

    skill_ids = [int(i) for i in payload.get('skill_ids', []) if str(i).isdigit()]
    add_project = bool(payload.get('add_project', False))

    # On vérifie que les IDs envoyés correspondent bien à des compétences
    # existantes, pour éviter de calculer avec des identifiants farfelus.
    valid_ids = set(Skill.objects.filter(id__in=skill_ids).values_list('id', flat=True))

    result = simulate_evolution(student, extra_skill_ids=list(valid_ids), add_project=add_project)
    return JsonResponse(result)
