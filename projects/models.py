from django.db import models
from students.models import StudentProfile


class Project(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=255, help_text="Séparées par des virgules")
    image = models.ImageField(upload_to='projects/images/', blank=True, null=True)
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    @property
    def technologies_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]
