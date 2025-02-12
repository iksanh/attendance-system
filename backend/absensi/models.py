from django.db import models
from pegawai.models import Pegawai
# Create your models here.


class Absensi (models.Model):
    pegawai  = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        db_table  = "m_absensi"

class MetodeAbsensi(models.TextChoices):
    EOFFICE = "e-office","E-Office"
    FINGER = "finger", "Finger Print"
    MANUAL = "manual","Manual"

class AbsensiDetail(models.Model):

    absensi  = models.ForeignKey(Absensi, on_delete=models.CASCADE)
    metode = models.CharField(max_length=30, choices=MetodeAbsensi.choices, default=MetodeAbsensi.MANUAL)
    waktu_masuk = models.TimeField(null=True, blank=True)
    waktu_keluar = models.TimeField(null=True, blank=True)
    jam_kerja = models.FloatField(null=True, blank=True)
    
    class Meta: 
        db_table = "m_absensi_detail"