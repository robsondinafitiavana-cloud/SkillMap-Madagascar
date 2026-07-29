from django.db import models
from students.models import StudentProfile


class Certificate(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=150)
    issue_date = models.DateField()
    file = models.FileField(upload_to='certificates/files/', blank=True, null=True)
    image = models.ImageField(upload_to='certificates/images/', blank=True, null=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.title} - {self.organization}"
