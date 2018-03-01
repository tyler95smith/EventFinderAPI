from django.db import models

class Account(models.Model):
	eventname = models.CharField(max_length=100)
