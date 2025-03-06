from django.urls import path
from pegawai.api.views import pegawai_list_create_view, pegawai_retrive_update_delete_view, pegawai_upload_csv_view

urlpatterns = [
    path('', pegawai_list_create_view, name="pegawai-list"),
    path('<int:id>/', pegawai_retrive_update_delete_view, name="pegawai-get-id"),
    path('upload_csv/', pegawai_upload_csv_view, name="pegawai-upload-csv"),
]
