from django.db import models
from .event import Event
from .account import Account

class Conversation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    host = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="host_account")
    guest = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="guest_account")
