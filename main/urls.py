from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"
urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('likes/<int:comment_id>', views.likes, name="likes"),
    path('dislikes/<int:comment_id>', views.dislikes, name="dislikes"),
    path('lookcard/<int:lookcard_id>/comments/', views.commentpage, name="comment_page"),
    path('lookcard/<int:lookcard_id>/create/', views.create, name="create_comment"),
    path('lookcard/<int:lookcard_id>/', views.lookcard, name="lookcard_detail"),
    path('alllookcards/<str:topic>/', views.alllookcards, name="alllookcards"),
    path('allevents/', views.allevents, name="allevents"),
    path('calendar/', views.calendar, name="calendar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)