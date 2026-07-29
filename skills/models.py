from django.db import models
from students.models import StudentProfile


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('LANGAGE', 'Langage de programmation'),
        ('FRAMEWORK', 'Framework / Librairie'),
        ('RESEAU', 'Réseaux'),
        ('SYSTEME', 'Systèmes / Linux'),
        ('IA', 'Intelligence Artificielle'),
        ('CYBER', 'Cybersécurité'),
        ('DESIGN', 'Design'),
        ('AUTRE', 'Autre'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='AUTRE')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class StudentSkill(models.Model):
    LEVEL_CHOICES = [
        (1, 'Débutant'), (2, 'Intermédiaire'), (3, 'Avancé'), (4, 'Expert'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='student_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='student_skills')
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1)

    class Meta:
        unique_together = ('student', 'skill')
        ordering = ['-level']

    def __str__(self):
        return f"{self.student} - {self.skill} ({self.get_level_display()})"
