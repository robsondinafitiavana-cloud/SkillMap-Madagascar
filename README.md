# SkillMap Madagascar 🇲🇬

Plateforme de cartographie des compétences connectant étudiants, jeunes diplômés
et entreprises à Madagascar. Projet réalisé dans le cadre d'une soutenance de
Licence en Informatique.

## Stack technique

- **Backend** : Django 5, Python 3, PostgreSQL
- **Frontend** : Django Templates + Tailwind CSS (CDN)
- **Bibliothèques** : Django Authentication, ReportLab (génération de CV PDF),
  Chart.js (statistiques), Pillow (images)

## Fonctionnalités implémentées

- Authentification par rôle (Étudiant / Entreprise / Administrateur), inscription,
  connexion, déconnexion, réinitialisation de mot de passe
- Profil étudiant complet (photo, bio, université, filière, niveau, réseaux)
- Gestion des compétences (catégorie + niveau), projets, certificats, expériences
- Génération automatique du CV en PDF (ReportLab, palette Madagascar)
- Portfolio public partageable par lien
- Profil entreprise, publication d'offres (stage / emploi / freelance)
- Candidatures avec statuts (en attente / acceptée / refusée)
- Recherche intelligente de candidats (compétence, université, ville, filière,
  niveau) avec classement automatique par score de pertinence
- Score d'employabilité calculé automatiquement (compétences 40 %, projets 25 %,
  certificats 20 %, expériences 15 %)
- Notifications (nouvelle offre, nouvelle candidature, profil validé, statut mis à jour)
- Tableaux de bord dédiés (étudiant, entreprise, administrateur) avec graphiques Chart.js
- Validation des profils étudiants par l'administrateur
- Interface responsive, palette inspirée du drapeau malgache (rouge / vert / blanc)

## Installation

### 1. Cloner et créer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurer l'environnement

```bash
cp .env.example .env
```

Éditez `.env` :
- Pour démarrer **rapidement sans installer PostgreSQL** (développement/démo) :
  laissez `DB_ENGINE=sqlite`.
- Pour la configuration **officielle du cahier des charges (PostgreSQL)** :
  mettez `DB_ENGINE=postgresql` et renseignez `DB_NAME`, `DB_USER`,
  `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (créez au préalable la base et
  l'utilisateur PostgreSQL correspondants).

### 3. Migrations et données de départ

```bash
python manage.py migrate
python manage.py seed_skills        # crée le référentiel de compétences
python manage.py createsuperuser    # compte administrateur
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

Rendez-vous sur http://127.0.0.1:8000/

## Structure du projet

```
skillmap/           configuration du projet (settings, urls)
accounts/           authentification, rôles utilisateur
students/           profil étudiant, expériences, CV PDF, portfolio public
companies/          profil entreprise, recherche de candidats
skills/             référentiel de compétences + compétences de l'étudiant
projects/           projets étudiants
certificates/       certificats étudiants
jobs/                offres d'emploi
applications/       candidatures
dashboard/          tableaux de bord par rôle
notifications/      notifications utilisateur
templates/          gabarits HTML (Tailwind CSS)
static/ media/      fichiers statiques et fichiers uploadés
```

## Notes pour la soutenance

- Le score d'employabilité est calculé dans `students/scoring.py` — la logique
  et les pondérations y sont commentées.
- Le CV PDF est généré dans `students/cv_pdf.py` avec ReportLab.
- Les 10 apps Django suivent l'architecture demandée dans le cahier des charges.
- Le modèle `User` personnalisé (`accounts/models.py`) porte le rôle
  (étudiant / entreprise / administrateur) et le statut de validation.
- Pensez à créer quelques comptes de démonstration (un étudiant complet, une
  entreprise avec une offre publiée) avant la soutenance pour illustrer le
  tableau de bord et le score d'employabilité.

## Tests automatisés

Le projet inclut des tests unitaires qui valident les règles métier
importantes (score d'employabilité, inscription par rôle, anti-doublon de
candidature, isolation des données entre entreprises, etc.) :

```bash
python manage.py test
```

Utile pour ta soutenance : ça montre que le projet est fiabilisé et pas
seulement "codé à la main" — le jury apprécie généralement de voir des tests.

## Annuaires publics et référentiel partagé

