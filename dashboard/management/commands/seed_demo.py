"""
Commande de génération de données de démonstration.

Objectif : remplir la plateforme avec des profils réalistes (étudiants,
entreprises, offres, candidatures, quelques messages) pour que les
tableaux de bord, le classement et les annuaires soient parlants dès le
premier lancement — très utile pour une démonstration ou une soutenance.

Utilisation :
    python manage.py seed_demo            # crée les données de démo
    python manage.py seed_demo --clear     # supprime UNIQUEMENT les comptes
                                            # de démo (préfixe "demo_"), sans
                                            # toucher aux vrais comptes

Tous les comptes créés utilisent le préfixe "demo_" dans leur nom
d'utilisateur, ce qui permet de les identifier et de les supprimer
proprement plus tard sans risquer d'effacer de vraies données.
"""
import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from applications.models import Application
from certificates.models import Certificate
from companies.models import CompanyProfile
from jobs.models import Job
from messaging.models import Conversation, Message
from projects.models import Project
from skills.models import Skill, StudentSkill
from students.models import Experience, StudentProfile

User = get_user_model()
DEMO_PASSWORD = "Demo1234!"

STUDENT_NAMES = [
    ("Faniry", "Rakotomalala"), ("Voahangy", "Andrianirina"), ("Tojo", "Rabemananjara"),
    ("Miora", "Rasoanaivo"), ("Hery", "Ravelojaona"), ("Onja", "Randriamampionona"),
    ("Fenosoa", "Rakotoarisoa"), ("Ando", "Razafindrakoto"), ("Nirina", "Rasolofoson"),
    ("Tahiana", "Andriamahefa"), ("Zo", "Rakotondrabe"), ("Volatiana", "Ramanantsoa"),
    ("Mamy", "Rasamimanana"), ("Aina", "Rakotoson"), ("Rivo", "Andrianarisoa"),
]
DEPARTMENTS = ["Informatique", "Génie Logiciel", "Réseaux et Télécommunications", "Intelligence Artificielle"]
UNIVERSITIES = ["Inside University", "Université d'Antananarivo", "IST-T", "ESPA", "Institut Sup'Numeric"]
CITIES = ["Antananarivo", "Toamasina", "Fianarantsoa", "Mahajanga", "Antsirabe"]
LEVELS = ["L1", "L2", "L3", "M1", "M2"]

COMPANIES = [
    ("TechMada Solutions", "Développement logiciel", "Antananarivo"),
    ("Ariary Digital", "Fintech", "Antananarivo"),
    ("Zafy Systems", "Cybersécurité", "Antsirabe"),
    ("Baobab Innovation", "Intelligence Artificielle", "Toamasina"),
    ("Malagasy Cloud", "Infrastructure Cloud", "Antananarivo"),
]

PROJECT_TITLES = [
    "Application de gestion de stock", "Plateforme e-commerce locale",
    "Système de réservation en ligne", "Chatbot d'assistance client",
    "Application mobile de covoiturage", "Dashboard analytique",
]


