from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('annuaire/', views.student_directory, name='student_directory'),
    path('profil/', views.profile_edit, name='profile_edit'),
    path('experiences/', views.experience_list, name='experience_list'),
    path('experiences/<int:pk>/supprimer/', views.experience_delete, name='experience_delete'),
    path('cv/telecharger/', views.download_cv, name='download_cv'),
    path('portfolio/<slug:slug>/', views.portfolio_public, name='portfolio'),
]
