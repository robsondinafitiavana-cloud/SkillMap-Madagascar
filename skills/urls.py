from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('referentiel/', views.skill_catalog, name='skill_catalog'),
    path('<int:pk>/supprimer/', views.skill_delete, name='skill_delete'),
]
