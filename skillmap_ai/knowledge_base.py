"""
Base de connaissances des métiers de l'informatique.

Chaque entrée décrit un métier avec ses compétences "obligatoires" et
"recommandées". Ces données sont utilisées par la commande
`seed_careers` pour peupler la base (voir management/commands/seed_careers.py) ;
elles ne sont donc lues qu'une seule fois, au moment du chargement initial.

Pour AJOUTER un métier : il suffit d'ajouter une entrée à la liste
CAREERS ci-dessous, puis de relancer `python manage.py seed_careers`.
Pas besoin de toucher au moteur de recommandation (engine.py) : il lit
les métiers directement depuis la base de données.

Les noms de compétences correspondent au référentiel partagé de
l'application (app skills) ; toute compétence qui n'existe pas encore y
est automatiquement créée par la commande de seed (comme pour le
référentiel ouvert aux étudiants/entreprises).
"""

CAREERS = [
    {
        'name': "Développeur Backend",
        'domain': "Développement",
        'description': "Conçoit et développe la partie serveur des applications web : logique métier, bases de données, API.",
        'recommended_level': "L3 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "700 000 - 1 500 000 Ar / mois",
        'growth_prospects': "Évolution possible vers Lead Backend ou Architecte logiciel.",
        'required': ["Python", "Django", "PostgreSQL"],
        'recommended': ["Git", "Docker", "Django REST Framework"],
    },
    {
        'name': "Développeur Frontend",
        'domain': "Développement",
        'description': "Construit les interfaces utilisateur avec lesquelles interagissent les visiteurs d'un site ou d'une application.",
        'recommended_level': "L2 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "600 000 - 1 300 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead Frontend ou Architecte UI.",
        'required': ["JavaScript", "HTML/CSS", "React"],
        'recommended': ["TypeScript", "Git", "Design UI/UX"],
    },
    {
        'name': "Développeur Full Stack",
        'domain': "Développement",
        'description': "Intervient à la fois sur la partie serveur et sur l'interface utilisateur d'une application.",
        'recommended_level': "L3 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "800 000 - 1 700 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead Développeur ou Architecte logiciel.",
        'required': ["Python", "Django", "JavaScript", "React"],
        'recommended': ["PostgreSQL", "Git", "Docker"],
    },
    {
        'name': "Data Analyst",
        'domain': "Données",
        'description': "Explore et analyse des données pour en tirer des indicateurs utiles à la prise de décision.",
        'recommended_level': "L3 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "700 000 - 1 400 000 Ar / mois",
        'growth_prospects': "Évolution vers Data Scientist ou Lead Data Analyst.",
        'required': ["Python", "SQL", "Excel avancé"],
        'recommended': ["Power BI", "Machine Learning", "Communication"],
    },
    {
        'name': "Data Scientist",
        'domain': "Données",
        'description': "Construit des modèles prédictifs et analyse des données complexes pour résoudre des problèmes métier.",
        'recommended_level': "M1 minimum",
        'desired_experience': "1 an d'expérience ou projets académiques solides",
        'average_salary': "900 000 - 2 000 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead Data Scientist ou Ingénieur IA.",
        'required': ["Python", "Machine Learning", "SQL"],
        'recommended': ["Deep Learning", "Intelligence Artificielle", "Power BI"],
    },
    {
        'name': "Ingénieur IA",
        'domain': "Données",
        'description': "Conçoit, entraîne et déploie des modèles d'intelligence artificielle en production.",
        'recommended_level': "M1 minimum",
        'desired_experience': "1 an d'expérience ou projets académiques solides",
        'average_salary': "1 000 000 - 2 200 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead AI Engineer ou Chercheur en IA.",
        'required': ["Python", "Intelligence Artificielle", "Machine Learning"],
        'recommended': ["Deep Learning", "Cloud (AWS/Azure)", "Git"],
    },
    {
        'name': "Administrateur Système",
        'domain': "Infrastructure",
        'description': "Installe, configure et maintient les serveurs et systèmes d'exploitation d'une organisation.",
        'recommended_level': "L2 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "600 000 - 1 300 000 Ar / mois",
        'growth_prospects': "Évolution vers Administrateur Systèmes Senior ou Responsable Infrastructure.",
        'required': ["Linux", "Windows Server", "Réseaux"],
        'recommended': ["Docker", "Sécurité des réseaux", "Cloud (AWS/Azure)"],
    },
    {
        'name': "Administrateur Réseau",
        'domain': "Infrastructure",
        'description': "Met en place et supervise l'infrastructure réseau (routeurs, switchs, pare-feux) d'une organisation.",
        'recommended_level': "L2 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "600 000 - 1 300 000 Ar / mois",
        'growth_prospects': "Évolution vers Ingénieur Réseau ou Responsable Infrastructure.",
        'required': ["Réseaux", "Administration réseau", "Sécurité des réseaux"],
        'recommended': ["Linux", "Cybersécurité", "Windows Server"],
    },
    {
        'name': "Expert Cybersécurité",
        'domain': "Sécurité",
        'description': "Protège les systèmes d'information contre les cyberattaques et audite leur niveau de sécurité.",
        'recommended_level': "L3 minimum",
        'desired_experience': "1 an d'expérience ou certifications reconnues",
        'average_salary': "900 000 - 2 000 000 Ar / mois",
        'growth_prospects': "Évolution vers Responsable Sécurité des Systèmes d'Information (RSSI).",
        'required': ["Cybersécurité", "Sécurité des réseaux", "Linux"],
        'recommended': ["Réseaux", "Python", "Administration réseau"],
    },
    {
        'name': "Développeur Mobile",
        'domain': "Développement",
        'description': "Développe des applications pour smartphones et tablettes (Android, iOS ou multiplateforme).",
        'recommended_level': "L3 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "700 000 - 1 500 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead Mobile ou Architecte Mobile.",
        'required': ["JavaScript", "React", "Git"],
        'recommended': ["Kotlin", "Swift", "Design UI/UX"],
    },
    {
        'name': "DevOps",
        'domain': "Infrastructure",
        'description': "Automatise le déploiement, l'intégration continue et l'exploitation des applications.",
        'recommended_level': "L3 minimum",
        'desired_experience': "1 an d'expérience ou projets académiques solides",
        'average_salary': "900 000 - 1 900 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead DevOps ou Architecte Cloud.",
        'required': ["Docker", "Linux", "Git"],
        'recommended': ["Kubernetes", "Cloud (AWS/Azure)", "Réseaux"],
    },
    {
        'name': "Chef de Projet Informatique",
        'domain': "Gestion",
        'description': "Planifie, coordonne et pilote un projet informatique de sa conception jusqu'à sa livraison.",
        'recommended_level': "L3 minimum",
        'desired_experience': "1 an d'expérience ou projets académiques solides",
        'average_salary': "800 000 - 1 800 000 Ar / mois",
        'growth_prospects': "Évolution vers Directeur de Projet ou Product Manager.",
        'required': ["Gestion de projet", "Communication", "Agile/Scrum"],
        'recommended': ["Git", "SQL", "Design UI/UX"],
    },
    {
        'name': "Testeur QA",
        'domain': "Qualité",
        'description': "Vérifie la qualité et le bon fonctionnement des logiciels avant leur mise en production.",
        'recommended_level': "L2 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "600 000 - 1 200 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead QA ou Ingénieur Automatisation de tests.",
        'required': ["Tests unitaires", "Python", "Git"],
        'recommended': ["Agile/Scrum", "SQL", "JavaScript"],
    },
    {
        'name': "UX/UI Designer",
        'domain': "Design",
        'description': "Conçoit des interfaces à la fois esthétiques et faciles à utiliser pour les utilisateurs finaux.",
        'recommended_level': "L2 minimum",
        'desired_experience': "Débutant accepté (stage / junior)",
        'average_salary': "600 000 - 1 300 000 Ar / mois",
        'growth_prospects': "Évolution vers Lead Designer ou Product Designer.",
        'required': ["Design UI/UX", "Figma", "Communication"],
        'recommended': ["HTML/CSS", "JavaScript", "Gestion de projet"],
    },
    {
        'name': "Ingénieur Cloud",
        'domain': "Infrastructure",
        'description': "Conçoit et administre les infrastructures hébergées sur des plateformes cloud (AWS, Azure, GCP).",
        'recommended_level': "L3 minimum",
        'desired_experience': "1 an d'expérience ou projets académiques solides",
        'average_salary': "900 000 - 2 000 000 Ar / mois",
        'growth_prospects': "Évolution vers Architecte Cloud ou Lead Cloud Engineer.",
        'required': ["Cloud (AWS/Azure)", "Linux", "Docker"],
        'recommended': ["Kubernetes", "Réseaux", "Python"],
    },
]

# Catégorie par défaut attribuée aux compétences non encore présentes dans
# le référentiel (voir seed_careers.py) — cohérent avec les catégories
# utilisées ailleurs dans l'application (app skills).
SKILL_CATEGORY_HINTS = {
    "HTML/CSS": "LANGAGE", "TypeScript": "LANGAGE", "SQL": "LANGAGE",
    "Kotlin": "LANGAGE", "Swift": "LANGAGE",
    "Django REST Framework": "FRAMEWORK",
    "Cloud (AWS/Azure)": "SYSTEME", "Kubernetes": "SYSTEME",
    "Excel avancé": "AUTRE", "Power BI": "AUTRE", "Communication": "AUTRE",
    "Agile/Scrum": "AUTRE", "Tests unitaires": "AUTRE",
}
