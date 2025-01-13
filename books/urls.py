from django.urls import path
from .views import BookDetailCreateAPIView

urlpatterns = [
    path('detail/', BookDetailCreateAPIView.as_view(), name='book-detail-create'),  # 책 URL 상세 저장 API
]
