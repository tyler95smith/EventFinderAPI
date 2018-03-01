from django.db import models
from .event import Event

class Notification(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	time_to_send = models.DateTimeField()
	message = models.CharField(max_length=512)
