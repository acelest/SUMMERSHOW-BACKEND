from django.db import models
from django.utils.text import slugify
import random
from string import ascii_letters

class Discipline(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Disciplines"


class Candidat(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.CharField(unique=True,null=True,blank=True,max_length=255)
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

class Vote(models.Model):
    candidate = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=200, blank=True)
    payment_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Vote for {self.candidate.name}"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Votes"

generate_random_string = lambda taille:"".join([ascii_letters[random.randint(0, len(ascii_letters)-1) ] for i in range(taille)])