"""
Tests automatisés de l'app students.

Objectif pédagogique : ces tests servent aussi de documentation vivante du
comportement attendu (score d'employabilité, portfolio public, etc.) et
peuvent être lancés avec :

    python manage.py test students
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from certificates.models import Certificate
from projects.models import Project
from skills.models import Skill, StudentSkill
from students.models import StudentProfile
from students.scoring import compute_employability_score

User = get_user_model()


class EmployabilityScoreTests(TestCase):
    """Vérifie que le calcul du score d'employabilité respecte les
    pondérations annoncées (compétences 40 %, projets 25 %, certificats 20 %,
    expériences 15 %)."""

    def setUp(self):
        user = User.objects.create_user(username='etu1', password='pass1234', role='student')
        self.student = StudentProfile.objects.create(
            user=user, first_name='Rasoa', last_name='Andria', department='Informatique',
        )

    def test_score_zero_pour_profil_vide(self):
        score = compute_employability_score(self.student)
        self.assertEqual(score['total'], 0)

    def test_score_augmente_avec_les_competences(self):
        skill = Skill.objects.create(name='Django', category='FRAMEWORK')
        StudentSkill.objects.create(student=self.student, skill=skill, level=4)  # Expert

        score = compute_employability_score(self.student)
        self.assertGreater(score['total'], 0)
        # Une seule compétence Expert doit peser sur la sous-note "compétences"
        self.assertGreater(score['skills_subscore'], 0)

    def test_score_total_borne_a_100(self):
        # On ajoute largement plus que les cibles de chaque catégorie pour
        # vérifier qu'on ne dépasse jamais 100/100.
        for i in range(15):
            skill = Skill.objects.create(name=f'Skill{i}', category='AUTRE')
            StudentSkill.objects.create(student=self.student, skill=skill, level=4)
            Project.objects.create(
                student=self.student, title=f'Projet {i}', description='desc',
                technologies='Django', date='2025-01-01',
            )
            Certificate.objects.create(
                student=self.student, title=f'Certif {i}', organization='OC', issue_date='2025-01-01',
            )
        score = compute_employability_score(self.student)
        self.assertLessEqual(score['total'], 100)


class PortfolioPublicTests(TestCase):
    """Vérifie que le portfolio public respecte le paramètre de
    confidentialité choisi par l'étudiant."""

    def setUp(self):
        user = User.objects.create_user(username='etu2', password='pass1234', role='student')
        self.student = StudentProfile.objects.create(
            user=user, first_name='Voa', last_name='Rakoto', department='Réseaux',
            portfolio_public=True,
        )

    def test_portfolio_accessible_sans_connexion(self):
        url = reverse('students:portfolio', kwargs={'slug': self.student.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Voa Rakoto')

    def test_portfolio_prive_renvoie_404(self):
        self.student.portfolio_public = False
        self.student.save()
        url = reverse('students:portfolio', kwargs={'slug': self.student.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class StudentDirectoryTests(TestCase):
    """Vérifie que l'annuaire public n'affiche que les profils publics."""

    def test_seuls_les_profils_publics_apparaissent(self):
        u1 = User.objects.create_user(username='pub', password='pass1234', role='student')
        StudentProfile.objects.create(user=u1, first_name='Public', last_name='X', portfolio_public=True)
        u2 = User.objects.create_user(username='priv', password='pass1234', role='student')
        StudentProfile.objects.create(user=u2, first_name='Prive', last_name='Y', portfolio_public=False)

        response = self.client.get(reverse('students:student_directory'))
        self.assertContains(response, 'Public X')
        self.assertNotContains(response, 'Prive Y')
