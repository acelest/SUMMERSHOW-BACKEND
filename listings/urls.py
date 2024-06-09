from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidatVotesAPIView, DisciplineViewSet, CandidatViewSet, VoteViewSet, InitiatePaymentAPIView, VerifyPaymentAPIView
from .views import CandidatListAPIView

router = DefaultRouter()
router.register(r'disciplines', DisciplineViewSet)
router.register(r'candidats', CandidatViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('candidat/<str:discipline_slug>/', CandidatListAPIView.as_view(), name='candidats-list'),
    path('candidats/<int:id>/votes/', CandidatVotesAPIView.as_view(), name='candidat_votes'),
    path('initiate-payment/', InitiatePaymentAPIView.as_view(), name='initiate-payment'),
    path('verify-payment/', VerifyPaymentAPIView.as_view(), name='verify-payment'),
]
