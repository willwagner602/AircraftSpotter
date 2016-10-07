__author__ = 'wbw'

from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError


def create_user(request):
    if request.method == 'POST':
        user_info = request.POST

        username = user_info['username']
        password = user_info['password']
        password_confirmation = user_info['password_confirmation']
        email = user_info['email']

        if password != password_confirmation:
            # return error
            return render(request, 'registration/create_user.html', {'error': 'passwords do not match'})
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            print(user)
        except IntegrityError as e:
            print(request.__dict__)
            return render(request, 'registration/create_user.html', {'error': 'This username is not valid'})

        return redirect('/user/login', success = 'User created successfully!', username = user.username)

    else:
        return render(request, 'registration/create_user.html', {})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/login.html', {'display':'user does not exist'})
    else:
        return render(request, 'registration/login.html', {'username': 'username', 'shit':'shit'})


def logout_user(request):
    logout(request)
    return redirect('/')
