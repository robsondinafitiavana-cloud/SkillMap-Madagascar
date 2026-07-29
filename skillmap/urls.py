from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from dashboard.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='root'),
    path('comptes/', include('accounts.urls')),
    path('etudiants/', include('students.urls')),
    path('entreprises/', include('companies.urls')),
    path('competences/', include('skills.urls')),
    path('projets/', include('projects.urls')),
    path('certificats/', include('certificates.urls')),
    path('offres/', include('jobs.urls')),
    path('candidatures/', include('applications.urls')),
    path('tableau-de-bord/', include('dashboard.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
