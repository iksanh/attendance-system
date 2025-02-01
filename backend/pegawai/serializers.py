from rest_framework import serializers
from .models import Pegawai


class PegawaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pegawai
        fields = '__all__'

        