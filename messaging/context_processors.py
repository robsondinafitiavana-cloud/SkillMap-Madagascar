from .models import Message


def unread_messages(request):
    """Rend le nombre de messages non lus disponible dans tous les templates
    (pour afficher un badge sur le lien "Messages" de la sidebar)."""
    if not request.user.is_authenticated:
        return {'unread_messages_count': 0}

    if getattr(request.user, 'is_student', False) and hasattr(request.user, 'student_profile'):
        conversations = request.user.student_profile.conversations.all()
    elif getattr(request.user, 'is_company', False) and hasattr(request.user, 'company_profile'):
        conversations = request.user.company_profile.conversations.all()
    else:
        return {'unread_messages_count': 0}

    count = Message.objects.filter(
        conversation__in=conversations, is_read=False
    ).exclude(sender=request.user).count()
    return {'unread_messages_count': count}
