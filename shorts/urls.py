from django.urls import path
from .views import ShortsAPIView

urlpatterns = [
    path('', ShortsAPIView.as_view()),
]
