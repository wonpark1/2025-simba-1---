from django.shortcuts import render, redirect
from django.contrib import auth #logout을 위해 필요
from django.contrib.auth.models import User #sign up을 위해 필요
from .models import Profile
from django.http import JsonResponse
import random

def accountpage(request):
    return render(request, 'accounts/accounts.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip() #strip: 사용자가 띄어쓰기를 실수로 넣어도 앞뒤 공백 제거 후 인증 시도
        password = request.POST.get('password', '').strip()

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main:mainpage')
        else:
            return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호를 확인하세요.'})

    elif request.method == 'GET':
        return render(request, 'accounts/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')

def Signup1(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm  = request.POST.get('confirm', '')

        
        
        # 세션에 임시 보관
        request.session['signup_username'] = username     
        request.session['signup_password'] = password     
        return redirect('accounts:signup2')
    
    # GET
    return render(request, 'accounts/SignupPage1.html')

def check_username(request):
    username = request.GET.get('username', '').strip()
    exist = User.objects.filter(username=username).exists()
    return JsonResponse({'exists':exist})

def Signup2(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname', '').strip()

        # 1단계 세션값
        username = request.session.get('signup_username')
        password = request.session.get('signup_password')
        if not (username and password):
            return redirect('accounts:signup1')   # 세션 만료 대비

        # User&Profile 생성
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, nickname=nickname)

        user.save()
        profile.save()
        auth.login(request, user)

        request.session.pop('signup_username', None) # 세션 정리
        request.session.pop('signup_password', None) # 세션 정리

        return redirect('main:mainpage')
    return render(request, 'accounts/SignupPage2.html')