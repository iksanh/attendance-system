from django.shortcuts import render
from rest_framework import generics
from .models import Absensi
from .serializers import AbsensiSerializer

# Create your views here.

class AbsensiCreateView(generics.ListCreateAPIView):
    qs = Absensi.objects.all()
    serializer_class = AbsensiSerializer


absensi_list_create_view = AbsensiCreateView.as_view()
