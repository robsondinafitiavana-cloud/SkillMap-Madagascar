from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('entreprise/mes-offres/', views.company_job_list, name='company_job_list'),
    path('entreprise/publier/', views.job_create, name='job_create'),
    path('entreprise/<int:pk>/modifier/', views.job_edit, name='job_edit'),
    path('entreprise/<int:pk>/supprimer/', views.job_delete, name='job_delete'),
]
