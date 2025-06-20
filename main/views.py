from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
import re
from django.db.models import Count
from datetime import datetime

# Create your views here.
def mainpage(request):
    user = request.user
    profile = request.user.profile
    now = datetime.now()
    current_month = now.month
    month_obj = Month.objects.get(number=current_month)
    event_lookcards = LookCard.objects.filter(event__month=month_obj).order_by('event__title')

    return render(request, 'main/mainpage.html', {'month': current_month, 'user': user, 'profile': profile, 'event': event_lookcards})

def commentpage(request, lookcard_id):
    sort = request.GET.get('sort','latest')
    lookcard = get_object_or_404(LookCard, id=lookcard_id)
    comments = lookcard.comments.all()

    if sort == 'likes':
        comments = comments.annotate(like_count=Count('like')).order_by('-like_count')
    elif sort == 'latest':
        comments = comments.order_by('-create_at')

    return render(request, 'main/CommentPage.html', {
        'lookcard': lookcard,
        'comments': comments,
        'sort': sort
    })

def create(request, lookcard_id):
    if request.user.is_authenticated:
        new_comment = Comment()
        new_comment.look_card = get_object_or_404(LookCard, id=lookcard_id)
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.image  = request.FILES.get('image')
        new_comment.create_at = timezone.now()
        new_comment.save()

        return redirect('main:lookcard_detail', lookcard_id=lookcard_id)
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
            return redirect('main:comment_page', lookcard_id=edit_comment.look_card.id) 
        
        return render(request, 'main/edit.html', {'comment': edit_comment})
    else:
        return redirect('accounts:login')
    
def delete(request, id):
    delete_comment = Comment.objects.get(pk=id)
    delete_comment.delete()
    return redirect('main:comment_page', lookcard_id=delete_comment.look_card.id)

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

def lookcard(request, lookcard_id):
    lookcard = get_object_or_404(LookCard, id=lookcard_id)
    items = lookcard.items.all()
    comments = lookcard.comments.all()

    if request.method == 'POST':
        comment_content = request.POST.get('comment_content', '')
        if comment_content:
            new_comment = Comment(
                look_card=lookcard,
                writer=request.user,
                content=comment_content,
                create_at=timezone.now()
            )
            new_comment.save()
            return redirect('main:lookcard', lookcard_id=lookcard.id)

    return render(request, 'main/LookCardPage.html', {'lookcard': lookcard, 'items': items, 'comments': comments})