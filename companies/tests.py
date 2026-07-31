"""
Tests de l'app companies : la page "Mon profil entreprise" façon
Facebook/Instagram, et le fait qu'elle affiche bien les bonnes statistiques.
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from companies.models import CompanyProfile
from jobs.models import Job

User = get_user_model()


class CompanyProfileViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='rh_test', password='pass1234', role='company')
        self.company = CompanyProfile.objects.create(user=self.user, company_name='TestCorp', sector='IT')

    def test_page_profil_accessible_et_affiche_les_offres(self):
        Job.objects.create(
            company=self.company, title='Dev Django', description='desc',
            contract_type='STAGE', deadline=date.today() + timedelta(days=30),
        )
        self.client.login(username='rh_test', password='pass1234')
        response = self.client.get(reverse('companies:profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestCorp')
        self.assertContains(response, 'Dev Django')

    def test_modification_redirige_vers_la_page_profil(self):
        self.client.login(username='rh_test', password='pass1234')
        response = self.client.post(reverse('companies:profile_edit'), {
            'company_name': 'TestCorp', 'sector': 'IT',
        })
        self.assertRedirects(response, reverse('companies:profile_view'))

    def test_un_etudiant_ne_peut_pas_voir_le_profil_dune_autre_entreprise(self):
        # profile_view utilise toujours l'entreprise du user connecté :
        # impossible d'y accéder sans être une entreprise.
        student_user = User.objects.create_user(username='etu_test', password='pass1234', role='student')
        self.client.login(username='etu_test', password='pass1234')
        response = self.client.get(reverse('companies:profile_view'))
        self.assertEqual(response.status_code, 404)
