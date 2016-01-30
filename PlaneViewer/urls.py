from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.aircraft_list, name='plane_test'),
    url(r'^aircraft$', views.get_aircraft, name='plane_test'),
]