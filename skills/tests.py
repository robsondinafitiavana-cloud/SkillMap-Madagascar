"""
Tests de l'app skills : le référentiel de compétences doit être ouvert à
tout utilisateur connecté (étudiant ou entreprise), sans doublons.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from companies.models import CompanyProfile
from skills.models import Skill
from students.models import StudentProfile

User = get_user_model()


class SkillCatalogTests(TestCase):

    def test_un_etudiant_peut_ajouter_une_competence(self):
        user = User.objects.create_user(username='etu', password='pass1234', role='student')
        StudentProfile.objects.create(user=user, first_name='A', last_name='B')
        self.client.login(username='etu', password='pass1234')

        response = self.client.post(reverse('skills:skill_catalog'), {
            'name': 'Rust', 'category': 'LANGAGE',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Skill.objects.filter(name='Rust').exists())

    def test_une_entreprise_peut_aussi_ajouter_une_competence(self):
        user = User.objects.create_user(username='rh', password='pass1234', role='company')
        CompanyProfile.objects.create(user=user, company_name='TestCorp')
        self.client.login(username='rh', password='pass1234')

        response = self.client.post(reverse('skills:skill_catalog'), {
            'name': 'Kubernetes', 'category': 'SYSTEME',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Skill.objects.filter(name='Kubernetes').exists())

    def test_pas_de_doublon_insensible_a_la_casse(self):
        Skill.objects.create(name='Python', category='LANGAGE')
        user = User.objects.create_user(username='etu2', password='pass1234', role='student')
        StudentProfile.objects.create(user=user, first_name='C', last_name='D')
        self.client.login(username='etu2', password='pass1234')

        self.client.post(reverse('skills:skill_catalog'), {'name': 'python', 'category': 'LANGAGE'})
        self.assertEqual(Skill.objects.filter(name__iexact='python').count(), 1)
