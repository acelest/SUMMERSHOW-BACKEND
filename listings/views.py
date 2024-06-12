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

# class VerifyTransaction(APIView):
class VerifyTransaction(APIView):
    def post(self, request):
        notchpay_reference = request.data.get('reference')
        candidate_id = request.data.get('candidate_id')
        region = request.data.get('region')
        amount = request.data.get('amount')

        if not notchpay_reference or not candidate_id or not region or not amount:
            return Response({"message": "La référence de transaction, la région, l'ID du candidat ou le montant est manquant"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier la transaction avec Notch Pay
        url = f"https://api.notchpay.co/payments/verify/{notchpay_reference}"
        headers = {
            "Authorization": "Bearer YOUR_SECRET_KEY",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return Response({"message": "Erreur lors de la vérification de la transaction"}, status=status.HTTP_400_BAD_REQUEST)

        transaction_data = response.json()
        if transaction_data['status'] != 'success':
            return Response({"message": "La transaction n'a pas été validée"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculer le nombre de votes en fonction du montant et de la région
        if region == 'cameroon':
            price_per_vote = 100  # Prix par vote pour les résidents du Cameroun
        else:
            price_per_vote = 1000  # Prix par vote pour les étrangers

        num_votes = int(amount) // price_per_vote

        # Enregistrer les votes
        Vote.objects.create(
            candidate_id=candidate_id,
            transaction_reference=notchpay_reference,
            num_votes=num_votes,
            verified=True
        )

        return Response({"message": "La transaction a été confirmée avec succès et les votes ont été enregistrés"}, status=status.HTTP_200_OK)