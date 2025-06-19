from django.shortcuts import render, redirect
from django.contrib import auth #logout을 위해 필요
from django.contrib.auth.models import User #sign up을 위해 필요
from .models import Profile
import random

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

def Signup1(request):
    

    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            request.session['username'] = request.POST['username']
            request.session['password'] = request.POST['password']
            request.session['confirm'] = request.POST['confirm']
            return redirect('accounts:signup2')
        
        else:
            return render(request, 'accounts/SignupPage1.html', {'error'})
        
    username = request.session.get('username')
    password = request.session.get('password')
    email = request.session.get('email')

        
    return render(request, 'accounts/SignupPage1.html')

def Signup2(request):
    if request.method == 'POST':
        request.session['gender'] = request.POST['gender']
        request.session['email'] = request.POST['email']
        
        return redirect('accounts:signup3')
    
    return render(request, 'accounts/SignupPage2.html')

def Signup3(request):
    default_image = [
        '/media/profile/pfp1.png',
        '/media/profile/pfp2.png',
        '/media/profile/pfp3.png'
    ]

    if request.method == 'POST':
        
        username = request.session.get('username')
        password = request.session.get('password')
        confirm = request.session.get('confirm')
        email = request.session.get('email')
        nickname = request.POST['nickname']
        gender = request.session.get('gender')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        pfp = request.FILES.get('pfp')
        if pfp:
            profile = Profile(user=user, nickname=nickname, gender=gender, pfp=pfp)

        else:
            pfp = random.choice(default_image)
            profile = Profile(user=user, nickname=nickname, gender=gender, pfp=pfp)
           
        profile.save()
        auth.login(request, user)
        return redirect('/')

    return render(request, 'accounts/SignupPage3.html')