from django.urls import path
from .views import MostViewedAPIView, MostCommentedAPIView, MostWishedAPIView

urlpatterns = [
    path('most-viewed', MostViewedAPIView.as_view(), name='most-viewed'),
    path('most-commented', MostCommentedAPIView.as_view(), name='most-commented'),
    path('most-wished', MostWishedAPIView.as_view(), name='most-wished'),
]