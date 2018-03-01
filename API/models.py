from django.db import models

# Create your models here.
class Account(models.Model):
	eventname = models.CharField(max_length=100)

class Event(models.Model):
	eventname = models.CharField(max_length=100)

class Conversation(models.Model):
    event = models.ForeignKey(Event,   on_delete=models.CASCADE)
    host  = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="host_account")
    guest = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="guest_account")

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
