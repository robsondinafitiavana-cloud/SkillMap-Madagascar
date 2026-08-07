"""
Base de connaissances du Conseiller de carrière IA.

Un métier (`Career`) est décrit par sa fiche descriptive et par la liste des
compétences qui lui sont associées (`CareerSkill`), chacune marquée comme
"obligatoire" ou "recommandée". C'est cette base de connaissances que le
moteur de recommandation (skillmap_ai/engine.py) compare au profil de
l'étudiant pour calculer un pourcentage de compatibilité par métier.

Stockée en base de données (plutôt qu'en dur dans le code Python), elle
reste facilement extensible : on peut ajouter un nouveau métier ou changer
ses compétences directement depuis l'admin Django, sans toucher au code.
"""
from django.db import models

from skills.models import Skill


class Career(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    domain = models.CharField(max_length=100, blank=True, help_text="Ex : Développement, Données, Infrastructure...")
    recommended_level = models.CharField(max_length=100, blank=True, help_text="Ex : L3 minimum")
    desired_experience = models.CharField(max_length=150, blank=True, help_text="Ex : Débutant accepté (stage/junior)")
    average_salary = models.CharField(max_length=150, blank=True, help_text="Ex : 700 000 - 1 500 000 Ar / mois")
    growth_prospects = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def required_skills(self):
        return [cs.skill for cs in self.career_skills.filter(importance='REQUIRED').select_related('skill')]

    def recommended_skills(self):
        return [cs.skill for cs in self.career_skills.filter(importance='RECOMMENDED').select_related('skill')]


class CareerSkill(models.Model):
    IMPORTANCE_CHOICES = [
        ('REQUIRED', 'Obligatoire'),
        ('RECOMMENDED', 'Recommandée'),
    ]
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='career_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='career_links')
    importance = models.CharField(max_length=15, choices=IMPORTANCE_CHOICES, default='REQUIRED')

    class Meta:
        unique_together = ('career', 'skill')
        ordering = ['importance', 'skill__name']

    def __str__(self):
        return f"{self.career.name} - {self.skill.name} ({self.get_importance_display()})"
