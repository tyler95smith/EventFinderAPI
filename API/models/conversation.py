from django.db import models
from django.contrib.auth.models import User
from .event import Event

class Conversation(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	host = models.ForeignKey(User, on_delete=models.CASCADE,related_name="host_account")
	guest = models.ForeignKey(User, on_delete=models.CASCADE,related_name="guest_account")
