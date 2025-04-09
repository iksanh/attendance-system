from django.urls import path
from .views import pegawai_list_view, pegawai_update_view, pegawai_create_view, pegawai_delete_view, pegawai_deactivate_view


urlpatterns = [
    path('', pegawai_list_view, name='pegawai-list'),
    path('create/', pegawai_create_view, name='pegawai-create'),
    path('update/<int:pk>/', pegawai_update_view, name='pegawai-update'),
    path('delete/<int:pk>/', pegawai_delete_view, name='pegawai-delete'),
    path('deactivate/<int:pk>/', pegawai_deactivate_view, name='pegawai-deactivate')
]