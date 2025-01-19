from django.urls import path
from .views import ShortsAPIView, ShortVisitAPIView, ShortShareAPIView, ShortDetailAPIView, ShortIndividualAPIView, BestShortsAPIView

urlpatterns = [
    path('', ShortsAPIView.as_view()),
    path('<int:book_id>/visit', ShortVisitAPIView.as_view(), name='short-visit-api'),
    path('<int:book_id>/share', ShortShareAPIView.as_view(), name='short-share-api'),
    path('<int:book_id>/detail', ShortDetailAPIView.as_view(), name ='short-detail-api'),
    path('<int:book_id>/individual', ShortIndividualAPIView.as_view(), name ='short-individual-api'),
    path('best', BestShortsAPIView.as_view(), name='best-shorts-api'),
]
