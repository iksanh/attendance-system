# Generated by Django 4.2 on 2025-02-13 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('absensi', '0003_absensidetail_pegawai'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absensidetail',
            name='pegawai',
        ),
    ]
