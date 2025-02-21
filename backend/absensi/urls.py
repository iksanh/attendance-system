from django.urls import path
from .views import absensi_list_create_view, absensi_detail_list_view, absensi_upload_view


urlpatterns = [
    path('', absensi_list_create_view, name='api-absensi-create'),
    path('detail/', absensi_detail_list_view, name='api-absensi-list-detail'),
    path('upload_excel/', absensi_upload_view, name='api-absensi-upload')
]