from django.urls import path
from .views import BookCreateAPIView

urlpatterns = [
    path('', BookCreateAPIView.as_view(), name='book-create'),  # 명세서에 맞게 경로 수정
]
