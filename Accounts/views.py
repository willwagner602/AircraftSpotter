__author__ = 'wbw'

from django.shortcuts import render
from django.contrib.auth.models import User


def create_user(request):
    if request.method == 'POST':
        user_info = request.POST

        # ToDo: Figure out why this errors the the first time a user logs in and never again
        username = user_info['email']
        password = user_info['password']
        password_confirmation = user_info['password_confirmation']

        print(user_info)

        if password != password_confirmation:
            # return error
            return render(request, 'registration/create_user.html', {'error': 'passwords do not match'})

        user = User.objects.create_user(username, email=username, password=password)

        return render(request, 'registration/login.html', {'success': 'User created successfully!'})

    else:
        return render(request, 'registration/create_user.html', {})