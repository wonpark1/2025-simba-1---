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
        password = request.POST.get('password', '')
        confirm  = request.POST.get('confirm', '')

        if username in User.objects.values_list('username', flat=True):
            return JsonResponse({'error': '이미 존재하는 아이디입니다'}, status=777)
        
        if password != confirm:
            return JsonResponse({'error': '비밀번호가 일치하지 않습니다'}, status=777)
        
        #세션에 임시 보관
        request.session['signup_username'] = username     
        request.session['signup_password'] = password     
        return redirect('accounts:signup2')
    
    #GET
    return render(request, 'accounts/SignupPage1.html')

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
        Profile.objects.create(user=user, nickname=nickname)

        request.session.flush() # 세션 정리

        return redirect('accounts:login')
    return render(request, 'accounts/SignupPage2.html')