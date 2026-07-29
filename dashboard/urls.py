from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/valider/<int:user_id>/', views.validate_profile, name='validate_profile'),
]
