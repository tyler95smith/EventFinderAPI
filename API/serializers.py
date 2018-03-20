from django.contrib.auth.models import User
from .models.person import Person
from .models.event import Event
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

	password = serializers.CharField(write_only=True)

	def create(self, valid_data):

		user = User.objects.create(
				username=valid_data['username'],
				email=valid_data['email'],
			)
		user.set_password(valid_data['password'])
		user.save()

		return user

	class Meta:
		model = User
		fields = ('id','username','email', 'password')


#--------------------------------------------------------------------
#
#	PersonSerializer
#		Serializes a Person (personal account) model. 
#
#		create method will "pop" the 'user' dict from the valid_data,
#		use it to create a new User, and then will use the new 
#		user and the rest of the valid_data to create a new Person
#		Account. 
#
#---------------------------------------------------------------------
class PersonSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	
	def create(self, valid_data):
		user_data = valid_data.pop('user')
		n_user = User.objects.create(**user_data)
		person = Person.objects.create(user=n_user,**valid_data)
		person.save()

		return person

	class Meta:
		model = Person
		fields = ('id', 'user', 'date_of_birth', 'bio', 'primaryLocation', 'currentLocation', 'hideLocation')

class EventSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Event
		fields = ('id', 'date_created', 'event_name', 'location')