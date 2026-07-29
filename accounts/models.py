from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Utilisateur SkillMap Madagascar : étudiant, entreprise ou administrateur.

    On étend le User standard de Django (AbstractUser) plutôt que de créer 3
    modèles séparés, pour garder UN SEUL système d'authentification (login,
    mot de passe, permissions) commun aux 3 rôles. Le champ `role` indique
    ensuite QUEL profil détaillé aller chercher :
        - role='student' -> voir students.models.StudentProfile (OneToOne)
        - role='company' -> voir companies.models.CompanyProfile (OneToOne)
        - role='admin'   -> pas de profil détaillé, accès à l'admin Django
    """

    class Role(models.TextChoices):
        STUDENT = 'student', 'Étudiant'
        COMPANY = 'company', 'Entreprise'
        ADMIN = 'admin', 'Administrateur'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    is_validated = models.BooleanField(default=False, help_text="Profil validé par l'administrateur")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_company(self):
        return self.role == self.Role.COMPANY

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
