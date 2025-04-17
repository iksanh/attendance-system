from .models import Absensi, AbsensiDetail
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from .forms import AbsensiForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from pegawai.models import Pegawai

class AbsensiCreateView(FormView):
    # model = Absensi
    form_class = AbsensiForm
    template_name = "absensi_form.html"
    success_url = reverse_lazy('absensi-list')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # context['pegawais'] = Pegawai.objects.filter(status=True).order_by('id')
        context['absensi'] = Pegawai.objects.prefetch_related('absensi_set').all().order_by('id')
        context['pegawai_data'] = Pegawai.objects.prefetch_related('absensi_set').all().order_by('id')


        return context
    
absensi_create_view = AbsensiCreateView.as_view()

class AbsensiListView(ListView):
    model = Absensi
    template_name = "absensi_list.html"
    context_object_name = "absensi_list"

    def get_queryset(self):
        return Absensi.objects.all()
    
absensi_list_view = AbsensiListView.as_view()


