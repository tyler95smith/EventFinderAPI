from django.db import models
from .event import Event
from django.contrib.auth.models import User
from datetime import datetime

class Rsvp(models.Model):
	date_created = models.DateTimeField(default=datetime.now, blank=True)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	requester = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.IntegerField(default=0) # 0 = waiting, 1 = accepted, 2 = declined
