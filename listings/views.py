# views.py
from rest_framework import viewsets
from .models import Discipline, Candidat, Vote
from .serializers import DisciplineSerializer, CandidatSerializer, VoteSerializer
from .serializers import CandidatSerializer
from rest_framework import permissions
from rest_framework import generics

class NoDeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all methods except DELETE
        if request.method == "DELETE":
            return False
        return True
class DisciplineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

class CandidatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [NoDeletePermission]
class CandidatListAPIView(generics.ListAPIView):
    serializer_class = CandidatSerializer

    def get_queryset(self):
        discipline_slug = self.kwargs['discipline_slug']
        return Candidat.objects.filter(discipline__slug=discipline_slug)
   


    # en attendant les payements
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        payment_confirmed = request.data.get("payment_confirmed", instance.payment_confirmed)
        instance.payment_confirmed = payment_confirmed
        instance.save()
        return super().update(request, *args, **kwargs)
