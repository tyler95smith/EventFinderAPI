from django.db import models
from API.models import Event

class EventPicture (models.Model):
	event = models.OneToOneField(Event, on_delete=models.CASCADE)
	image = models.FileField(null=True, blank=True)