class Command(BaseCommand):
    help = "Génère des données de démonstration réalistes (étudiants, entreprises, offres, candidatures)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Supprime les comptes de démo existants au lieu d'en créer.")

    def handle(self, *args, **options):
        if options['clear']:
            self._clear()
            return
        self._seed()

    def _clear(self):
        deleted, _ = User.objects.filter(username__startswith='demo_').delete()
        self.stdout.write(self.style.SUCCESS(f"{deleted} enregistrement(s) lié(s) aux comptes de démo supprimé(s)."))

    @transaction.atomic
    def _seed(self):
        skills = list(Skill.objects.all())
        if not skills:
            self.stdout.write(self.style.WARNING(
                "Aucune compétence en base : lancez d'abord `python manage.py seed_skills`."
            ))
            return

        students = self._create_students(skills)
        companies = self._create_companies()
        jobs = self._create_jobs(companies, skills)
        self._create_applications(students, jobs)
        self._create_messages(students, companies)

        self.stdout.write(self.style.SUCCESS(
            f"Données de démo créées : {len(students)} étudiants, {len(companies)} entreprises, "
            f"{len(jobs)} offres. Mot de passe commun : {DEMO_PASSWORD}"
        ))

    def _create_students(self, skills):
        students = []
        for i, (first, last) in enumerate(STUDENT_NAMES):
            username = f"demo_etu{i+1}"
            user, created = User.objects.get_or_create(
                username=username, defaults={'email': f'{username}@example.mg', 'role': 'student', 'is_validated': True},
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()

            student, _ = StudentProfile.objects.update_or_create(
                user=user, defaults={
                    'first_name': first, 'last_name': last,
                    'university': random.choice(UNIVERSITIES),
                    'department': random.choice(DEPARTMENTS),
                    'level': random.choice(LEVELS),
                    'city': random.choice(CITIES),
                    'bio': f"Étudiant(e) passionné(e) par le développement et les nouvelles technologies à {random.choice(CITIES)}.",
                    'portfolio_public': True,
                },
            )

            # Compétences : entre 3 et 8, avec un niveau aléatoire.
            for skill in random.sample(skills, k=min(random.randint(3, 8), len(skills))):
                StudentSkill.objects.update_or_create(
                    student=student, skill=skill, defaults={'level': random.randint(1, 4)},
                )

            # Projets : entre 1 et 4.
            for j in range(random.randint(1, 4)):
                Project.objects.get_or_create(
                    student=student, title=f"{random.choice(PROJECT_TITLES)} #{j+1}",
                    defaults={
                        'description': "Projet académique réalisé en équipe ou en solo, mettant en pratique les compétences acquises en cours.",
                        'technologies': ', '.join(s.name for s in random.sample(skills, k=min(3, len(skills)))),
                        'date': date.today() - timedelta(days=random.randint(30, 700)),
                    },
                )

            # Certificats : 0 à 3.
            for k in range(random.randint(0, 3)):
                Certificate.objects.get_or_create(
                    student=student, title=f"Certification {random.choice(['Python', 'Django', 'Cloud', 'Cybersécurité'])} niveau {k+1}",
                    organization=random.choice(["OpenClassrooms", "Coursera", "Google", "Microsoft"]),
                    defaults={'issue_date': date.today() - timedelta(days=random.randint(30, 500))},
                )

            # Expériences : 0 à 2.
            for m in range(random.randint(0, 2)):
                start = date.today() - timedelta(days=random.randint(200, 900))
                Experience.objects.get_or_create(
                    student=student, title="Stagiaire développeur", organization=random.choice([c[0] for c in COMPANIES]),
                    defaults={'start_date': start, 'end_date': start + timedelta(days=90), 'is_current': False},
                )

            students.append(student)
        return students

    def _create_companies(self):
        companies = []
        for i, (name, sector, city) in enumerate(COMPANIES):
            username = f"demo_rh{i+1}"
            user, created = User.objects.get_or_create(
                username=username, defaults={'email': f'{username}@example.mg', 'role': 'company'},
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()
            company, _ = CompanyProfile.objects.update_or_create(
                user=user, defaults={
                    'company_name': name, 'sector': sector, 'city': city,
                    'description': f"{name} est une entreprise malgache spécialisée en {sector.lower()}.",
                },
            )
            companies.append(company)
        return companies

    def _create_jobs(self, companies, skills):
        jobs = []
        titles = ["Développeur Full-Stack", "Ingénieur Réseaux", "Data Analyst", "Chef de projet IT", "Développeur Mobile"]
        for company in companies:
            for j in range(random.randint(2, 4)):
                job, _ = Job.objects.get_or_create(
                    company=company, title=f"{random.choice(titles)} ({company.company_name})",
                    defaults={
                        'description': "Nous recherchons un(e) candidat(e) motivé(e) pour rejoindre notre équipe technique.",
                        'contract_type': random.choice(['STAGE', 'EMPLOI', 'FREELANCE']),
                        'city': company.city, 'deadline': date.today() + timedelta(days=random.randint(15, 90)),
                        'salary': f"{random.randint(400, 1500)} 000 Ar / mois",
                    },
                )
                job.required_skills.set(random.sample(skills, k=min(random.randint(2, 5), len(skills))))
                jobs.append(job)
        return jobs

    def _create_applications(self, students, jobs):
        statuses = ['PENDING', 'PENDING', 'ACCEPTED', 'REJECTED']  # PENDING plus fréquent
        for student in students:
            for job in random.sample(jobs, k=min(random.randint(1, 3), len(jobs))):
                Application.objects.get_or_create(
                    student=student, job=job, defaults={'status': random.choice(statuses), 'message': "Candidature motivée, disponible rapidement."},
                )

    def _create_messages(self, students, companies):
        for company in companies[:3]:
            for student in random.sample(students, k=min(2, len(students))):
                conversation, _ = Conversation.objects.get_or_create(student=student, company=company)
                Message.objects.get_or_create(
                    conversation=conversation, sender=company.user,
                    defaults={'content': f"Bonjour {student.first_name}, votre profil a retenu notre attention !"},
                )
