from django.urls import path
from .views import ShortsAPIView, ShortVisitAPIView

urlpatterns = [
    path('', ShortsAPIView.as_view()),
    path('<int:book_id>/visit', ShortVisitAPIView.as_view(), name='short-visit-api'),
]
