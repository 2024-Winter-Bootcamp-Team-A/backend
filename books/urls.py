from django.urls import path
from .views import BooksBulkAPIView, BooksAPIView, BooksGPTAPIView, BookAPIView

urlpatterns = [
    path('', BooksAPIView.as_view()),
    path('gpt', BooksGPTAPIView.as_view()),
    path('bulk', BooksBulkAPIView.as_view(), name='bulk_save'),
    path('<int:book_id>', BookAPIView.as_view()),
]
