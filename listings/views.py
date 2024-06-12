from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Discipline, Candidat, Vote
from .serializers import DisciplineSerializer, CandidatWithDisciplineSerializer, CandidatWithoutDisciplineSerializer, VoteSerializer
import requests
import random
import string

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

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
    serializer_class = CandidatWithDisciplineSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [NoDeletePermission]

class CandidatListAPIView(generics.ListAPIView):
    serializer_class = CandidatWithoutDisciplineSerializer

    def get_queryset(self):
        discipline_slug = self.kwargs['discipline_slug']
        return Candidat.objects.filter(discipline__slug=discipline_slug)

class CandidatVotesAPIView(APIView):
    def get(self, request, id):
        candidat = get_object_or_404(Candidat, id=id)
        votes = Vote.objects.filter(candidate=candidat)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

class VerifyTransaction(APIView):
    def post(self, request):
        # Récupérer la référence de transaction, la région et le montant depuis les données de la demande
        transaction_reference = request.data.get('transaction_reference')
        region = request.data.get('region')
        amount = request.data.get('amount')

        if not transaction_reference or not region or not amount:
            return Response({"message": "La référence de transaction, la région ou le montant est manquant"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier la validité de la transaction (à adapter selon vos besoins)
        try:
            vote = Vote.objects.get(transaction_reference=transaction_reference)
        except Vote.DoesNotExist:
            return Response({"message": "La transaction n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        # Calculer le nombre de votes en fonction du montant et de la région
        if region == 'Cameroon':
            price_per_vote = 100  # Prix par vote pour les résidents du Cameroun
        else:
            price_per_vote = 1000  # Prix par vote pour les étrangers

        num_votes = int(amount) // price_per_vote  # Calcul du nombre de votes

        # Enregistrer les votes
        vote.verify_and_record_vote(num_votes)

        return Response({"message": "La transaction a été confirmée avec succès et les votes ont été enregistrés"}, status=status.HTTP_200_OK)