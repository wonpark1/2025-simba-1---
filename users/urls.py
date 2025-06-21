from django.urls import path
from .views import *

app_name="users"

urlpatterns = [
    path('mypage/', mypage, name="mypage"),
    path('logout/', logout, name="logout"),
    path('mycomment/', mycomment, name="mycomment"),
]