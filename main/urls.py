from django.urls import path
from .views import *
from . import views

app_name = "main"
urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('comment/', views.comentpage, name="comment_page"),
    path('create/', create, name="create"),
    path('edit/<int:id>', edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('update/<int:id>', update, name="update"),
]