from django.urls import path
from absensi.api.views import absensi_list_create_view, absensi_detail_list_view, absensi_upload_view, pegawai_absensi_api, absensi_pivot_api_view


urlpatterns = [
    path('', absensi_list_create_view, name='api-absensi-create'),
    path('detail/', absensi_detail_list_view, name='api-absensi-list-detail'),
    path('upload_excel/', absensi_upload_view, name='api-absensi-upload'),
    path('pegawai_absensi/', pegawai_absensi_api, name='api-pegawai-absensi'),
    path('pivot_absensi/', absensi_pivot_api_view, name='api-pegawai-absensi-pivot')
]