from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
import re
# Create your views here.
def mainpage(request):
    return render(request, 'main/mainpage.html')

def comentpage(request):
    comments = Comment.objects.all().order_by('-create_at')
    return render(request, 'main/commentpage.html', {'comments': comments})

def create(request):
    if request.user.is_authenticated:
        new_comment = Comment()
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.create_at = timezone.now()
        new_comment.save()

        return redirect('main:comment_page')
    else:
        return redirect('accounts:login')

def update(request, id):
    update_comment = Comment.objects.get(pk=id)

    if request.user.is_authenticated and request.user == update_comment.writer:
        update_comment.content = request.POST['content']
        update_comment.create_at = timezone.now()

        update_comment.save()

        update_comment.tags.clear()
        update_words = re.split(r'[ \t\n]+', update_comment.content)
        update_tag_list = []

        for w in update_words:
            if len(w) > 0:
                if w[0] == '#':
                    update_tag_list.append(w[1:])
                    for t in update_tag_list:
                        tag, boolean = Tag.objects.get_or_create(name=t)
                        update_comment.tags.add(tag.id)

        return redirect('main:detail', update_comment.id)
    else:
        return redirect('accounts:login')

def update(request, id):
    update_comment = Comment.objects.get(pk=id)

    if request.user.is_authenticated and request.user == update_comment.writer:
        update_comment.content = request.POST['content']
        update_comment.create_at = timezone.now()
        update_comment.save()

        return redirect('main:comment_page', update_comment.id)
    else:
        return redirect('accounts:login')

def delete(request, id):
    delete_comment = Comment.objects.get(pk=id)
    delete_comment.delete()

    return redirect('main:comment_page')
    
def delete(request, id):
    delete_comment = Comment.objects.get(pk=id)
    delete_comment.delete()

    return redirect('main:comment_page')


def edit(request, id):
    edit_comment = Comment.objects.get(pk=id)

    if request.user.is_authenticated and request.user == edit_comment.writer:
        return render(request, 'main/edit.html', {'comment': edit_comment})
    else:
        return redirect('accounts:login')