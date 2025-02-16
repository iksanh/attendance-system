from rest_framework import serializers

from .models import Absensi, AbsensiDetail, MetodeAbsensi
from pegawai.serializers import PegawaiSerializer
from pegawai.models import Pegawai
from datetime import datetime

class AbsensiDetailSerializer(serializers.ModelSerializer):
    pegawai = serializers.SerializerMethodField(read_only=True)
    # pegawai = PegawaiSerializer(many=True, read_only=True)
    tanggal_absen = serializers.SerializerMethodField(read_only=True)
    absensi_id = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AbsensiDetail
        fields = ['absensi_id', 'tanggal_absen','pegawai','metode', 'waktu_masuk', 'waktu_keluar', 'jam_kerja']

    def get_pegawai(self,obj):
        return {
            'id' : obj.absensi.pegawai.id,
            'nama' : obj.absensi.pegawai.nama
        }
    def get_absensi_id(self, obj):
        return obj.absensi.id

    def get_tanggal_absen(self, obj):
        return obj.absensi.date
class AbsensiSerializer(serializers.ModelSerializer):
    absensi_detail = AbsensiDetailSerializer(write_only=True)
    pegawai_id = serializers.PrimaryKeyRelatedField(queryset=Pegawai.objects.all(), write_only=True, source='pegawai')
    pegawai = PegawaiSerializer(read_only=True)

    class Meta:
        model = Absensi
        fields = ['pegawai_id','pegawai', 'date', 'absensi_detail']

   
    def create(self, validated_data):
        absensi_detail_data = validated_data.pop('absensi_detail')

        absensi = Absensi.objects.create(**validated_data)

        print(absensi)
        
        waktu_masuk = absensi_detail_data.get('waktu_masuk')
        waktu_keluar = absensi_detail_data.get('waktu_keluar')
        jam_kerja = None

        if waktu_masuk and waktu_keluar:
            fmt = "%H:%M:%S"
            waktu_masuk = datetime.strptime(str(waktu_masuk), fmt)
            waktu_keluar = datetime.strptime(str(waktu_keluar), fmt)
            jam_kerja = (waktu_keluar-waktu_masuk).seconds / 3600
        
        AbsensiDetail.objects.create(
            absensi=absensi,
            metode=absensi_detail_data.get('metode', MetodeAbsensi.MANUAL),
            waktu_masuk=waktu_masuk,
            waktu_keluar=waktu_keluar,
            jam_kerja=jam_kerja
            )


        return absensi
