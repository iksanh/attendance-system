from django.db import models
from pegawai.models import Pegawai
# Create your models here.


class Absensi (models.Model):
    pegawai  = models.ForeignKey(Pegawai, on_delete=models.CASCADE)
    date = models.DateField()


    class Meta:
        db_table  = "m_absensi"