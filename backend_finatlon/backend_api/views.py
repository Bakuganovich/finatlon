from rest_framework import viewsets, permissions
from .models import Participant, Expert
from .serializers import ParticipantSerializer, ExpertSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]

class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [permissions.AllowAny]

from .models import Listener
from .serializers import ListenerSerializer

class ListenerViewSet(viewsets.ModelViewSet):
    queryset = Listener.objects.all()
    serializer_class = ListenerSerializer
    permission_classes = [permissions.AllowAny]   # пока открытый доступ