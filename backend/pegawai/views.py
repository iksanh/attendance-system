from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status, views
from rest_framework.response import Response
from .models import Pegawai
from .serializers import PegawaiSerializer, PegawaiUploadCSVSerializer
import csv

# View untuk pegawai
class PegawaiListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PegawaiSerializer
    queryset = Pegawai.objects.all()


pegawai_list_create_view = PegawaiListCreateAPIView.as_view()

class PegawaiRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pegawai.objects.all()
    serializer_class = PegawaiSerializer
    lookup_field = 'id'

    

pegawai_retrive_update_delete_view = PegawaiRetrieveUpdateDestroyAPIView.as_view()


class PegawaiCSVUploadView(generics.GenericAPIView):
    def post(self, request, format=None):
        serializer = PegawaiUploadCSVSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            csv_file = serializer.validated_data["file"]
            csv_data = csv_file.read().decode("utf-8")
            reader = csv.DictReader(csv_data.splitlines())
            try:
                #baca dan decode csv file 
                for row in reader:
                    Pegawai.objects.create(
                        nip=row["nip"],
                        nama=row["nama"],
                        jabatan=row["jabatan"],
                        grade=int(row["grade"])
                    )
                
                return Response({"message": "Berhasil import data pegawai"}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


    def get(self, request, *args, **kwargs):
        filename = "pegawai_data.csv"

        #membuat http response 
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        #buat csv writer 

        writer = csv.writer(response)
        writer.writerow(["nip","nama", "jabatan", "grade"])
        
        pegawai_data = Pegawai.objects.all()
        for pegawai in  pegawai_data:
            writer.writerow([pegawai.nip, pegawai.nama, pegawai.jabatan, pegawai.grade])
        
        return response

pegawai_upload_csv_view = PegawaiCSVUploadView.as_view()