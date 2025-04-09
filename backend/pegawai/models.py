from django.db import models

# Create your models here.


#model for jabatan 
class Pegawai(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    grade = models.IntegerField()
    status = models.BooleanField(default=True)
    class Meta:
        db_table = "m_pegawai"

    def __str__(self):
        return f"{self.nama}"