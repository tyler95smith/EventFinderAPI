from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models.person import Person
from .models.event import Event
from .models.interests import Interests
from .models.rsvp import Rsvp
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
		fields = ('id','username','email', 'password', 'last_name', 'first_name')

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
		user_data = valid_data.pop('user', {}) # get user information
		user_inst = getattr(instance, 'user', {})
		user_inst.first_name = user_data.get('first_name')
		user_inst.save()
		#instance.date_of_birth = valid_data.get('date_of_birth')
		instance.bio = valid_data.get('bio')
		#instance.primaryLocation = valid_data.get('primaryLocation')
		#instance.currentLocation = valid_data.get('currentLocation')
		#instance.is_hidden = valid_data.get('hideLocation')
		instance.save()
		return instance


	class Meta:
		model = Person
		fields = ('id', 'user', 'date_of_birth', 'bio', 'primaryLocation', 'currentLocation', 'hideLocation', 'isBanned')

class EventSerializer(serializers.ModelSerializer):
	attendees = serializers.PrimaryKeyRelatedField(many=True,queryset=User.objects.all())
	interests = serializers.PrimaryKeyRelatedField(many=True, queryset=Interests.objects.all())
	
	host_info = serializers.SerializerMethodField('get_host_p_info')
	attendees_info = serializers.SerializerMethodField('get_attendees_p_info')
	
	def get_host_p_info(self, obj):
		event = obj
		p = Person.objects.get(user = event.host)
		serializer = PersonSerializer(p)
		return serializer.data

	def get_attendees_p_info(self, obj):
		infoArr = []
		for attendee in obj.attendees.all():
			a = Person.objects.get(user=attendee)
			infoArr.append(a)
		serializer = PersonSerializer(infoArr, many=True)
		return serializer.data

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

	def update(self, instance, valid_data):
		instance.event_name = valid_data.get('event_name')
		instance.location = valid_data.get('location')
		instance.event_date = valid_data.get('event_date')
		instance.description = valid_data.get('description')
		instance.age_min = valid_data.get('age_min')
		instance.age_max = valid_data.get('age_max')
		instance.save()

		return instance

	class Meta:
		model = Event
		fields = ('id', 'date_created', 'event_name', 'location', 'event_date', 'description', 'age_min', 'age_max', 'interests', 'attendees', 'host', 'is_hidden', 'host_info', 'attendees_info')

class RsvpSerializer(serializers.ModelSerializer):
	def create(self, valid_data):
		rsvp = Rsvp.objects.create(**valid_data)
		rsvp.save()

		return rsvp

	class Meta:
		model = Rsvp
		fields = '__all__'
