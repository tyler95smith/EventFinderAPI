from django.db import models
from .conversation import Conversation
from .account import Account

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
