from django.db import models

# Create your models here.
class Interests(models.Model):
	eventname = models.CharField(max_length=100)	

class Account(models.Model):
	eventname = models.CharField(max_length=100)

class Event(models.Model):
	event_name = models.CharField(max_length=100)
	location = models.CharField(max_length=200)
	description = models.CharField(max_length=512)
	age_min = models.IntegerField(default=0)
	age_max = models.IntegerField(default=0)
	interests = models.ForeignKey(Interests, on_delete=models.CASCADE)
	host = models.ForeignKey(Account, on_delete=models.CASCADE)

class Conversation(models.Model):
    event = models.ForeignKey(Event,   on_delete=models.CASCADE)
    host  = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="host_account")
    guest = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="guest_account")

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
