from django.urls import path
from .views import absensi_list_view, absensi_create_view

urlpatterns = [
    path('', absensi_list_view, name='absensi-list'),
    path('create/',absensi_create_view, name='absensi-create')
]