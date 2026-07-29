from django.conf import settings
from django.db import models
from django.urls import reverse


class StudentProfile(models.Model):
    LEVEL_CHOICES = [
        ('L1', 'Licence 1'), ('L2', 'Licence 2'), ('L3', 'Licence 3'),
        ('M1', 'Master 1'), ('M2', 'Master 2'), ('DOCTORAT', 'Doctorat'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    university = models.CharField(max_length=150, default="Inside University")
    department = models.CharField(max_length=150, blank=True)  # Filière
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='L3')
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.first_name}-{self.last_name}-{self.user_id}".lower().replace(' ', '-')
            self.slug = base
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('students:portfolio', kwargs={'slug': self.slug})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Experience(models.Model):
    """Expérience professionnelle / stage déclarée par l'étudiant."""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} @ {self.organization}"
