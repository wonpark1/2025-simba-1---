from django.urls import path
from .views import *
from . import views

app_name = "main"
urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('comment/', views.comentpage, name="comment_page"),
    path('create/', create, name="create"),
    path('update/<int:id>', update, name="update"),
]