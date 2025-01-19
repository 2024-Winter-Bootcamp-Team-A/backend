from django.urls import path
from .views import FAQAPIView, FAQSearchAPIView

urlpatterns = [
    path('', FAQAPIView.as_view(), name='faq-api'), 
    path('search', FAQSearchAPIView.as_view(), name='faq-search'), 
]