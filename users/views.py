from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def mypage(request):
    user = request.user
    context = {
        'user':user,
        'profile':user.profile,
    }
    return render(request, 'users/mypage.html', context)

def logout(request):
    auth.logout(request)
    return redirect('accounts:login')

def mycomment(request):
    user = request.user
    comments = user.comment_set.all()
    context = {
        'user': user,
        'comments': comments,
    }
    return render(request, 'users/MyCommentPage.html', context)