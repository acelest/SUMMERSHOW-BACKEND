from django.contrib import admin
from .models import Candidat,Discipline,Vote


models = [Candidat,Discipline,Vote]

for model in models:
    admin.site.register(model)