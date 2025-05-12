from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def mypage(request):
    context = {
        'user':request.user,
    }
    return render(request, 'users/mypage.html', context)