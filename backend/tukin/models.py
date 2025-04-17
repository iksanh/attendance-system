from django.db import models

# Create your models here.

class Tukin(models.Model):
    kelas_jabatan = models.IntegerField(unique=True)
    jumlah_tunjangan = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        db_table="m_tukin"