- **Annuaire des étudiants** (`/etudiants/annuaire/`) et **annuaire des
  entreprises** (`/entreprises/annuaire/`) : consultables par tout le monde,
  sans connexion. Seuls les étudiants ayant activé "portfolio public"
  apparaissent dans leur annuaire.
- **Référentiel de compétences** (`/competences/referentiel/`) : commun à
  toute la plateforme. N'importe quel utilisateur connecté — étudiant ou
  entreprise — peut y ajouter une compétence manquante ; elle devient alors
  immédiatement disponible pour tout le monde (anti-doublon automatique,
  insensible à la casse).

## Messagerie étudiant ↔ entreprise (quasi temps réel)

Une entreprise peut contacter un étudiant depuis sa fiche candidat ou son
portfolio public, et un étudiant peut contacter une entreprise depuis sa
fiche publique. La discussion se fait dans `/messages/`.

**Fonctionnement technique** : plutôt que des WebSockets (qui demanderaient
Django Channels + un serveur Redis, plus complexes à faire fonctionner de
façon fiable), la messagerie utilise un rafraîchissement automatique en
JavaScript (`fetch` toutes les 4 secondes) qui interroge une petite API JSON
Django. C'est beaucoup plus simple à expliquer et à faire tourner de façon
fiable pour un projet académique, tout en donnant une vraie sensation de
messagerie instantanée. Le code du polling est commenté dans
`templates/messaging/conversation_detail.html` et `messaging/views.py`.

## Données de démonstration et classement

**Jeu de données de démo** — pour présenter la plateforme déjà remplie
(dashboards, classement, annuaires) sans créer les comptes à la main :

```bash
python manage.py seed_demo            # crée 15 étudiants, 5 entreprises,
                                        # des offres, candidatures et messages
python manage.py seed_demo --clear     # supprime uniquement les comptes de
                                        # démo (préfixe "demo_"), sans toucher
                                        # aux vrais comptes créés depuis l'app
```

Mot de passe commun de tous les comptes de démo : `Demo1234!`
(ex. `demo_etu1` à `demo_etu15`, `demo_rh1` à `demo_rh5`).

**Classement des meilleurs profils** (`/etudiants/classement/`) : page
publique qui trie les étudiants (au profil public) par score
d'employabilité décroissant, avec médailles 🥇🥈🥉 pour le podium.

## Conseiller de carrière IA (100 % local)

Un module d'aide à la décision (app `skillmap_ai`) qui analyse le profil
d'un étudiant et recommande les métiers de l'informatique qui lui
correspondent, avec un plan de progression personnalisé.

**Important pour la soutenance** : ce n'est PAS un grand modèle de langage
(pas de ChatGPT, pas de Claude, pas de connexion internet). C'est un
système d'IA symbolique à base de règles, entièrement transparent :

1. **Base de connaissances** (`skillmap_ai/knowledge_base.py`) — 15 métiers
   de l'informatique, chacun avec ses compétences obligatoires et
   recommandées. Stockée en base de données (modèles `Career` /
   `CareerSkill`), donc modifiable depuis l'admin Django sans toucher au code.
2. **Moteur de recommandation** (`skillmap_ai/engine.py`) — calcule un
   pourcentage de compatibilité par une formule pondérée simple et
   explicable (70 % compétences obligatoires + 30 % recommandées).
3. **Génération d'explications** (`skillmap_ai/explainer.py`) — un texte en
   français est assemblé à partir de gabarits pré-rédigés remplis avec les
   résultats du calcul (génération de texte "à base de règles", une
   technique d'IA symbolique classique, pas un réseau de neurones).
4. **Plan de progression** (`skillmap_ai/roadmap.py`) — regroupe les
   compétences manquantes en étapes d'apprentissage.
5. **Simulateur d'évolution** (`skillmap_ai/simulator.py`) — réutilise
   exactement la formule du score d'employabilité pour estimer l'effet
   d'apprendre de nouvelles compétences, sans rien modifier en base.

### Mise en route

```bash
python manage.py migrate
python manage.py seed_skills      # référentiel de compétences
python manage.py seed_careers     # base de connaissances des métiers
```

Accessible depuis la sidebar étudiant : **🧭 Conseiller de carrière IA**
(page `/conseiller-carriere/`).

Pour ajouter un métier : éditer `skillmap_ai/knowledge_base.py` puis
relancer `python manage.py seed_careers` — ou l'ajouter directement dans
l'admin Django (`/admin/skillmap_ai/career/`).
