from django.urls import path
from .views import WishAPIView

urlpatterns = [
    path('<int:book_id>/wishes', WishAPIView.as_view(), name='wish-api'),
    path('wishlist/', WishAPIView.as_view(), name='wishlist-api'),
]