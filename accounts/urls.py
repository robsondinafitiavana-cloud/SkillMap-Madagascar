from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.choose_role, name='choose_role'),
    path('inscription/etudiant/', views.StudentRegisterView.as_view(), name='register_student'),
    path('inscription/entreprise/', views.CompanyRegisterView.as_view(), name='register_company'),
    path('connexion/', views.SkillMapLoginView.as_view(), name='login'),
    path('deconnexion/', views.SkillMapLogoutView.as_view(), name='logout'),

    # Réinitialisation du mot de passe (Django auth intégré)
    path('mot-de-passe/reinitialiser/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name='password_reset'),
    path('mot-de-passe/reinitialiser/envoye/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('mot-de-passe/reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('mot-de-passe/reinitialiser/termine/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
