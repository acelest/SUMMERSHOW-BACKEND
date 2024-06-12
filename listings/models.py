import requests
from django.db import models
from django.utils.text import slugify
import random
from string import ascii_letters

# Fonction utilitaire pour générer une chaîne aléatoire
def generate_random_string(length):
    return ''.join(random.choice(ascii_letters) for _ in range(length))
def generate_transaction_reference():
    return ''.join(random.choice(ascii_letters) for _ in range(10))

# Modèle Discipline
class Discipline(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='disciplines/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Disciplines"

# Modèle Candidat
class Candidat(models.Model):
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(unique=True, null=True, blank=True, max_length=255)
    name = models.CharField(max_length=200)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='candidates_photos/')
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.identifier = generate_random_string(32)
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.identifier}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.identifier})"

    class Meta:
        ordering = ['identifier']

# Modèle Vote
class Vote(models.Model):
    candidate = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=200, blank=True)
    payment_confirmed = models.BooleanField(default=False)
    # transaction_reference = models.CharField(max_length=255, unique=True)
    transaction_reference = models.CharField(max_length=20, default=generate_transaction_reference)  # Définir une valeur par défaut
    def __str__(self):
        return f"Vote for {self.candidate.name}"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Votes"

    # Méthode pour vérifier et enregistrer un vote à partir de NotchPay
    def verify_and_record_vote(self, notchpay_reference):
        # Endpoint de vérification dans votre backend
        verification_endpoint = "http://127.0.0.1:8000/api/verify-transaction/"

        # Requête POST pour vérifier la transaction avec la référence donnée
        response = requests.post(verification_endpoint, data={"reference": notchpay_reference})

        # Vérification de la réponse du backend
        if response.status_code == 200 and response.json().get('status') == 'success':
            # Si la transaction est confirmée, enregistrez le vote
            self.payment_confirmed = True
            self.save()
            return True
        else:
            # Sinon, la transaction a échoué ou n'est pas valide
            return False
