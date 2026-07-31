"""
App messaging : messagerie entre un étudiant et une entreprise.

Deux modèles simples :
    Conversation -> le "fil" entre UN étudiant et UNE entreprise (il ne peut
                    exister qu'une seule conversation entre une paire donnée,
                    grâce à unique_together).
    Message      -> chaque message envoyé dans une conversation, avec son
                    expéditeur (le User, étudiant ou entreprise).

La "temps réel" est obtenue côté frontend par un rafraîchissement automatique
(polling AJAX toutes les quelques secondes) plutôt que par WebSocket : c'est
volontairement plus simple à faire fonctionner de façon fiable (aucune
dépendance externe comme Redis ou un serveur ASGI), tout en donnant une vraie
sensation de messagerie instantanée pour l'utilisateur.
"""
from django.conf import settings
from django.db import models

from companies.models import CompanyProfile
from students.models import StudentProfile


class Conversation(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='conversations')
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'company')
        ordering = ['-id']

    def __str__(self):
        return f"{self.student.full_name} <-> {self.company.company_name}"

    def other_party_name(self, user):
        """Retourne le nom à afficher pour "l'autre" participant, vu depuis `user`."""
        if user == self.student.user:
            return self.company.company_name
        return self.student.full_name

    def last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count_for(self, user):
        return self.messages.exclude(sender=user).filter(is_read=False).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} : {self.content[:30]}"
