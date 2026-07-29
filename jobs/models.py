from django.db import models
from django.utils import timezone
from companies.models import CompanyProfile
from skills.models import Skill


class Job(models.Model):
    CONTRACT_CHOICES = [
        ('STAGE', 'Stage'),
        ('EMPLOI', 'Emploi'),
        ('FREELANCE', 'Freelance'),
    ]
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True, help_text="Ex: 800 000 Ar / mois")
    contract_type = models.CharField(max_length=10, choices=CONTRACT_CHOICES, default='STAGE')
    required_skills = models.ManyToManyField(Skill, blank=True, related_name='jobs')
    city = models.CharField(max_length=100, blank=True)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"

    @property
    def is_expired(self):
        return self.deadline < timezone.now().date()
