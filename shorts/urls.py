from django.urls import path
from .views import ShortsAPIView, ShortVisitAPIView, ShortShareAPIView, ShortDetailAPIView, ShortIndividualAPIView, ShortIndividualsAPIView, BestShortsAPIView, ShortsFilterAPIView, ShortsSearchAPIView


urlpatterns = [
    path('', ShortsAPIView.as_view()),
    path('<int:book_id>/visit', ShortVisitAPIView.as_view(), name='short-visit-api'),
    path('<int:book_id>/share', ShortShareAPIView.as_view(), name='short-share-api'),
    path('<int:book_id>/detail', ShortDetailAPIView.as_view(), name ='short-detail-api'),
    path('<int:book_id>', ShortIndividualAPIView.as_view(), name ='short-individual-api'),
    path('side', ShortIndividualsAPIView.as_view(), name='short-individuals-api'),
    path('best', BestShortsAPIView.as_view(), name='best-shorts-api'),
    path('shorts',ShortsFilterAPIView.as_view(), name="shorts-filter"),
    path('search', ShortsSearchAPIView.as_view(), name='shorts-search-api'),
]


