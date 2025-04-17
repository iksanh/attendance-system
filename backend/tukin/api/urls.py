from django.urls import path
from .views import tukin_list_create_view, tukin_retrive_update_destroy_view


urlpatterns = [
    path('', tukin_list_create_view, name='tukin-list-create'),
    path('<int:pk>/', tukin_retrive_update_destroy_view, name='tukin-detail')
]