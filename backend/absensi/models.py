from django.db import models, connection
from django.core.exceptions import ValidationError
from pegawai.models import Pegawai
# Create your models here.

class MetodeAbsensi(models.TextChoices):
    OPTION = "","--PILIH METODE--"
    EOFFICE = "e-office","E-Office"
    FINGER = "finger", "Finger Print"
    MANUAL = "manual","Manual"

class AbsensiDetailManager(models.Manager):
    def search_by_tanggal_absen(self, tanggal_absen=None, pegawai_id=None):
        
        queryset = self.all()
        if tanggal_absen:
            queryset = queryset.filter(absensi__date=tanggal_absen)

        if pegawai_id:
            print("test")
            queryset = queryset.filter(absensi__pegawai_id=pegawai_id
            )
        return queryset

class AbsensiManager(models.Manager):
    def search_by_tanggal_absen(self, tanggal_absen=None, pegawai_id=None):
        
        queryset = self.all()
        if tanggal_absen:
            queryset = queryset.filter(date=tanggal_absen)

        if pegawai_id:
            print("test")
            queryset = queryset.filter(pegawai_id=pegawai_id
            )
        return queryset
    
    def search_pegawai_absensi_pivot(self, tanggal_absen):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.id AS pegawai_id,
                    p.nama,
                    MAX(a.waktu_masuk) FILTER (WHERE a.metode = 'manual') AS manual_masuk,
                    MAX(a.waktu_keluar) FILTER (WHERE a.metode = 'manual') AS manual_keluar,
                    MAX(a.waktu_masuk) FILTER (WHERE a.metode = 'e-office') AS eoffice_masuk,
                    MAX(a.waktu_keluar) FILTER (WHERE a.metode = 'e-office') AS eoffice_keluar,
                    MAX(a.waktu_masuk) FILTER (WHERE a.metode = 'finger') AS finger_masuk,
                    MAX(a.waktu_keluar) FILTER (WHERE a.metode = 'finger') AS finger_keluar
                FROM m_pegawai p
                LEFT JOIN m_absensi a ON p.id = a.pegawai_id AND a.date = %s
                WHERE p.status = TRUE
                GROUP BY p.id, p.nama
                ORDER BY p.id
            """, [tanggal_absen])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


class Absensi(models.Model):
    pegawai  = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    date = models.DateField()
    metode = models.CharField(max_length=30, choices=MetodeAbsensi.choices, default=MetodeAbsensi.MANUAL)
    waktu_masuk = models.TimeField(null=True, blank=True)
    waktu_keluar = models.TimeField(null=True, blank=True)
    jam_kerja = models.FloatField(null=True, blank=True)

    class Meta:
        db_table  = "m_absensi"
    
    objects = AbsensiManager()

class AbsensiDetail(models.Model):

    absensi  = models.ForeignKey(Absensi, on_delete=models.CASCADE)
    metode = models.CharField(max_length=30, choices=MetodeAbsensi.choices, default=MetodeAbsensi.MANUAL)
    waktu_masuk = models.TimeField(null=True, blank=True)
    waktu_keluar = models.TimeField(null=True, blank=True)
    jam_kerja = models.FloatField(null=True, blank=True)
    
    class Meta: 
        db_table = "m_absensi_detail"

      
    objects = AbsensiDetailManager()
