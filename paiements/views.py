# paiements/views.py
from django.http import JsonResponse
from rest_framework.views import APIView
import requests
import os
from dotenv import load_dotenv
from listings.models import Vote

# Chargement des variables d'environnement
load_dotenv()
API_PAYMENT_KEY = os.getenv("API_PAYMENT_KEY")

def generate_random_string():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

class PaymentInitializationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        amount = request.data.get('amount')
        phone = request.data.get('phone')
        reference = generate_random_string()
        description = "Payment for vote"

        # Initialiser le paiement avec Notch Pay
        response, transaction_reference = initialize_payment(email, amount, phone, reference, description)

        if response.status_code == 201:
            return JsonResponse({
                'status': 'success',
                'message': 'Payment initialized',
                'transaction_reference': transaction_reference,
                'authorization_url': response.json().get('authorization_url')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to initialize payment'
            }, status=response.status_code)

def initialize_payment(email, amount, phone, reference, description):
    url = 'https://api.notchpay.co/payments/initialize'
    headers = {
        'Authorization': f'Bearer {API_PAYMENT_KEY}',
        'Accept': 'application/json'
    }
    data = {
        'email': email,
        'currency': 'XAF',
        'amount': amount,
        'phone': phone,
        'reference': reference,
        'description': description
    }
    response = requests.post(url, headers=headers, json=data)
    transaction_reference = response.json().get('transaction').get('reference')
    return response, transaction_reference


# paiements/views.py (suite)
class PaymentCompletionView(APIView):
    def post(self, request):
        reference = request.data.get('reference')
        phone = request.data.get('phone')
        
        # Compléter le paiement avec Notch Pay
        response = complete_payment(reference, phone)

        if response.status_code == 202:
            # Paiement confirmé, mise à jour du modèle Vote
            try:
                vote = Vote.objects.get(user_id=reference)
                vote.payment_confirmed = True
                vote.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment completed'
                })
            except Vote.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Vote not found'
                }, status=404)
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to complete payment'
            }, status=response.status_code)

def complete_payment(reference, phone):
    url = f'https://api.notchpay.co/payments/{reference}'
    headers = {
        'Authorization': f'Bearer {API_PAYMENT_KEY}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': 'cm.orange',
        'data': {'phone': phone}
    }
    response = requests.put(url, headers=headers, json=data)
    return response
