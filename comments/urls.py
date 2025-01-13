from django.urls import path
from .views import CommentAPIView, CommentDeleteAPIView

urlpatterns = [
    path('<int:book_id>/comments', CommentAPIView.as_view(), name='comment-api'),
    path('<int:book_id>/comments/<int:comment_id>', CommentDeleteAPIView.as_view(), name='comment-delete-api'),
]