from django import forms
from .models import Absensi, AbsensiDetail, MetodeAbsensi
from pegawai.models import Pegawai

class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ['pegawai', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date', 'class': 'form-control'})
        }


# class AbsensiDetailForm(forms.ModelForm):
#     class Meta: 
#         model = AbsensiDetail
#         fields =['metode', 'waktu_masuk', 'waktu_keluar', 'jam_kerja']
#         widgets = {
#             'metode': forms.Select(choices=MetodeAbsensi.choices, attrs={'class':'form-control'}),
#             'waktu_masuk': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'waktu_keluar': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'jam_kerja': forms.NumberInput(attrs={'class': 'form-control'}),
#         }


class AbsensiDetailForm(forms.ModelForm):
    class Meta:
        model = AbsensiDetail
        fields = ['absensi', 'metode', 'waktu_masuk', 'waktu_keluar', 'jam_kerja']

    # You will need to define a custom field for the Pegawai model to show a list of all employees
    pegawai = forms.ModelChoiceField(queryset=Pegawai.objects.all(), required=True, label="Pegawai")
    metode = forms.ChoiceField(choices=MetodeAbsensi.choices, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form as necessary, you can add choices or validators here
        self.fields['metode'].choices = MetodeAbsensi.choices