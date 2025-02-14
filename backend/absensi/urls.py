from django.urls import path
from .views import absensi_list_create_view


urlpatterns = [
    path('', absensi_list_create_view, name='api-absensi-create')
]