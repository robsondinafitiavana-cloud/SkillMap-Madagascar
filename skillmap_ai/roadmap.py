"""
Construction du plan de progression ("roadmap") vers le métier le plus
compatible : on regroupe les compétences manquantes par étapes de 2, en
donnant la priorité aux compétences OBLIGATOIRES avant les recommandées
(logique simple mais efficace : d'abord ce qui est indispensable).
"""

SKILLS_PER_STEP = 2


def build_roadmap(match):
    """À partir d'un résultat de engine.compute_career_matches (un seul
    métier), retourne la liste ordonnée des étapes d'apprentissage."""
    ordered_missing = match['missing_required'] + match['missing_recommended']

    steps = []
    for i in range(0, len(ordered_missing), SKILLS_PER_STEP):
        chunk = ordered_missing[i:i + SKILLS_PER_STEP]
        steps.append({
            'step_number': len(steps) + 1,
            'skills': chunk,
        })

    return {
        'target_career': match['career'],
        'steps': steps,
        'already_ready': len(ordered_missing) == 0,
    }
