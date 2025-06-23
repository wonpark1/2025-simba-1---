from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.views import pushpagestack, poppagestack, previouspage

@login_required
def mypage(request):
    pushpagestack(request, request.get_full_path())
    user = request.user
    context = {
        'user':user,
        'profile':user.profile,
    }
    return render(request, 'users/mypage.html', context)

def logout(request):

    auth.logout(request)
    return redirect('accounts:accountpage')

def mycomment(request):
    pushpagestack(request, request.get_full_path())
    user = request.user
    comments = user.comment_set.all()
    context = {
        'user': user,
        'comments': comments,
    }
    return render(request, 'users/MyCommentPage.html', context)