from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from .models import User

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        res_data = {}

        if not(username and password):
            res_data['error'] = "모든 값을 입력해야 합니다."
            return render(request, 'signup.html', res_data)
        else:
            user = User(
                username = username,
                password = make_password(password),
            )
            print(">> User Save Complete")
            user.save()
        return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = make_password(request.POST['password'])
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print(">> User Login Complete")
            return redirect('home')
    print("<< Login Fail!")
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')