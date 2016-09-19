from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^create_user$', views.create_user, name="create_user"),
    url(r'^login$', views.login_user, name='login'),
    url(r'^', include('django.contrib.auth.urls'))
]