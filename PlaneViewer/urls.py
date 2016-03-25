from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.aircraft_display, name='aircraft_test'),
    url(r'^data$', views.data_manager, name='aircraft_data'),
]