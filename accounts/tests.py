"""
Tests de l'app accounts : vérifie que l'inscription crée bien le bon type
de profil selon le rôle choisi, et que les rôles sont correctement isolés.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from companies.models import CompanyProfile
from students.models import StudentProfile

User = get_user_model()


class RegistrationTests(TestCase):

    def test_inscription_etudiant_cree_un_studentprofile(self):
        response = self.client.post(reverse('accounts:register_student'), {
            'username': 'nouvel_etudiant', 'email': 'e@example.com',
            'first_name': 'Tojo', 'last_name': 'Rabe',
            'university': 'Inside University', 'department': 'Informatique',
            'password1': 'UnMotDePasse123', 'password2': 'UnMotDePasse123',
        })
        self.assertEqual(response.status_code, 302)  # redirection après succès
        user = User.objects.get(username='nouvel_etudiant')
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertTrue(StudentProfile.objects.filter(user=user).exists())

    def test_inscription_entreprise_cree_un_companyprofile(self):
        response = self.client.post(reverse('accounts:register_company'), {
            'username': 'nouvelle_entreprise', 'email': 'rh@example.com',
            'company_name': 'TestCorp', 'sector': 'IT',
            'password1': 'UnMotDePasse123', 'password2': 'UnMotDePasse123',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='nouvelle_entreprise')
        self.assertEqual(user.role, User.Role.COMPANY)
        self.assertTrue(CompanyProfile.objects.filter(user=user).exists())

    def test_connexion_avec_mauvais_mot_de_passe_echoue(self):
        User.objects.create_user(username='test_login', password='BonMotDePasse123')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'test_login', 'password': 'MauvaisMotDePasse',
        })
        self.assertEqual(response.status_code, 200)  # reste sur la page, pas de redirection
        self.assertFalse(response.context['user'].is_authenticated)
