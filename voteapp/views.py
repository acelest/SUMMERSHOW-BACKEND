# voteapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from listings.models import Vote

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
