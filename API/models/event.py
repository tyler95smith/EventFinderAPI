from django.db import models
from django.contrib.auth.models import User
from .interest import Interest

class Event(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	event_name = models.CharField(max_length=100)
	location = models.CharField(max_length=200)
	event_date = models.DateTimeField()
	description = models.CharField(max_length=512)
	age_min = models.IntegerField(default=0)
	age_max = models.IntegerField(default=0)
	interests = models.CharField(max_length=200, default = '')
	attendees = models.ManyToManyField(User, related_name="attendee_accounts")
	host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_host_account")
	is_hidden = models.BooleanField(default=False)
