from django import forms
from .models import Absensi, AbsensiDetail, MetodeAbsensi
from pegawai.models import Pegawai

class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'metode': forms.Select(attrs={ 'class': 'form-control'})
        }


