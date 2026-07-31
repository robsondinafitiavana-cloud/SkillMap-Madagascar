from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('demarrer/etudiant/<int:student_pk>/', views.start_with_student, name='start_with_student'),
    path('demarrer/entreprise/<int:company_pk>/', views.start_with_company, name='start_with_company'),
    path('<int:pk>/api/messages/', views.api_poll_messages, name='api_poll_messages'),
    path('<int:pk>/api/envoyer/', views.api_send_message, name='api_send_message'),
]
