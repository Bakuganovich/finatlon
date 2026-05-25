from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParticipantViewSet, ExpertViewSet, ListenerViewSet


router = DefaultRouter()
router.register(r'participant', ParticipantViewSet) # /api/participant/
router.register(r'expert', ExpertViewSet) # /api/expert/
router.register(r'listener', ListenerViewSet)   # /api/listener/

urlpatterns = [
    path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
    path('drf-auth/', include('rest_framework.urls')),

]


