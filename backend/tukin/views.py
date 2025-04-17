from django.shortcuts import render
from django.views import generic
from .models import Tukin
from .forms import TukinForm

# Create your views here.


class TukinListView(generic.ListView):
    model = Tukin
    template_name = "tukin_list.html"
    context_object_name = "tukins"

    def get_queryset(self):
        return Tukin.objects.all().order_by('-kelas_jabatan')
    
    def get_context_data(self, **kwargs):
        
        context =  super().get_context_data(**kwargs)
        context['form'] = TukinForm()

        return context
    
tukin_list_view = TukinListView.as_view()

