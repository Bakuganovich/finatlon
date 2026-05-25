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


from .models import Listener, Section, Goal

class ListenerSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    preparation_level_display = serializers.CharField(source='get_preparation_level_display', read_only=True)
    format_participation_display = serializers.CharField(source='get_format_participation_display', read_only=True)
    class Meta:
        model = Listener
        fields = '__all__'  # или перечислите явно нужные поля

