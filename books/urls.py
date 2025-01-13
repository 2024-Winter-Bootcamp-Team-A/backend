from django.urls import path
from .views import BookSaveAPIView

urlpatterns = [
    path('bulk/', BookSaveAPIView.as_view(), name='bulk_save'),
]
