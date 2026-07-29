from .models import Notification


def notify(user, notif_type, message, link=""):
    """Crée une notification pour un utilisateur donné."""
    return Notification.objects.create(
        user=user, notif_type=notif_type, message=message, link=link
    )
