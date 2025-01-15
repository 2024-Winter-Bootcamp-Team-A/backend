from django.urls import path
from .views import RecordAPIView

urlpatterns = [
    path('<int:book_id>/records', RecordAPIView.as_view(), name='record-api'),
    path('records/', RecordAPIView.as_view(), name='record-api'),
]