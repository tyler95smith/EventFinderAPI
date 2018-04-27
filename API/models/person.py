from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .interest import Interest
#TODO: From reading online, it sounds like in addition to these "Profile" models for
#	different account types, we should also create a custom User model so we can
#	define how to distinguish what type of Account can belong to said User. 

#=======================================================
#
#	Model to be used for the account of a user
#	which is and individual person. This will be
#	the default account model. 
#
#=======================================================

class Person(models.Model):

	#
	# The User this Person Account belongs to:
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	#
	# Personal Account Attributes:
	date_of_birth = models.DateField(null=True)
	bio = models.CharField(max_length=500, default="")
	primaryLocation = models.CharField(max_length=200, default='') #todo: Needs to be a Location, not just text
	currentLocation = models.CharField(max_length=200, default='') #todo: Needs to be a Location, not just text
	hideLocation = models.BooleanField(default=False)
	isFemale = models.BooleanField(default=True)
	isBanned = models.BooleanField(default=False)
	interests = models.CharField(max_length=200, default='')

	  #todo: profilePicture ImageField
		  #todo: photos array[images]
	  #todo: interests... I believe that this needs to be implemented from the interests model..
	  #	  as in, an interest will belong to many users. Then from this model a getInterests()
	  #	  function can be implemented.
