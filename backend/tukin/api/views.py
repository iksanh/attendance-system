from rest_framework import generics
from .serializers import TukinSerializer
from tukin.models import Tukin


#list dan create 
class TukinListCreateView(generics.ListCreateAPIView):
    queryset = Tukin.objects.all()
    serializer_class = TukinSerializer

tukin_list_create_view = TukinListCreateView.as_view()

class TukinRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tukin.objects.all()
    serializer_class = TukinSerializer

tukin_retrive_update_destroy_view = TukinRetriveUpdateDestroyView.as_view()





