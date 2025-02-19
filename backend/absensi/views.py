from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Absensi, AbsensiDetail, AbsensiDetailManager
from .serializers import AbsensiSerializer, AbsensiDetailSerializer

# Create your views here.

class AbsensiCreateView(generics.ListCreateAPIView):

    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        tanggal_absen = self.request.query_params.get('tanggal_absen')
        pegawai_id = self.request.query_params.get('pegawai_id')
      
        return AbsensiDetail.objects.search_by_tanggal_absen(tanggal_absen, pegawai_id)
    
    def get_serializer_class(self):
        #jika method post 

        if self.request.method == "POST":
            return AbsensiSerializer
        return AbsensiDetailSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

absensi_list_create_view = AbsensiCreateView.as_view()

class AbsensiDetailListView(generics.ListAPIView):
    serializer_class = AbsensiSerializer
    queryset = Absensi.objects.all()


absensi_detail_list_view = AbsensiDetailListView.as_view()