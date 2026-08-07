"""
Tests du Conseiller de carrière IA : le moteur de recommandation doit
identifier le bon métier selon les compétences déclarées, l'explication
générée doit être cohérente, le simulateur doit refléter une progression,
et l'accès doit rester réservé aux étudiants.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from companies.models import CompanyProfile
from skills.models import Skill, StudentSkill
from skillmap_ai.engine import compute_career_matches
from skillmap_ai.explainer import generate_explanation
from skillmap_ai.models import Career, CareerSkill
from skillmap_ai.roadmap import build_roadmap
from skillmap_ai.simulator import simulate_evolution
from students.models import StudentProfile

User = get_user_model()


class CareerMatchingEngineTests(TestCase):

    def setUp(self):
        # Deux métiers volontairement différents pour vérifier que le
        # moteur distingue bien les profils.
        self.python_skill = Skill.objects.create(name='Python', category='LANGAGE')
        self.django_skill = Skill.objects.create(name='Django', category='FRAMEWORK')
        self.figma_skill = Skill.objects.create(name='Figma', category='DESIGN')

        self.backend = Career.objects.create(name='Développeur Backend')
        CareerSkill.objects.create(career=self.backend, skill=self.python_skill, importance='REQUIRED')
        CareerSkill.objects.create(career=self.backend, skill=self.django_skill, importance='REQUIRED')

        self.designer = Career.objects.create(name='UX/UI Designer')
        CareerSkill.objects.create(career=self.designer, skill=self.figma_skill, importance='REQUIRED')

        user = User.objects.create_user(username='dev_test', password='pass1234', role='student')
        self.student = StudentProfile.objects.create(user=user, first_name='A', last_name='B')
        StudentSkill.objects.create(student=self.student, skill=self.python_skill, level=3)
        StudentSkill.objects.create(student=self.student, skill=self.django_skill, level=3)

    def test_le_metier_le_plus_compatible_est_correctement_identifie(self):
        matches = compute_career_matches(self.student)
        self.assertEqual(matches[0]['career'], self.backend)
        self.assertEqual(matches[0]['percent'], 100)

    def test_un_metier_sans_competence_correspondante_a_un_score_de_zero(self):
        matches = compute_career_matches(self.student)
        designer_match = next(m for m in matches if m['career'] == self.designer)
        self.assertEqual(designer_match['percent'], 0)

    def test_explication_mentionne_le_metier_et_les_points_forts(self):
        matches = compute_career_matches(self.student)
        explanation = generate_explanation(matches)
        self.assertIn('Développeur Backend', explanation)
        self.assertIn('Python', explanation)

    def test_roadmap_est_vide_si_toutes_les_competences_sont_maitrisees(self):
        matches = compute_career_matches(self.student)
        roadmap = build_roadmap(matches[0])
        self.assertTrue(roadmap['already_ready'])
        self.assertEqual(roadmap['steps'], [])


class SimulatorTests(TestCase):

    def setUp(self):
        self.skill = Skill.objects.create(name='Docker', category='SYSTEME')
        user = User.objects.create_user(username='sim_test', password='pass1234', role='student')
        self.student = StudentProfile.objects.create(user=user, first_name='C', last_name='D')

    def test_ajouter_une_competence_augmente_le_score_simule(self):
        result = simulate_evolution(self.student, extra_skill_ids=[self.skill.id])
        self.assertGreater(result['after'], result['before'])

    def test_une_competence_deja_possedee_n_est_pas_recomptee(self):
        StudentSkill.objects.create(student=self.student, skill=self.skill, level=4)
        result = simulate_evolution(self.student, extra_skill_ids=[self.skill.id])
        # Le score simulé doit être strictement identique au score actuel,
        # puisque la compétence est déjà acquise.
        self.assertEqual(result['before'], result['after'])


class AdvisorAccessTests(TestCase):

    def test_page_reservee_aux_etudiants(self):
        user = User.objects.create_user(username='rh_access', password='pass1234', role='company')
        CompanyProfile.objects.create(user=user, company_name='TestCorp')
        self.client.login(username='rh_access', password='pass1234')
        response = self.client.get(reverse('skillmap_ai:advisor'))
        self.assertEqual(response.status_code, 403)

    def test_etudiant_peut_acceder_a_la_page(self):
        user = User.objects.create_user(username='etu_access', password='pass1234', role='student')
        StudentProfile.objects.create(user=user, first_name='E', last_name='F')
        self.client.login(username='etu_access', password='pass1234')
        response = self.client.get(reverse('skillmap_ai:advisor'))
        self.assertEqual(response.status_code, 200)
