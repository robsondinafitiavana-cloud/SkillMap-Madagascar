"""
Génération d'explications en langage naturel — par gabarits (templates),
PAS par un modèle de langage entraîné sur Internet.

C'est une technique classique appelée "génération de texte à base de
règles" (rule-based NLG) : on assemble des phrases à partir de morceaux de
texte pré-rédigés, remplis avec les données calculées par le moteur de
recommandation (engine.py). Le résultat est déterministe (la même entrée
donne toujours la même explication), rapide, et 100 % local.

C'est ce composant qui joue le rôle du "modèle d'IA local chargé de
produire des explications naturelles" : il ne s'agit pas d'un réseau de
neurones, mais d'un système symbolique — une approche d'IA tout aussi
légitime et beaucoup plus simple à expliquer et à garantir fiable.
"""


def _join_names(skills, max_items=3):
    names = [s.name for s in skills[:max_items]]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} et {names[1]}"
    return ", ".join(names[:-1]) + f" et {names[-1]}"


def generate_explanation(matches):
    """Construit un texte de synthèse à partir du classement des métiers
    (résultat de engine.compute_career_matches)."""
    if not matches or matches[0]['percent'] == 0:
        return (
            "Nous n'avons pas encore assez d'informations sur vos compétences "
            "pour vous proposer des recommandations fiables. Ajoutez vos "
            "compétences dans votre profil pour débloquer le conseiller de carrière."
        )

    top = matches[0]
    sentences = [
        f"Votre profil correspond à {top['percent']} % au métier de {top['career'].name}."
    ]

    if top['matched_required']:
        sentences.append(
            f"Vos compétences en {_join_names(top['matched_required'])} sont des points forts pour ce métier."
        )

    missing = top['missing_required'] + top['missing_recommended']
    if missing:
        sentences.append(
            f"Pour améliorer vos chances, nous vous recommandons d'apprendre {_join_names(missing)}."
        )
    else:
        sentences.append("Vous maîtrisez déjà l'ensemble des compétences clés de ce métier, félicitations !")

    # Métiers alternatifs : les 2 suivants, s'ils restent raisonnablement pertinents.
    alternatives = [m for m in matches[1:3] if m['percent'] >= 30]
    if alternatives:
        alt_text = " et ".join(f"{m['career'].name} ({m['percent']} %)" for m in alternatives)
        sentences.append(f"Votre profil est également compatible avec {alt_text}.")

    return " ".join(sentences)
