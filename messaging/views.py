"""
Vues de la messagerie.

Deux vues "normales" (pages HTML) :
    conversation_list   -> liste des discussions de l'utilisateur connecté
    conversation_detail -> une discussion précise (affichage initial des
                            messages ; le rafraîchissement ensuite se fait
                            en JavaScript via les vues API ci-dessous)

Deux vues "API" qui répondent en JSON, appelées par le JavaScript de
conversation_detail.html :
    api_poll_messages -> "y a-t-il de nouveaux messages depuis le dernier
                          affiché ?" (appelée toutes les 4 secondes)
    api_send_message  -> envoyer un nouveau message sans recharger la page
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from companies.models import CompanyProfile
from notifications.utils import notify
from students.models import StudentProfile
from .forms import MessageForm
from .models import Conversation, Message


def _user_is_participant(conversation, user):
    """Un utilisateur ne peut voir/écrire dans une conversation que s'il en
    est l'un des deux participants (l'étudiant concerné ou l'entreprise
    concernée)."""
    return user == conversation.student.user or user == conversation.company.user


@login_required
def conversation_list(request):
    if getattr(request.user, 'is_student', False):
        student = get_object_or_404(StudentProfile, user=request.user)
        conversations = student.conversations.select_related('company').all()
    elif getattr(request.user, 'is_company', False):
        company = get_object_or_404(CompanyProfile, user=request.user)
        conversations = company.conversations.select_related('student').all()
    else:
        conversations = Conversation.objects.none()

    # On trie par date du dernier message (les discussions les plus
    # récemment actives en premier), et on prépare les infos d'affichage.
    items = []
    for conv in conversations:
        last = conv.last_message()
        items.append({
            'conversation': conv,
            'other_name': conv.other_party_name(request.user),
            'last_message': last,
            'unread_count': conv.unread_count_for(request.user),
        })
    items.sort(key=lambda i: i['last_message'].created_at if i['last_message'] else i['conversation'].created_at, reverse=True)

    return render(request, 'messaging/conversation_list.html', {'items': items})


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if not _user_is_participant(conversation, request.user):
        return HttpResponseForbidden("Vous n'avez pas accès à cette conversation.")

    # En ouvrant la discussion, on marque comme lus les messages reçus.
    conversation.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)

    messages_qs = conversation.messages.select_related('sender').all()
    form = MessageForm()

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'other_name': conversation.other_party_name(request.user),
        'messages_list': messages_qs,
        'form': form,
        'last_message_id': messages_qs.last().id if messages_qs.exists() else 0,
    })


@login_required
def start_with_student(request, student_pk):
    """Une entreprise clique sur "Contacter" depuis un profil étudiant :
    on récupère la conversation existante ou on en crée une nouvelle."""
    if not getattr(request.user, 'is_company', False):
        return HttpResponseForbidden("Réservé aux entreprises.")
    company = get_object_or_404(CompanyProfile, user=request.user)
    student = get_object_or_404(StudentProfile, pk=student_pk)
    conversation, _ = Conversation.objects.get_or_create(student=student, company=company)
    return redirect('messaging:conversation_detail', pk=conversation.pk)


@login_required
def start_with_company(request, company_pk):
    """Un étudiant clique sur "Contacter" depuis une fiche entreprise."""
    if not getattr(request.user, 'is_student', False):
        return HttpResponseForbidden("Réservé aux étudiants.")
    student = get_object_or_404(StudentProfile, user=request.user)
    company = get_object_or_404(CompanyProfile, pk=company_pk)
    conversation, _ = Conversation.objects.get_or_create(student=student, company=company)
    return redirect('messaging:conversation_detail', pk=conversation.pk)


@login_required
def api_poll_messages(request, pk):
    """Endpoint JSON interrogé toutes les quelques secondes par le
    JavaScript de la page de discussion : "donne-moi les messages plus
    récents que celui-ci"."""
    conversation = get_object_or_404(Conversation, pk=pk)
    if not _user_is_participant(conversation, request.user):
        return HttpResponseForbidden()

    after_id = int(request.GET.get('after', 0))
    new_messages = conversation.messages.filter(id__gt=after_id).select_related('sender')
    # Les messages reçus pendant qu'on regarde la page sont aussi marqués lus.
    new_messages.exclude(sender=request.user).update(is_read=True)

    data = [{
        'id': m.id,
        'content': m.content,
        'is_mine': m.sender_id == request.user.id,
        'created_at': timezone.localtime(m.created_at).strftime('%H:%M'),
    } for m in new_messages]

    return JsonResponse({'messages': data})


@login_required
@require_POST
def api_send_message(request, pk):
    """Endpoint JSON appelé par le formulaire de discussion (envoi sans
    recharger la page)."""
    conversation = get_object_or_404(Conversation, pk=pk)
    if not _user_is_participant(conversation, request.user):
        return HttpResponseForbidden()

    content = json.loads(request.body).get('content', '').strip() if request.body else ''
    if not content:
        return JsonResponse({'error': 'Message vide.'}, status=400)

    message = Message.objects.create(conversation=conversation, sender=request.user, content=content)

    # On notifie l'autre participant (visible dans la cloche de notifications).
    recipient = conversation.company.user if request.user == conversation.student.user else conversation.student.user
    sender_name = conversation.other_party_name(recipient)  # nom de l'expéditeur vu par le destinataire
    notify(recipient, 'NEW_MESSAGE', f"Nouveau message de {sender_name}", link=f"/messages/{conversation.pk}/")

    return JsonResponse({
        'id': message.id,
        'content': message.content,
        'created_at': timezone.localtime(message.created_at).strftime('%H:%M'),
    })
