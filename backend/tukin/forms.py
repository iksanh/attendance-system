from django import forms
from .models import Tukin
from attendence.forms import BasicFormStyle

class TukinForm(BasicFormStyle):
    class Meta:
        model = Tukin
        fields = ['kelas_jabatan', 'jumlah_tunjangan']

        # widgets = {
        #     'kelas_jabatan': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'jumlah_tunjangan': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        # }