from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('ajouter/', views.project_create, name='project_create'),
    path('<int:pk>/modifier/', views.project_edit, name='project_edit'),
    path('<int:pk>/supprimer/', views.project_delete, name='project_delete'),
]
