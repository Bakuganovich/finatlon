from rest_framework import serializers
from .models import Participant, Expert

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("__all__")

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ("__all__")