from django.db import models

# Create your models here.
class Conversation(models.Model):
    event = models.ForeignKey(Event,   on_delete=models.CASCADE)
    host  = models.ForeignKey(Account, on_delete=models.CASCADE)
    guest = models.ForeignKey(Account, on_delete=models.CASCADE)

class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.CharField(512)