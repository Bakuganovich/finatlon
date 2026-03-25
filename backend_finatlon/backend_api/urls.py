from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Expert
from .views import ParticipantViewSet, ExpertViewSet

router = DefaultRouter()
router.register(r'participant', ParticipantViewSet) # /api/participant/
router.register(r'expert', ExpertViewSet) # /api/expert/

urlpatterns = [
    path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),

]