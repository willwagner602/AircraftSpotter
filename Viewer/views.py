__author__ = 'wbw'

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User


def create_user(request):
    if request.method == 'POST':
        user_info = request.POST
        username = user_info['email']
        password = user_info['password']
        password_confirmation = user_info['password_confirmation']
        print(user_info)
        return render(request, 'registration/create_user.html', {})
    else:
        return render(request, 'registration/create_user.html', {})