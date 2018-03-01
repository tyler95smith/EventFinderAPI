from django.db import models
from django.contrib.auth.models import User
from .conversation import Conversation

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
