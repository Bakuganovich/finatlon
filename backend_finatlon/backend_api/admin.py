from django.contrib import admin
from .models import (
    Section, Session, Participant, Expert, GeneralParticipant, Goal
)

admin.site.register(Participant)
admin.site.register(Expert)
admin.site.register(GeneralParticipant)
admin.site.register(Goal)
admin.site.register(Section)
admin.site.register(Session)

# Register your models here.
