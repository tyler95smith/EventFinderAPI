from django.contrib.auth.models import User
from .models.person import Person
from .models.event import Event
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):

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



class PersonSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Person
		fields = ('id', 'user', 'date_of_birth', 'bio', 'primaryLocation', 'currentLocation', 'hideLocation')

class EventSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Event
		fields = ('id', 'date_created', 'event_name', 'location', 'event_date', 'description', 'age_min', 'age_max')