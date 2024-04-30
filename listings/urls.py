from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisciplineViewSet, CandidatViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'disciplines', DisciplineViewSet)
router.register(r'candidats', CandidatViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
