from django import forms
from .models import Pegawai

class PegawaiForm(forms.ModelForm):
    class Meta:
        model = Pegawai
        fields = ['nip','nama','jabatan','grade']

        widgets = {
            'nip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan NIP'}),
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Nama'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Jabatan'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Grade'}),
        }
        labels = {
            'nip': 'NIP',
            'nama': 'Nama Lengkap',
            'jabatan': 'Jabatan',
            'grade': 'Grade',
        }
        
    def clean_nip(self):
        nip = self.cleaned_data.get('nip')
        if not nip.isdigit():
            raise forms.ValidationError("NIP harus berupa angka.")
        if len(nip) < 8:
            raise forms.ValidationError("NIP harus memiliki minimal 8 karakter.")
        return nip