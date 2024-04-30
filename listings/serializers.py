# serializers.py
from rest_framework import serializers
from .models import Discipline, Candidat, Vote

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name', 'description', 'slug']

class CandidatSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()  

    class Meta:
        model = Candidat
        fields = ['id', 'name', 'identifier', 'discipline', 'photo', 'slug']

class VoteSerializer(serializers.ModelSerializer):
    candidate = CandidatSerializer()  

    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'user_id', 'payment_confirmed']

   
    def update(self, instance, validated_data):
        instance.payment_confirmed = validated_data.get('payment_confirmed', instance.payment_confirmed)
        instance.save()
        return instance
