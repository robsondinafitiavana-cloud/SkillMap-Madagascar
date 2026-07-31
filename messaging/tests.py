"""
Tests de l'app messaging : démarrage de conversation, envoi/réception de
messages, et surtout l'isolation de sécurité (un tiers ne doit jamais
pouvoir lire ou écrire dans une conversation qui ne le concerne pas).
"""
import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from companies.models import CompanyProfile
from messaging.models import Conversation, Message
from students.models import StudentProfile

User = get_user_model()


class MessagingTests(TestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(username='etu', password='pass1234', role='student')
        self.student = StudentProfile.objects.create(user=self.student_user, first_name='A', last_name='B')
        self.company_user = User.objects.create_user(username='rh', password='pass1234', role='company')
        self.company = CompanyProfile.objects.create(user=self.company_user, company_name='TestCorp')

    def test_entreprise_peut_demarrer_une_conversation(self):
        self.client.login(username='rh', password='pass1234')
        self.client.get(reverse('messaging:start_with_student', args=[self.student.pk]))
        self.assertTrue(Conversation.objects.filter(student=self.student, company=self.company).exists())

    def test_demarrer_deux_fois_ne_cree_pas_de_doublon(self):
        self.client.login(username='rh', password='pass1234')
        self.client.get(reverse('messaging:start_with_student', args=[self.student.pk]))
        self.client.get(reverse('messaging:start_with_student', args=[self.student.pk]))
        self.assertEqual(Conversation.objects.filter(student=self.student, company=self.company).count(), 1)

    def test_envoi_et_reception_de_message(self):
        conversation = Conversation.objects.create(student=self.student, company=self.company)
        self.client.login(username='rh', password='pass1234')

        response = self.client.post(
            reverse('messaging:api_send_message', args=[conversation.pk]),
            data=json.dumps({'content': 'Bonjour !'}), content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.filter(conversation=conversation).count(), 1)

    def test_un_tiers_ne_peut_pas_lire_la_conversation(self):
        conversation = Conversation.objects.create(student=self.student, company=self.company)
        intrus = User.objects.create_user(username='intrus', password='pass1234', role='student')
        StudentProfile.objects.create(user=intrus, first_name='In', last_name='Trus')

        self.client.login(username='intrus', password='pass1234')
        response = self.client.get(reverse('messaging:conversation_detail', args=[conversation.pk]))
        self.assertEqual(response.status_code, 403)

    def test_le_polling_ne_renvoie_que_les_nouveaux_messages(self):
        conversation = Conversation.objects.create(student=self.student, company=self.company)
        m1 = Message.objects.create(conversation=conversation, sender=self.company_user, content='Premier')
        Message.objects.create(conversation=conversation, sender=self.student_user, content='Deuxieme')

        self.client.login(username='rh', password='pass1234')
        response = self.client.get(reverse('messaging:api_poll_messages', args=[conversation.pk]) + f'?after={m1.id}')
        data = response.json()
        self.assertEqual(len(data['messages']), 1)
        self.assertEqual(data['messages'][0]['content'], 'Deuxieme')
