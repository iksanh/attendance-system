# Generated by Django 4.2 on 2025-04-09 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('absensi', '0004_remove_absensidetail_pegawai'),
    ]

    operations = [
        migrations.AddField(
            model_name='absensi',
            name='jam_kerja',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='absensi',
            name='metode',
            field=models.CharField(choices=[('e-office', 'E-Office'), ('finger', 'Finger Print'), ('manual', 'Manual')], default='manual', max_length=30),
        ),
        migrations.AddField(
            model_name='absensi',
            name='waktu_keluar',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='absensi',
            name='waktu_masuk',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
