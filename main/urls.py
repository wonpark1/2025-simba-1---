from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"
urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('comment/', views.commentpage, name="comment_page"),
    path('create/', create, name="create"),
    path('edit/<int:id>', edit, name="edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('likes/<int:comment_id>', likes, name="likes"),
    path('dislikes/<int:comment_id>', dislikes, name="dislikes"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)