from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.aircraft_list, name='plane_test'),
    url(r'^data$', views.data_manager, name='get_aircraft'),
]