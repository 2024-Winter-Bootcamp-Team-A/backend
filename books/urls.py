from django.urls import path
from .views import BooksBulkAPIView, BooksAPIView, BooksGPTAPIView

urlpatterns = [
    path('', BooksAPIView.as_view()),
    path('gpt', BooksGPTAPIView.as_view()),
    path('bulk', BooksBulkAPIView.as_view(), name='bulk_save'),
]
