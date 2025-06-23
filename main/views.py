from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from django.db.models import Count
from datetime import datetime

# Create your views here.
def pushpagestack(request, current_page):
    stack = request.session.get('page_stack', [])
    if not stack or stack[-1] != current_page:
        stack.append(current_page)
        request.session['page_stack'] = stack

def poppagestack(request):
    stack = request.session.get('page_stack', [])
    if stack:
        stack.pop()
        request.session['page_stack'] = stack
        return redirect(stack[-1])
    else:
        print("에러가 발생했습니다. 다시 시도해주세요.")
        return redirect('main:mainpage')


def previouspage(request):
    return poppagestack(request)
    
def mainpage(request):
    pushpagestack(request, request.path)

    user = request.user
    profile = request.user.profile
    now = datetime.now()
    today_date = now.day
    current_month = now.month
    month_obj = Month.objects.get(number=current_month)

    event_lookcards = LookCard.objects.filter(
        event__month=month_obj,
        event__end__gte=today_date
    ).order_by('event__title')

    for event in event_lookcards:
        if event.event.start == 1:
            if event.event.end == 10:
                event.period = '초'
            elif event.event.end == 20:
                event.period = '초중순'
        elif event.event.start == 11 and event.event.end == 20:
            event.period = '중'
        elif event.event.start == 21 and event.event.end == 31:
            event.period = '말'

    scheduled_events = []

    if not event_lookcards:
        next_month_num = current_month + 1 if current_month < 12 else 1
        next_month_obj = Month.objects.get(number=next_month_num)
        scheduled_events = Event.objects.filter(month=next_month_obj).order_by('start')

    return render(request, 'main/mainpage.html', {
        'month': current_month,
        'user': user,
        'profile': profile,
        'event': event_lookcards,
        'scheduled_events': scheduled_events,
    })

def commentpage(request, lookcard_id):
    pushpagestack(request, request.get_full_path())

    sort = request.GET.get('sort','latest')
    lookcard = get_object_or_404(LookCard, id=lookcard_id)
    same_event_lookcards = LookCard.objects.filter(event__title=lookcard.event.title)
    comments = Comment.objects.filter(look_card__in=same_event_lookcards).order_by('-create_at')
    writers = comments.values_list('writer__username', flat=True)

    if sort == 'likes':
        comments = comments.annotate(like_count=Count('likes')).order_by('-like_count')
    elif sort == 'latest':
        comments = comments.order_by('-create_at')
    else:
        comments = comments.annotate(dislike_count=Count('dislikes')).order_by('-dislike_count')

    return render(request, 'main/CommentPage.html', {
        'user': request.user,
        'profile': request.user.profile,
        'writers': writers,
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

        return redirect('main:comment_page', lookcard_id=lookcard_id)
    else:
        return redirect('accounts:login')

def edit(request, id):
    pushpagestack(request, request.path)

    edit_comment = get_object_or_404(Comment, pk=id)

    next_url = request.GET.get('next', '/')

    if request.user.is_authenticated and request.user == edit_comment.writer:
        if request.method == "POST":          
            edit_comment.content = request.POST.get('content', '')
            if 'image' in request.FILES:              
                edit_comment.image = request.FILES['image']
            edit_comment.create_at = timezone.now()
            edit_comment.save()
            return redirect(next_url)
        
    return render(request, 'main/CommentEditPage.html', {
        'comment': edit_comment,
        'next_url': next_url
    })

def delete(request, id):
    delete_comment = Comment.objects.get(pk=id)
    delete_comment.delete()
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

def likes(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    next_url = request.GET.get('next', '/')

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)

    return redirect(next_url) if next_url else redirect('main:comment_page', lookcard_id=comment.look_card.id)

def dislikes(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    next_url = request.GET.get('next', '/')

    if request.user in comment.dislikes.all():
        comment.dislikes.remove(request.user)
    else:
        comment.dislikes.add(request.user)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)

    comment.save()
    return redirect(next_url) if next_url else redirect('main:comment_page', lookcard_id=comment.look_card.id)

def lookcard(request, lookcard_id):
    pushpagestack(request, request.get_full_path())
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

def allevents(request):
    pushpagestack(request, request.get_full_path())
    user = request.user
    profile = request.user.profile
    events = Event.objects.all()
    unique_events = []
    event_dict = {}

    for event in events:
        if '_' in event.title:
            topic = event.title.split('_')[1]
        else:   
            topic = event.title
            event.lookcard = LookCard.objects.filter(event=event).first()

        if topic not in event_dict:
            event.topic = topic
            event_dict[topic] = event
            
    unique_events = event_dict.values()

    lookcards = LookCard.objects.filter(event__in=events).order_by('event__title')

    return render(request, 'main/AllEventPage.html', {
        'user': user,
        'profile': profile,
        'unique_events': unique_events,
        'events': events,
        'lookcards': lookcards
    })

def calendar(request):
    pushpagestack(request, request.get_full_path())
    semester = request.GET.get('semester', '1')
    months = []
    events = []
    month_events = []
    
    if semester == '1':
        for i in range(1, 9):
            months.append(i)
    else:
        for i in range(9, 13):
            months.append(i)

    for month in months:
        month_num = Month.objects.get(number=month)
        events = Event.objects.filter(month=month_num)
        if events.exists():
            month_events.append({
                'month': month_num,
                'events': events
            })

    return render(request, 'main/CalendarPage.html', {
        'months': months,
        'events': events,
        'month_events': month_events,
        'active_semester': int(semester)
    })
  
def alllookcards(request, topic):
    pushpagestack(request, request.path)

    if topic == '시험기간':
        events = Event.objects.filter(title__icontains='시험기간')
        lookcards = LookCard.objects.filter(event__in=events, month__number__in=[4, 10]).order_by('event__month__number', 'event__title')
        for lookcard in lookcards:
            lookcard.semester = '1학기' if lookcard.month.number in [4] else '2학기'
    
    else:
        events = Event.objects.filter(title__icontains=topic)
        lookcards = LookCard.objects.filter(event__in=events).order_by('event__month__number', 'event__title')

    return render(request, 'main/AllLookCardPage.html', {
        'topic': topic,
        'lookcards': lookcards,
    })