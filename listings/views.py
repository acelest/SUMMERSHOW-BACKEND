from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Discipline, Candidat, Vote
from .serializers import DisciplineSerializer, CandidatWithDisciplineSerializer, CandidatWithoutDisciplineSerializer, VoteSerializer
import requests

import random
import string

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
# Assurez-vous d'avoir correctement importé generate_random_string
# from .utils import generate_random_string

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

class InitiatePaymentAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        amount = request.data.get('amount')
        candidate_id = request.data.get('candidate_id')
        reference = generate_random_string(16)
        callback_url = 'http://localhost:3000/api/votes/verrify-payment'  # Remplacez par votre URL de callback

        headers = {
            "Authorization": "pk_test.h9RKh3G03eUK0Uan8cWj8Tqrs5uxKRHxgekGOPYgw4OwIXKb40D6Dtjx8X4yghLccGNPpuRQ9TgB5ILhhcO75mrdyLjDJOMvdG3ABTuCJKvLWRl06oCBFeMLWq58g",  # Remplacez par votre clé publique NotchPay
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "amount": int(amount),  # Assurez-vous que amount est un entier
            "currency": "XAF",
            "reference": reference,
            "callback_url": callback_url,
            "metadata": {
                "candidate_id": candidate_id,
                "numVotes": int(amount) // 100  # Convertissez amount en entier avant de diviser
            }
        }

        response = requests.post('https://api.notchpay.co/payments/initialize', json=data, headers=headers)
        if response.status_code == 200:
            payment_url = response.json().get('data').get('authorization_url')
            return Response({'payment_url': payment_url})
        return Response(response.json(), status=response.status_code)

class VerifyPaymentAPIView(APIView):
    def get(self, request):
        trxref = request.query_params.get('trxref')
        reference = request.query_params.get('reference')
        status = request.query_params.get('status')

        if status == 'success':
            headers = {
                "Authorization": "pk_test.h9RKh3G03eUK0Uan8cWj8Tqrs5uxKRHxgekGOPYgw4OwIXKb40D6Dtjx8X4yghLccGNPpuRQ9TgB5ILhhcO75mrdyLjDJOMvdG3ABTuCJKvLWRl06oCBFeMLWq58g",  # Remplacez par votre clé publique NotchPay
            }
            response = requests.get(f'https://api.notchpay.co/payments/verify/{reference}', headers=headers)
            if response.status_code == 200 and response.json().get('status') == 'success':
                metadata = response.json().get('data').get('metadata')
                candidate_id = metadata.get('candidate_id')
                numVotes = metadata.get('numVotes')

                candidate = Candidat.objects.get(pk=candidate_id)
                for _ in range(numVotes):
                    Vote.objects.create(candidate=candidate, payment_confirmed=True, amount=100, transaction_reference=reference)

                return Response({'message': 'Payment verified and votes recorded.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Payment verification failed.'}, status=status.HTTP_400_BAD_REQUEST)

