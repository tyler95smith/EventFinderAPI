from django.contrib.auth.models import User
from models.Person import Person
from rest_framework import serializers

class UserSerializer(serializers.HyperLinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id','username','email')

class PersonSerializer(serializers.HyperLinkedModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Person
		fields = ('id', 'user', 'date_of_birth', 'bio', 'primaryLocation', 'currentLocation', 'hideLocation')
