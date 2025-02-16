from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Absensi, AbsensiDetail, AbsensiDetailManager
from .serializers import AbsensiSerializer, AbsensiDetailSerializer

# Create your views here.

class AbsensiCreateView(generics.ListCreateAPIView):

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        tanggal_absen = self.request.query_params.get('tanggal_absen')
        if tanggal_absen:
            return AbsensiDetail.objects.search_by_tanggal_absen(tanggal_absen)
        queryset = AbsensiDetail.objects.all()
        return queryset
    
    def get_serializer_class(self):
        #jika method post 

        if self.request.method == "POST":
            return AbsensiSerializer
        return AbsensiDetailSerializer
    

absensi_list_create_view = AbsensiCreateView.as_view()

class AbsensiDetailListView(generics.ListAPIView):
    serializer_class = AbsensiSerializer
    queryset = Absensi.objects.all()


absensi_detail_list_view = AbsensiDetailListView.as_view()