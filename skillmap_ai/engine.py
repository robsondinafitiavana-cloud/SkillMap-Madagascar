"""
Moteur de recommandation du Conseiller de carrière IA.

Ceci N'EST PAS un modèle de langage : c'est un système à base de règles,
volontairement transparent et explicable — chaque étape du calcul peut être
justifiée avec une formule simple, ce qui est un vrai atout pour la
présentation du projet (on peut montrer exactement "pourquoi" le système a
recommandé tel métier, contrairement à une boîte noire).

Principe : pour chaque métier de la base de connaissances, on compare
l'ensemble des compétences de l'étudiant à l'ensemble des compétences
associées au métier (obligatoires et recommandées), et on en déduit un
pourcentage de compatibilité.

    compatibilité = 0.7 × (part des compétences OBLIGATOIRES maîtrisées)
                   + 0.3 × (part des compétences RECOMMANDÉES maîtrisées)

Les compétences obligatoires pèsent plus lourd (70 %) que les recommandées
(30 %), car elles sont déterminantes pour exercer le métier.
"""
from .models import Career

REQUIRED_WEIGHT = 0.7
RECOMMENDED_WEIGHT = 0.3


def compute_career_matches(student):
    """Calcule la compatibilité de l'étudiant avec chaque métier de la base
    de connaissances, et retourne la liste triée du plus au moins pertinent.

    Chaque élément retourné est un dict avec :
        career, percent, matched_required, missing_required,
        matched_recommended, missing_recommended
    """
    student_skill_ids = set(student.student_skills.values_list('skill_id', flat=True))

    careers = Career.objects.prefetch_related('career_skills__skill').all()
    results = []

    for career in careers:
        required = career.required_skills()
        recommended = career.recommended_skills()

        matched_required = [s for s in required if s.id in student_skill_ids]
        missing_required = [s for s in required if s.id not in student_skill_ids]
        matched_recommended = [s for s in recommended if s.id in student_skill_ids]
        missing_recommended = [s for s in recommended if s.id not in student_skill_ids]

        required_ratio = len(matched_required) / len(required) if required else None
        recommended_ratio = len(matched_recommended) / len(recommended) if recommended else None

        # Si l'une des deux listes est vide (métier sans compétence
        # "recommandée" par exemple), on ne doit pas pénaliser le score en
        # laissant sa part à 0 : tout le poids se reporte sur l'autre liste.
        if required_ratio is None and recommended_ratio is None:
            percent = 0
        elif required_ratio is None:
            percent = round(recommended_ratio * 100)
        elif recommended_ratio is None:
            percent = round(required_ratio * 100)
        else:
            percent = round((required_ratio * REQUIRED_WEIGHT + recommended_ratio * RECOMMENDED_WEIGHT) * 100)

        results.append({
            'career': career,
            'percent': percent,
            'matched_required': matched_required,
            'missing_required': missing_required,
            'matched_recommended': matched_recommended,
            'missing_recommended': missing_recommended,
        })

    results.sort(key=lambda r: r['percent'], reverse=True)
    return results
