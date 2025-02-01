from django.urls import path
from .views import pegawai_list_create_view, pegawai_retrive_update_delete_view

urlpatterns = [
    path('', pegawai_list_create_view, name="pegawai-list"),
    path('<int:id>/', pegawai_retrive_update_delete_view, name="pegawai-get-id"),
]
