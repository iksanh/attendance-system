from django.urls import path
from .views import tukin_list_view


urlpatterns = [
    path('', tukin_list_view, name='tukin-list'),
]