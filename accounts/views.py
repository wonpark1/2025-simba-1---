from django.shortcuts import render, redirect
from django.contrib import auth #logout을 위해 필요
from django.contrib.auth.models import User #sign up을 위해 필요
from .models import Profile

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main:mainpage')
        else:
            return render(request, 'accounts/login.html')
        
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')

def signup(request):
    if request.method == 'POST':

        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
            nickname=request.POST['nickname']
            gender=request.POST['gender']
            email=request.POST['email']

            profile = Profile(user=user, nickname=nickname, gender=gender, email=email)
            profile.save()

            auth.login(request, user)
            return redirect('/')
        
    return render(request, 'accounts/signup.html')