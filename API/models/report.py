from django.db import models
from .account import Account
from .event import Event

class Report(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	rep_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="reported_account")
	rep_event = models.ForeignKey(Event, on_delete=models.CASCADE)
	snitch = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="reportee_account")
	rep_message = models.CharField(max_length=512)
