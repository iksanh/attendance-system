import pandas as pd
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.db import connection
from rest_framework import generics, status
from rest_framework.views import APIView

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Absensi, AbsensiDetail, AbsensiDetailManager
from ..api.serializers import AbsensiSerializer, AbsensiDetailSerializer, PegawaiAbsensiSerializer, AbsensiPivotSerializer
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

        print(file, date, metode)

        if not file:
            return Response({"error": "tidak ada file yang diupload"}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            df = pd.read_excel(file)

            record = 0
            for index, row in df.iterrows():
                nip = str(row['NIP/NIK']).strip()
                pegawai = Pegawai.objects.filter(nip=nip).first()

                if not pegawai:
                    continue

                waktu_masuk = row.get('Waktu Masuk')
                waktu_keluar= row.get('Waktu Keluar')

                waktu_masuk = self.validate_time(waktu_masuk)
                waktu_keluar= self.validate_time(waktu_keluar)

                
                absensi,created = Absensi.objects.get_or_create(
                    pegawai=pegawai, 
                    date= date,
                    metode=metode,
                    waktu_masuk=waktu_masuk,
                    waktu_keluar=waktu_keluar,
                )

                # AbsensiDetail.objects.create(
                #     absensi=absensi, 
                #     metode=metode,
                #     waktu_masuk=waktu_masuk,
                #     waktu_keluar=waktu_keluar
                # )

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


class PegawaiAbsensiAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Define the raw SQL query
        get_tanggal_absensi = request.GET.get('date', None)
        print(get_tanggal_absensi)
        if get_tanggal_absensi:
            try:
                tanggal_absensi = datetime.strptime(get_tanggal_absensi, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        query = """
            SELECT
                p.id,
                p.nama,
                a.date,
                a.metode,
                a.waktu_masuk,
                a.waktu_keluar,
                a.jam_kerja
            FROM
                m_pegawai p
            LEFT JOIN
                m_absensi a ON p.id = a.pegawai_id
                AND a.date = %s
                AND a.metode = %s
            WHERE
                p.status = true
            ORDER BY
                p.id, a.date;
        """

        # Execute the query using Django's connection cursor
        with connection.cursor() as cursor:
            cursor.execute(query, [tanggal_absensi, 'manual'])
            rows = cursor.fetchall()

        # Process the results into a list of dictionaries
        results = []
        for row in rows:
            results.append({
                'id': row[0],
                'nama': row[1],
                'date': row[2],
                'metode': row[3],
                'waktu_masuk': row[4],
                'waktu_keluar': row[5],
                'jam_kerja': row[6],
            })

        # Use the serializer to format the data
        serializer = PegawaiAbsensiSerializer(results, many=True)

        # Return the results as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)

        pegawai = get_object_or_404(Pegawai, id=data.get('id'))

        # Convert the date string to a Date object
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        # Create a new Absensi instance

        # try to get an existing Absensi record or create a new one if it does't exist 
        absensi = Absensi.objects.filter(pegawai=pegawai, date=date_obj).first()

        if absensi:
            print('UPDATEDE')
            absensi.metode = data['metode']
            absensi.waktu_masuk=data['waktu_masuk']
            absensi.waktu_keluar=data['waktu_keluar']
            absensi.save()
            status_code = status.HTTP_200_OK
        else:
            print('CREATED')
            absensi = Absensi(
                pegawai=pegawai,
                date=date_obj,
                metode=data['metode'],
                waktu_masuk=data['waktu_masuk'],
                waktu_keluar=data['waktu_keluar']
            )
            absensi.save()
            status_code = status.HTTP_201_CREATED
        
        # Save the Absensi instance to the database
       
        
        # Return the saved data in the response
        return Response({
            'id': absensi.id,
            'pegawai': absensi.pegawai.id,
            'date': absensi.date,
            'metode': absensi.metode,
            'waktu_masuk': absensi.waktu_masuk,
            'waktu_keluar': absensi.waktu_keluar
        }, status=status_code)
        
    
    
    
pegawai_absensi_api = PegawaiAbsensiAPI.as_view()


class AbsensiPivotView(APIView):
    def get(self, request, *args, **kwargs):
        tanggal_absen = request.query_params.get('tanggal')
        if not tanggal_absen:
            return Response({"error": "Parameter 'tanggal' is required."}, status=status.HTTP_400_BAD_REQUEST)

        result = Absensi.objects.search_pegawai_absensi_pivot(tanggal_absen)
        serializer = AbsensiPivotSerializer(result, many=True)
        return Response(serializer.data)
    
absensi_pivot_api_view = AbsensiPivotView.as_view()