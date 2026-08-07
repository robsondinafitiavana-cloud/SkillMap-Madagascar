from django.urls import path
from . import views

app_name = 'skillmap_ai'

urlpatterns = [
    path('', views.advisor, name='advisor'),
    path('simuler/', views.simulate_api, name='simulate_api'),
]
