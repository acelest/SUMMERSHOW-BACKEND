from rest_framework import serializers
from .models import Discipline, Candidat, Vote

class DisciplineSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'description', 'slug', 'image_url')

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
        fields = ['id', 'name', 'identifier', 'discipline', 'photo', 'slug']

class CandidatWithoutDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = ['id', 'name', 'identifier', 'photo', 'slug']

# class Vote(models.Model):
#     candidate = models.ForeignKey(Candidat, on_delete=models.CASCADE)
#     user_id = models.CharField(max_length=200, blank=True)
#     payment_confirmed = models.BooleanField(default=False)
#     amount = models.PositiveIntegerField(default=100)  # Montant payé
#     transaction_reference = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"Vote for {self.candidate.name}"

#     class Meta:
#         ordering = ['-id']
#         verbose_name_plural = "Votes"