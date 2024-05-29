# views.py
from rest_framework import viewsets
from .models import Discipline, Candidat, Vote
from .serializers import DisciplineSerializer, CandidatSerializer, VoteSerializer
from .serializers import CandidatSerializer
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class NoDeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all methods except DELETE
        if request.method == "DELETE":
            return False
        return True

class DisciplineViewSet(viewsets.ModelViewSet):
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
   
class CandidatVotesAPIView(APIView):
    def get(self, request, id):
        try:
            identifiant = Candidat.objects.get(id=id)
            # candidat = Candidat.objects.get(name=candidat_name)
            votes = Vote.objects.filter(candidate=identifiant)
            serializer = VoteSerializer(votes, many=True)
            return Response(serializer.data)
        except Candidat.DoesNotExist:
            return Response({'message': 'Candidat not found'}, status=status.HTTP_404_NOT_FOUND)

    # en attendant les payements
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        payment_confirmed = request.data.get("payment_confirmed", instance.payment_confirmed)
        instance.payment_confirmed = payment_confirmed
        instance.save()
        return super().update(request, *args, **kwargs)

class PaymentAPIView(APIView):
    def get(self, request):
        # Votre logique pour gérer les paiements
        # Par exemple, récupérer les détails du paiement, traiter le paiement, etc.
        # Cette méthode peut retourner un objet Response contenant les détails du paiement ou un message de succès
        return Response({'message': 'Payment API endpoint'})