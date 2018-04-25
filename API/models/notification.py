from django.db import models
from .event import Event
from .rsvp import Rsvp
from django.contrib.auth.models import User
from datetime import datetime

class Notification(models.Model):
	DEFAULT_ID = 1
	sender = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_ID, related_name='sender')
	reciver = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_ID, related_name='reciver')
	date_created = models.DateTimeField(default=datetime.now, blank=True)
	date_sent = models.DateTimeField(null=True)
	message = models.CharField(max_length=512)
 