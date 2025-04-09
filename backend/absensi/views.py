from .models import Absensi, AbsensiDetail
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, DetailView, FormView
from .forms import AbsensiForm, AbsensiDetailForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from pegawai.models import Pegawai

class AbsensiCreateView(CreateView):
    model = Absensi
    form_class = AbsensiForm
    template_name = "absensi_form.html"
    success_url = reverse_lazy('absensi-list')


    def form_valid(self, form):
        response =  super().form_valid(form)

        #Create Absensi Detail Entry

        metode = self.request.POST.get('metode','manual')
        waktu_masuk = self.request.POST.get('waktu_masuk', None)
        waktu_keluar = self.request.POST.get('waktu_keluar', None)

        AbsensiDetail.objects.create(
            absensi=self.object,
            metode=metode,
            waktu_masuk=waktu_masuk if waktu_masuk else None,
            waktu_keluar=waktu_keluar if waktu_keluar else None,
        )

        return response
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["absensi_detail_form"] = AbsensiDetailForm()
        return context
    
absensi_create_view = AbsensiCreateView.as_view()

class AbsensiListView(ListView):
    model = Absensi
    template_name = "absensi_list.html"
    context_object_name = "absensi_list"

    def get_queryset(self):
        return Absensi.objects.prefetch_related("absensidetail_set").all()
    
absensi_list_view = AbsensiListView.as_view()


class AbsensiDetailView(FormView):
    template_name = "absensi_detail_form.html"
    form_class = AbsensiDetailForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['pegawai_list'] = Pegawai.objects.all()

        return context
    

    def form_valid(self, form):

        date = self.request.POST.get('date')
        metode = self.request.POST.get('metode')
        pegawai_ids = self.request.POST.getlist('pegawai')


        if date and metode and pegawai_ids:
            for pegawai_id in pegawai_ids:
                pegawai = Pegawai.objects.get(id=pegawai_id)

                #buat absensi 
                absensi = Absensi.objects.create(pegawai=pegawai, date=date)
        
                # Create AbsensiDetail instance
                absensi_detail = AbsensiDetail.objects.create(
                    absensi=absensi,
                    metode=metode,
                    waktu_masuk=self.request.POST.get('waktu_masuk'),
                    waktu_keluar=self.request.POST.get('waktu_keluar'),
                    jam_kerja=self.request.POST.get('jam_kerja'),
                )

            messages.success(self.request, "Absensi berhasil disimpan!")
            return redirect('absensi-list')  # Adjust the redirect URL as needed
        else:
            messages.error(self.request, "Please fill all fields.")

        return redirect('absensi-detail')  # In case of failure or incomplete data

    def form_invalid(self, form):
        # In case the form is invalid, show an error message
        messages.error(self.request, "There was an error with the form. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))