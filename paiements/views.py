from django.http import JsonResponse
from rest_framework.views import APIView
import requests
import json
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
API_PAYMENT_KEY = os.getenv("API_PAYMENT_KEY")


class PaymentInitializationView(APIView):
    def post(self, request):
        # Récupération des données de la requête
        email = request.data.get('email')
        amount = request.data.get('amount')
        phone = request.data.get('phone')
        reference = generate_random_string()  # Générer une référence unique
        description = "Description du paiement"

        # Appel de l'API Notch Pay pour initialiser le paiement
        response, transaction_reference = initialize_payment(email, amount, phone, reference, description)

        # Traitement de la réponse de l'API Notch Pay
        if response.status_code == 201:
            # Paiement initialisé avec succès
            return JsonResponse({
                'status': 'success',
                'message': 'Payment initialized',
                'transaction_reference': transaction_reference,
                'authorization_url': response.json().get('authorization_url')
            })
        else:
            # Échec de l'initialisation du paiement
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to initialize payment'
            }, status=response.status_code)


class PaymentCompletionView(APIView):
    def post(self, request, reference):
        # Récupération des données de la requête
        phone = request.data.get('phone')

        # Finalisation du paiement avec l'API Notch Pay
        response = complete_payment(reference, phone)

        # Traitement de la réponse de l'API Notch Pay
        if response.status_code == 202:
            # Paiement complété avec succès
            return JsonResponse({
                'status': 'success',
                'message': 'Payment completed'
            })
        else:
            # Échec de la finalisation du paiement
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to complete payment'
            }, status=response.status_code)


def initialize_payment(email, amount, phone, reference, description):
    url = 'https://api.notchpay.co/payments/initialize'
    headers = {
        'Authorization': API_PAYMENT_KEY,
        'Accept': 'application/json'
    }
    data = {
        'email': email,
        'currency': 'XAF',  # Choisir la devise appropriée
        'amount': amount,
        'phone': phone,
        'reference': reference,
        'description': description
    }
    response = requests.post(url, headers=headers, data=data)
    transaction_reference = response.json().get('transaction').get('reference')
    return response, transaction_reference


def complete_payment(reference, phone):
    url = f'https://api.notchpay.co/payments/{reference}'
    headers = {
        'Authorization': API_PAYMENT_KEY,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': 'cm.orange',  # Choisir le canal de paiement approprié
        'data': {'phone': phone}
    }
    response = requests.put(url, headers=headers, json=data)
    return response
