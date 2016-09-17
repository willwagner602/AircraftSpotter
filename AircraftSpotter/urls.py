from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.aircraft_test, name='aircraft_spotter'),
    url(r'^data/(?P<current_image_id>[0-9]+)$', views.aircraft_data, name='aircraft_data'),
    url(r'^error_report/(?P<current_image_id>[0-9]+)$', views.error_report, name='error_report'),
    url(r'^manager$', views.data_manager, name='data_manager'),
    url(r'^data(?P<current_image_id>[0-9]+)$', views.aircraft_data, name='aircraft_data'),
    url(r'^history', views.history, name='history'),
]
