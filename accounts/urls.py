from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path('', accountpage, name="accountpage"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup1/', Signup1, name="signup1"),
    path('signup2/', Signup2, name="signup2"),
    path('checkid/', check_username, name="check_username"),
]