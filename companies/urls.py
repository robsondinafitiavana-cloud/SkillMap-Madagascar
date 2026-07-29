from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('annuaire/', views.company_directory, name='company_directory'),
    path('annuaire/<int:pk>/', views.company_public_detail, name='company_public_detail'),
    path('profil/', views.profile_edit, name='profile_edit'),
    path('candidats/', views.search_candidates, name='search_candidates'),
    path('candidats/<int:pk>/', views.candidate_detail, name='candidate_detail'),
]
