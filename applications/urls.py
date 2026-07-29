from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('postuler/<int:job_pk>/', views.apply_to_job, name='apply_to_job'),
    path('mes-candidatures/', views.my_applications, name='my_applications'),
    path('entreprise/<int:job_pk>/', views.job_applications, name='job_applications'),
    path('<int:pk>/statut/<str:new_status>/', views.update_application_status, name='update_status'),
]
