from django.urls import path
from .views import pegawai_list_create_view

urlpatterns = [
    path('', pegawai_list_create_view, name="pegawai-list"),
]
