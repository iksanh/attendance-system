from django.shortcuts import render
from rest_framework import generics
from .models import Pegawai
from .serializers import PegawaiSerializer

# View untuk pegawai
class PegawaiListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PegawaiSerializer
    queryset = Pegawai.objects.all


pegawai_list_create_view = PegawaiListCreateAPIView.as_view()