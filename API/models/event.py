from django.db import models
from .interests import Interests
from .account import Account

class Event(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	event_name = models.CharField(max_length=100)
	location = models.CharField(max_length=200)
	event_date = models.DateTimeField()
	description = models.CharField(max_length=512)
	age_min = models.IntegerField(default=0)
	age_max = models.IntegerField(default=0)
	interests = models.ForeignKey(Interests, on_delete=models.CASCADE)
	attendees = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="atendee_accounts")
	host = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="event_host_account")
	is_hidden = models.BooleanField(default=False)
