"""
Simulateur d'évolution : "et si j'apprenais ces compétences en plus (et/ou
réalisais un nouveau projet) ?"

Réutilise EXACTEMENT la même formule que le score d'employabilité affiché
partout ailleurs sur la plateforme (students.scoring.compute_score_from_counts)
— aucune donnée n'est modifiée en base, tout est calculé "à blanc" pour
l'aperçu, ce qui permet à l'étudiant d'essayer plusieurs scénarios sans
risque avant de décider quoi apprendre en premier.
"""
from students.scoring import compute_employability_score, compute_score_from_counts

# Niveau hypothétique attribué à une compétence que l'étudiant ne possède
# pas encore mais qu'il envisage d'apprendre : on suppose un niveau
# "Intermédiaire" (2/4), ni trop optimiste (Expert) ni trop pessimiste
# (Débutant), pour une estimation réaliste de la progression.
ASSUMED_LEVEL_FOR_NEW_SKILL = 2


def simulate_evolution(student, extra_skill_ids=None, add_project=False):
    """Retourne le score actuel et le score estimé après l'ajout
    hypothétique de compétences et/ou d'un nouveau projet."""
    extra_skill_ids = extra_skill_ids or []

    current_score = compute_employability_score(student)

    existing_skills = list(student.student_skills.all())
    existing_ids = {s.skill_id for s in existing_skills}
    # On ne recompte pas une compétence déjà possédée par l'étudiant.
    truly_new_ids = [sid for sid in extra_skill_ids if sid not in existing_ids]

    nb_skills = current_score['nb_skills'] + len(truly_new_ids)
    total_level = sum(s.level for s in existing_skills) + len(truly_new_ids) * ASSUMED_LEVEL_FOR_NEW_SKILL
    avg_level = total_level / nb_skills if nb_skills else 0

    nb_projects = current_score['nb_projects'] + (1 if add_project else 0)

    simulated_score = compute_score_from_counts(
        nb_skills=nb_skills,
        avg_level=avg_level,
        nb_projects=nb_projects,
        nb_certificates=current_score['nb_certificates'],
        nb_experiences=current_score['nb_experiences'],
    )

    return {
        'before': current_score['total'],
        'after': simulated_score['total'],
        'gain': round(simulated_score['total'] - current_score['total'], 1),
    }
