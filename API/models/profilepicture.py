from django.db import models
from django.contrib.auth.models import User

class ProfilePicture (models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.FileField(null=True, blank=True)
	description = models.CharField(max_length=100, null=True, blank=True)
