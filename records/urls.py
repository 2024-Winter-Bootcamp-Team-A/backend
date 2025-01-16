from django.urls import path
from .views import RecordAPIView, RecordsAPIView

urlpatterns = [
    path('<int:book_id>/records', RecordAPIView.as_view(), name='record-api'),
    path('records', RecordsAPIView.as_view(), name='records-api'),
]