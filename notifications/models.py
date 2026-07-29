from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ('NEW_JOB', 'Nouvelle offre'),
        ('NEW_APPLICATION', 'Nouvelle candidature'),
        ('PROFILE_VALIDATED', 'Profil validé'),
        ('JOB_EXPIRED', 'Offre expirée'),
        ('APPLICATION_STATUS', 'Statut de candidature mis à jour'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='NEW_JOB')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.message}"
