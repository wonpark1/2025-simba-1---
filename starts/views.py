from django.shortcuts import render, redirect
from django.utils import timezone


# Create your views here.
def start1(request):
    return render(request, 'starts/start1.html')

def start2(request):
    return render(request, 'starts/start2.html')

def start3(request):
    return render(request, 'starts/start3.html')

def start4(request):
    return render(request, 'starts/start4.html')