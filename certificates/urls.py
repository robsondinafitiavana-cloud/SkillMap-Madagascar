from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('ajouter/', views.certificate_create, name='certificate_create'),
    path('<int:pk>/supprimer/', views.certificate_delete, name='certificate_delete'),
]
