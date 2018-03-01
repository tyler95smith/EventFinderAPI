from django.contrib.auth.models import User
from django.db import models

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
	user = models.OneToOneField(User)
	
	#
	# Personal Account Attributes:
	date_of_birth = models.DateField()
	bio = models.CharField(max_length=500)
	primaryLocation = models.CharField(max_length=200) #todo: Needs to be a Location, not just text
	currentLocation = models.CharField(max_lenght=200) #todo: Needs to be a Location, not just text
	hideLocation = models.BooleanField(default=False)

	  #todo: profilePicture ImageField
          #todo: photos array[images]
	  #todo: interests... I believe that this needs to be implemented from the interests model..
	  #	  as in, an interest will belong to many users. Then from this model a getInterests()
	  #	  function can be implemented.
