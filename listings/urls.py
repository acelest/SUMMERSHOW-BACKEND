from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CandidatVotesAPIView,
    DisciplineViewSet,
    CandidatViewSet,
    VoteViewSet,
    CandidatListAPIView,
    VerifyTransaction,
    votes_chart_data  # Assurez-vous d'importer la vue
)

router = DefaultRouter()
router.register(r'disciplines', DisciplineViewSet)
router.register(r'candidats', CandidatViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('candidat/<str:discipline_slug>/', CandidatListAPIView.as_view(), name='candidats-list'),
    path('candidats/<int:id>/votes/', CandidatVotesAPIView.as_view(), name='candidat_votes'),
    path('api/verify-transaction/', VerifyTransaction.as_view(), name='verify_transaction'),
    path('top-candidates-votes/', votes_chart_data, name='top_candidates_votes'),  # Utilisez l'URL correcte
]
