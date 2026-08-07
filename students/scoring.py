"""
Calcul du score d'employabilité SkillMap Madagascar.

Pondération :
    - Compétences   : 40 %
    - Projets       : 25 %
    - Certificats   : 20 %
    - Expériences   : 15 %

Chaque catégorie est plafonnée à un nombre de référence ("cible") au-delà
duquel elle est considérée comme complète (100 % de la sous-note), afin
d'éviter qu'un profil avec 50 compétences n'écrase artificiellement les
autres critères.

La logique de calcul pure (compute_score_from_counts) est séparée de la
lecture des données en base (compute_employability_score) : cela permet de
réutiliser exactement la même formule ailleurs — notamment dans le module
skillmap_ai pour simuler "et si j'apprenais telle compétence en plus ?"
sans dupliquer les règles de calcul ni toucher à la base de données.
"""

# Cibles utilisées pour ramener chaque catégorie à une note sur 100
TARGET_SKILLS = 8          # 8 compétences déclarées = sous-note pleine
TARGET_SKILL_LEVEL_BONUS = 4  # niveau moyen max (Débutant=1 ... Expert=4)
TARGET_PROJECTS = 5
TARGET_CERTIFICATES = 5
TARGET_EXPERIENCES = 3

WEIGHT_SKILLS = 0.40
WEIGHT_PROJECTS = 0.25
WEIGHT_CERTIFICATES = 0.20
WEIGHT_EXPERIENCES = 0.15


def _capped_ratio(count, target):
    if target <= 0:
        return 0
    return min(count / target, 1.0)


def compute_score_from_counts(nb_skills, avg_level, nb_projects, nb_certificates, nb_experiences):
    """Applique la formule du score d'employabilité à des chiffres déjà
    connus (plutôt qu'à un objet StudentProfile). C'est cette fonction que
    réutilise le simulateur d'évolution du conseiller de carrière IA."""
    skills_count_ratio = _capped_ratio(nb_skills, TARGET_SKILLS)
    skills_level_ratio = _capped_ratio(avg_level, TARGET_SKILL_LEVEL_BONUS)
    skills_subscore = (0.7 * skills_count_ratio + 0.3 * skills_level_ratio) * 100

    projects_subscore = _capped_ratio(nb_projects, TARGET_PROJECTS) * 100
    certificates_subscore = _capped_ratio(nb_certificates, TARGET_CERTIFICATES) * 100
    experiences_subscore = _capped_ratio(nb_experiences, TARGET_EXPERIENCES) * 100

    total = (
        skills_subscore * WEIGHT_SKILLS
        + projects_subscore * WEIGHT_PROJECTS
        + certificates_subscore * WEIGHT_CERTIFICATES
        + experiences_subscore * WEIGHT_EXPERIENCES
    )

    return {
        'total': round(total, 1),
        'skills_subscore': round(skills_subscore, 1),
        'projects_subscore': round(projects_subscore, 1),
        'certificates_subscore': round(certificates_subscore, 1),
        'experiences_subscore': round(experiences_subscore, 1),
        'nb_skills': nb_skills,
        'nb_projects': nb_projects,
        'nb_certificates': nb_certificates,
        'nb_experiences': nb_experiences,
    }


def compute_employability_score(student):
    """Retourne un dict avec le score global (/100) et le détail par catégorie."""
    student_skills = list(student.student_skills.all())
    nb_skills = len(student_skills)
    avg_level = (
        sum(s.level for s in student_skills) / nb_skills if nb_skills else 0
    )
    return compute_score_from_counts(
        nb_skills=nb_skills,
        avg_level=avg_level,
        nb_projects=student.projects.count(),
        nb_certificates=student.certificates.count(),
        nb_experiences=student.experiences.count(),
    )
