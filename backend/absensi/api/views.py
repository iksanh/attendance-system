import pandas as pd
from datetime import datetime
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Absensi, AbsensiDetail, AbsensiDetailManager
from ..api.serializers import AbsensiSerializer, AbsensiDetailSerializer
from pegawai.models import Pegawai

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

class AbsensiUploadExcelFile(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        date = request.data.get('date')
        metode = request.data.get('metode')

        if not file:
            return Response({"error": "tidak ada file yang diupload"}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            df = pd.read_excel(file)

            record = 0
            for index, row in df.iterrows():
                nip = str(row['nip']).strip()
                pegawai = Pegawai.objects.filter(nip=nip).first()

                if not pegawai:
                    continue

                waktu_masuk = row.get('waktu_masuk')
                waktu_keluar= row.get('waktu_keluar')

                waktu_masuk = self.validate_time(waktu_masuk)
                waktu_keluar= self.validate_time(waktu_keluar)

                
                absensi,created = Absensi.objects.get_or_create(
                    pegawai=pegawai, 
                    date= date
                )

                AbsensiDetail.objects.create(
                    absensi=absensi, 
                    metode=metode,
                    waktu_masuk=waktu_masuk,
                    waktu_keluar=waktu_keluar
                )

                record +=1
            return Response({"message": f"Data Absensi berhasil disimpan total {record}"}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def validate_time(self, time_value):
        """Convert time value to correct format or None if invalid"""
        if pd.isna(time_value) or str(time_value).strip() == "-":
            return None  # Handle missing or invalid time
        try:
            return datetime.strptime(str(time_value), "%H:%M:%S").time()  # Ensure valid time format
        except ValueError:
            return None  # Return None if format is incorrect

absensi_upload_view = AbsensiUploadExcelFile.as_view()
