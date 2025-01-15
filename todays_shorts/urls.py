from django.urls import path
from .views import TodaysShortsAPIView, CreateTodaysShortSAPIView, SavedSentenceCardsAPIView

urlpatterns = [
    path('', TodaysShortsAPIView.as_view(), name='todays-shorts-api'), # 오늘의 숏츠 조회 API
    path('<int:book_id>/', CreateTodaysShortSAPIView.as_view(), name='todays-shorts-create-api'), # 오늘의 숏츠 저장 API
    path('saved-cards/', SavedSentenceCardsAPIView.as_view(), name='saved-sentence-cards-api'),
]
