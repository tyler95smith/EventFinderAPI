from django.db import models

class Interests(models.Model):
	name = models.CharField(max_length=100)
	haveIt = models.BooleanField(false)
