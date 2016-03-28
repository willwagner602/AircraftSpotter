from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^create_user$', views.create_user, name="create_user"),
    url(r'^', include('django.contrib.auth.urls'))
]