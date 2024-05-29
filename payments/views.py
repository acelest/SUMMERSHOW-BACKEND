# views.py

import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from listings.models import Vote

def initialize_payment(request):
    url = 'https://api.notchpay.co/payments/initialize'
    headers = {
        'Authorization': settings.API_PAYMENT_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'email': 'customer@email.com',
        'currency': 'XAF',
        'amount': 1000,  # Montant à payer
        'reference': 'your_unique_reference'  # Référence unique
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if response.status_code == 201:
        # Redirection vers l'URL de paiement
        return redirect(response_data['authorization_url'])
    else:
        # Gestion des erreurs
        # Afficher un message d'erreur ou rediriger vers une page d'erreur
        pass




def verify_payment(request, reference):
    url = f'https://api.notchpay.co/payments/{reference}'
    headers = {
        'Authorization': settings.API_PAYMENT_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    return JsonResponse(response_data)

def complete_payment(request, reference):
    url = f'https://api.notchpay.co/payments/{reference}'
    headers = {
        'Authorization': settings.API_PAYMENT_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'channel': 'cm.orange',  # Canal de paiement (par exemple, Orange Money)
        'data': {
            'phone': '+237656019261'  # Numéro de téléphone pour le paiement
        }
    }

    response = requests.put(url, headers=headers, json=data)
    response_data = response.json()

    return JsonResponse(response_data)




@csrf_exempt  # Utilisé pour permettre à la vue de recevoir des demandes POST sans jeton CSRF
def confirm_payment(request):
    if request.method == 'POST':
        # Récupérer les données de confirmation de paiement de la requête POST
        payment_reference = request.POST.get('payment_reference', None)
        # Recherche du vote correspondant à la référence de paiement
        try:
            vote = Vote.objects.get(payment_reference=payment_reference)
            # Marquer le vote comme confirmé
            vote.confirm_payment()
            return JsonResponse({'message': 'Payment confirmed successfully.'})
        except Vote.DoesNotExist:
            return JsonResponse({'error': 'Vote not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
