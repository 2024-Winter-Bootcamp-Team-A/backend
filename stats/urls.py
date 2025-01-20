from django.urls import path
from .views import MostViewedAPIView, MostCommentedAPIView, MostWishedAPIView, MostPopularAPIView


urlpatterns = [
    path('most-viewed', MostViewedAPIView.as_view(), name='most-viewed'),
    path('most-commented', MostCommentedAPIView.as_view(), name='most-commented'),
    path('most-wished', MostWishedAPIView.as_view(), name='most-wished'),
    path('most-popular', MostPopularAPIView.as_view(), name='most-popular'),
]