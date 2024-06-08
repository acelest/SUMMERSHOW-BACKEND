from django.db import models
from django.utils.text import slugify
import random
import string

def generate_random_string(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

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


class Candidat(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(unique=True, null=True, blank=True, max_length=255)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='candidates_photos/')
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate identifier if object is being created
            self.identifier = generate_random_string(32)
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.identifier}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.identifier})"

    class Meta:
        ordering = ['identifier']


class Vote(models.Model):
    candidate = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=200, blank=True)
    payment_confirmed = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Ajouter le champ amount
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)  # Ajouter le champ transaction_reference

    def __str__(self):
        return f"Vote for {self.candidate.name}"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Votes"
