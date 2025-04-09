from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from .models import Pegawai
from .forms import PegawaiForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


class PegawaiListView(ListView):
    model = Pegawai
    template_name = "list.html"
    context_object_name = "pegawais"

    def get_queryset(self):
        return Pegawai.objects.filter(status=True).order_by('id')

pegawai_list_view = PegawaiListView.as_view()


class PegawaiCreateView(CreateView):
    model = Pegawai
    form_class = PegawaiForm
    template_name = 'pegawai_form.html'
    success_url = reverse_lazy('pegawai-list')
    
pegawai_create_view = PegawaiCreateView.as_view()


class PegawaiUpdateView(UpdateView):
    model = Pegawai
    form_class = PegawaiForm
    template_name = "pegawai_form.html"
    # success_url = reverse_lazy('pegawai-list')
    
    def get_success_url(self):
        # Get the ID of the updated pegawai and include it as a query parameter
        return f'{reverse_lazy("pegawai-list")}?highlight={self.object.id}'

pegawai_update_view = PegawaiUpdateView.as_view()


class PegawaiDeleteView(DeleteView):
    model = Pegawai
    success_url = reverse_lazy('pegawai-list')

pegawai_delete_view = PegawaiDeleteView.as_view()

class PegawaiDeactivateView(View):
    def post(self, request, pk):
        pegawai = get_object_or_404(Pegawai, pk=pk)
        pegawai.status=False
        pegawai.save()
        messages.success(request, f"Pegawai {pegawai.nama} telah dinonaktifkan.")
        return redirect(reverse_lazy('pegawai-list'))
    

pegawai_deactivate_view = PegawaiDeactivateView.as_view()
        