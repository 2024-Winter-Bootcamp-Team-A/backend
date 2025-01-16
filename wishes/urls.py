from django.urls import path
from .views import WishAPIView, WishesAPIView

urlpatterns = [
    path('<int:book_id>/wishes', WishAPIView.as_view(), name='wish-api'),
    path('wishes', WishesAPIView.as_view(), name='wishes-api'),
]