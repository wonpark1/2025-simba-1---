from django.urls import path
from .views import *

app_name="starts"

urlpatterns = [
    path('', start1, name="start1"),
    path('start2/', start2, name="start2"),
    path('start3/', start3, name="start3"),
    path('start4/', start4, name="start4"),
]