from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisciplineViewSet, CandidatViewSet, VoteViewSet
from .views import CandidatListAPIView

router = DefaultRouter()
router.register(r'disciplines', DisciplineViewSet)
router.register(r'candidats', CandidatViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/candidat/<str:discipline_slug>/', CandidatListAPIView.as_view(), name='candidats-list'),
]
