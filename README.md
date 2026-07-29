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
