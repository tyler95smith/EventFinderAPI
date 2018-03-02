from django.contrib.auth.models import User
from models.Person import Person
from rest_framework import serializers

class UserSerializer(serializers.HyperLinkedModelSerializer):

	password = serializers.CharField(write_only=True)

	def create(self, valid_data):

		user = User.objects.create(
				username=valid_data['username'],
				email=valid_data['email']
			)
		user.set_password(valid_data['password'])
		user.save()

		return user

	class Meta:
		model = User
		fields = ('id','username','email')



class PersonSerializer(serializers.HyperLinkedModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Person
		fields = ('id', 'user', 'date_of_birth', 'bio', 'primaryLocation', 'currentLocation', 'hideLocation')
