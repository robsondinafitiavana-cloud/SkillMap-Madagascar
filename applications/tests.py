"""
Tests de l'app applications : le cœur métier "un étudiant postule à une
offre" doit respecter deux règles importantes :
  1. Impossible de postuler deux fois à la même offre.
  2. Une entreprise ne peut changer le statut que des candidatures reçues
     sur SES propres offres.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from applications.models import Application
from companies.models import CompanyProfile
from jobs.models import Job
from students.models import StudentProfile

User = get_user_model()


class ApplicationFlowTests(TestCase):

    def setUp(self):
        student_user = User.objects.create_user(username='candidat', password='pass1234', role='student')
        self.student = StudentProfile.objects.create(
            user=student_user, first_name='Hery', last_name='Zafy', department='Informatique',
        )
        company_user = User.objects.create_user(username='recruteur', password='pass1234', role='company')
        self.company = CompanyProfile.objects.create(user=company_user, company_name='TestCorp')
        self.job = Job.objects.create(
            company=self.company, title='Stage Django', description='desc',
            contract_type='STAGE', deadline='2027-01-01',
        )

    def test_postuler_cree_une_candidature(self):
        self.client.login(username='candidat', password='pass1234')
        response = self.client.post(reverse('applications:apply_to_job', args=[self.job.pk]), {
            'message': 'Motivé !',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Application.objects.filter(student=self.student, job=self.job).exists())

    def test_impossible_de_postuler_deux_fois(self):
        Application.objects.create(student=self.student, job=self.job)
        self.client.login(username='candidat', password='pass1234')
        response = self.client.post(
            reverse('applications:apply_to_job', args=[self.job.pk]), {'message': 'Encore'}, follow=True,
        )
        # Toujours une seule candidature, la deuxième tentative est bloquée.
        self.assertEqual(Application.objects.filter(student=self.student, job=self.job).count(), 1)

    def test_entreprise_peut_changer_le_statut_de_sa_propre_offre(self):
        application = Application.objects.create(student=self.student, job=self.job)
        self.client.login(username='recruteur', password='pass1234')
        self.client.get(reverse('applications:update_status', args=[application.pk, 'ACCEPTED']))
        application.refresh_from_db()
        self.assertEqual(application.status, 'ACCEPTED')

    def test_entreprise_ne_peut_pas_modifier_les_offres_dautrui(self):
        autre_recruteur = User.objects.create_user(username='autre_rh', password='pass1234', role='company')
        CompanyProfile.objects.create(user=autre_recruteur, company_name='AutreCorp')
        application = Application.objects.create(student=self.student, job=self.job)

        self.client.login(username='autre_rh', password='pass1234')
        response = self.client.get(reverse('applications:update_status', args=[application.pk, 'ACCEPTED']))
        self.assertEqual(response.status_code, 404)  # l'offre n'appartient pas à cette entreprise
