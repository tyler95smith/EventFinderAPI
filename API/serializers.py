from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models.person import Person
from .models.event import Event
from .models.interests import Interests
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

	password = serializers.CharField(write_only=True)

	def create(self, valid_data):

		user = User.objects.create(
				username=valid_data['username'],
				email=valid_data['email'],
                password=make_password(valid_data['password'])
			)
		#user.set_password(make_password(valid_data['password']))
		user.save()

		return user

	class Meta:
		model = User
		fields = ('id','username','email', 'password')

#--------------------------------------------------------------------
#    Serializer for updating a User's password endpoint. 
#--------------------------------------------------------------------
class UpdatePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)
	id = serializers.IntegerField(required=True)
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
		n_user = User.objects.create_user(**user_data)
		person = Person.objects.create(user=n_user,**valid_data)
		person.save()

		return person

	def update(self, instance, valid_data):
		user_data = valid_data.pop('user') # get user information
		user_inst = getattr(instance, 'user') # get the person's user model and update it
		user_inst.username = user_data.get('username', user_inst.username)
		user_inst.email = user_data.get('email', user_inst.email)
		#instance.user.password = user_data.get('password') # before i created this custom update function password was required?
		user_inst.save() # save user section of data

		instance.date_of_birth = valid_data.get('date_of_birth')
		instance.bio = valid_data.get('bio')
		instance.primaryLocation = valid_data.get('primaryLocation')
		instance.currentLocation = valid_data.get('currentLocation')
		instance.is_hidden = valid_data.get('hideLocation')
		instance.save() # save person section of data

		return instance


	class Meta:
		model = Person
		fields = ('id', 'user', 'date_of_birth', 'bio', 'primaryLocation', 'currentLocation', 'hideLocation')

class EventSerializer(serializers.ModelSerializer):
	attendees = serializers.PrimaryKeyRelatedField(many=True,queryset=User.objects.all())
	interests = serializers.PrimaryKeyRelatedField(many=True, queryset=Interests.objects.all())
	
	def create(self, valid_data):
		interest_ids = valid_data.pop("interests")
		attendee_ids = valid_data.pop("attendees")
		event = Event.objects.create(**valid_data)
		for in_id in interest_ids:
			event.interests.add(in_id)
		for a_id in attendee_ids:
			event.attendees.add(a_id)
		event.save()
		
		return event
		
	class Meta:
		model = Event
		fields = ('id', 'date_created', 'event_name', 'location', 'event_date', 'description', 'age_min', 'age_max', 'interests', 'attendees', 'host', 'is_hidden')
