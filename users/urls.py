from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView, UserProfileAPIView
urlpatterns = [
    path('signup/', UserCreateAPIView.as_view(), name='user-signup'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile')
]