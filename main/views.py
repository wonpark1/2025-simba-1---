from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
import re
from django.db.models import Count

# Create your views here.
def mainpage(request):
    return render(request, 'main/mainpage.html')

def commentpage(request):
    sort = request.GET.get('sort','latest')

    if sort == 'likes':
        comments = (Comment.objects
                    .annotate(num_likes=Count('like'))
                    .order_by('-num_likes', '-create_at'))
    else:
        comments = Comment.objects.order_by('-create_at')
    return render(request, 'main/commentpage.html', {'comments': comments, 'cur_sort': sort})

def create(request):
    if request.user.is_authenticated:
        new_comment = Comment()
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.image  = request.FILES.get('image')
        new_comment.create_at = timezone.now()
        new_comment.save()

        return redirect('main:comment_page')
    else:
        return redirect('accounts:login')

def edit(request, id):
    edit_comment = get_object_or_404(Comment, pk=id)

    if request.user.is_authenticated and request.user == edit_comment.writer:
        if request.method == "POST":          
            edit_comment.content = request.POST.get('content', '')
            if 'image' in request.FILES:              
                edit_comment.image = request.FILES['image']
            edit_comment.create_at = timezone.now()
            edit_comment.save()
            return redirect('main:comment_page') 
        
        return render(request, 'main/edit.html', {'comment': edit_comment})
    else:
        return redirect('accounts:login')
    
def delete(request, id):
    delete_comment = Comment.objects.get(pk=id)
    delete_comment.delete()
    return redirect('main:comment_page')

def likes(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user in comment.like.all():
        comment.like.remove(request.user)
    else:
        comment.like.add(request.user)
        if request.user in comment.dislike.all():
            comment.dislike.remove(request.user)

    return redirect('main:comment_page')

def dislikes(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user in comment.dislike.all():
        comment.dislike.remove(request.user)
    else:
        comment.dislike.add(request.user)

        if request.user in comment.like.all():
            comment.like.remove(request.user)

    comment.save()
    return redirect('main:comment_page')