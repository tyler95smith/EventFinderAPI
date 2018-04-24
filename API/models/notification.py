from django.db import models
from .event import Event
from django.contrib.auth.models import User

class Notification(models.Model):
	notif_type = models.IntegerField() # 0 = RSVP, 1 = regular message
	#rsvp = models.ForeignKey(RSVP, on_delete=models.CASCADE, null=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	reciver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciver')
	date_created = models.DateTimeField()
	date_sent = models.DateTimeField()
	message = models.CharField(max_length=512)
