from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView
urlpatterns = [
    path('signup/', UserCreateAPIView.as_view(), name='user-signup'),
    path('login/', UserLoginAPIView.as_view(), name='user-login')
]