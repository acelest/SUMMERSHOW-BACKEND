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

class InitiatePaymentAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        amount = request.data.get('amount')
        candidate_id = request.data.get('candidate_id')
        region = request.data.get('region')
        reference = generate_random_string(16)
        callback_url = 'http://localhost:8000/api/verifyPayment'  # Remplacez par votre URL de callback

        headers = {
            "Authorization": "pk_test.xQLVZVGz7ZD8nadSGdcHIB4gB5VLeZld1u3V7WsYZDw10aTuHh2AoFutOr4wOWxuqUT6UJzzLaztNdTnUzHTvpBcYcXHDvlpFekVmGZfogXr2f8u1ZLUlzO4X7zqA",  # Remplacez par votre clé publique NotchPay
            "Content-Type": "application/json"
        }

        # Adjust amount based on region
        vote_price = 1000 if region == "Etranger" else 100
        num_votes = int(amount) // vote_price

        data = {
            "email": email,
            "amount": int(amount),  
            "currency": "XAF",
            "reference": reference,
            "callback_url": callback_url,
            "metadata": {
                "candidate_id": candidate_id,
                "numVotes": num_votes,
                "region": region
            }
        }

        response = requests.post('https://api.notchpay.co/payments/initialize', json=data, headers=headers)
        if response.status_code == 200:
            payment_url = response.json().get('data').get('authorization_url')
            return Response({'payment_url': payment_url})
        return Response(response.json(), status=response.status_code)

class VerifyPaymentAPIView(APIView):
    def get(self, request):
        reference = request.query_params.get('reference')
        status = request.query_params.get('status')

        if status == 'success':
            headers = {
                "Authorization": "pk_test.xQLVZVGz7ZD8nadSGdcHIB4gB5VLeZld1u3V7WsYZDw10aTuHh2AoFutOr4wOWxuqUT6UJzzLaztNdTnUzHTvpBcYcXHDvlpFekVmGZfogXr2f8u1ZLUlzO4X7zqA",  # Remplacez par votre clé publique NotchPay
            }
            response = requests.get(f'https://api.notchpay.co/payments/verify/{reference}', headers=headers)
            if response.status_code == 200 and response.json().get('status') == 'success':
                metadata = response.json
