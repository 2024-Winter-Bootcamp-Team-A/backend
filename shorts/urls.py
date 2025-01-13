from django.urls import path
from .views import ShortsAPIView, ShortVisitAPIView, ShortShareAPIView

urlpatterns = [
    path('', ShortsAPIView.as_view()),
    path('<int:book_id>/visit', ShortVisitAPIView.as_view(), name='short-visit-api'),
    path('<int:book_id>/share', ShortShareAPIView.as_view(), name='short-share-api'),
]
