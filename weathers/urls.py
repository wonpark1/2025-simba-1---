from django.urls import path, include
from .views import weather_view

app_name="weathers"

urlpatterns = [
    path('checking/', weather_view, name='checking'),
]