from django.contrib import admin
from django import forms
from .models import Absensi, AbsensiDetail, Pegawai, MetodeAbsensi

class AbsensiForm(forms.ModelForm):
    """ Custom form to input date and method in the main form """
    metode = forms.ChoiceField(choices=MetodeAbsensi.choices)

    class Meta:
        model = Absensi
        fields = ['date']

    def save(self, commit=True):
        """ Override save method to apply metode to all AbsensiDetail """
        instance = super().save(commit=False)
        if commit:
            instance.save()
            for pegawai in Pegawai.objects.all():
                AbsensiDetail.objects.update_or_create(
                    absensi=instance,
                    pegawai=pegawai,  # ✅ Assign Pegawai explicitly
                    defaults={'metode': self.cleaned_data['metode']}
                )
        return instance

class AbsensiDetailInline(admin.TabularInline):
    model = AbsensiDetail
    extra = 0  # Don't add extra empty forms
    fields = ('pegawai_display','waktu_masuk', 'waktu_keluar')  # ✅ Pegawai now works
    readonly_fields = ('pegawai_display',)

   
    def pegawai_display(self, obj):
        return Pegawai.objects.nama
    
    pegawai_display.short_description = "Pegawai"

    

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    form = AbsensiForm  # Use custom form
    list_display = ('date',)
    inlines = [AbsensiDetailInline]  # Show all employees in inline form


