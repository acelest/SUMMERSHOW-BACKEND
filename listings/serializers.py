from rest_framework import serializers
from .models import Discipline, Candidat, Vote

class DisciplineSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Discipline
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.image_url
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class CandidatWithDisciplineSerializer(serializers.ModelSerializer):
    discipline = DisciplineSerializer()  

    class Meta:
        model = Candidat
        fields = '__all__'

class CandidatWithoutDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = '__all__'

