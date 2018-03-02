from django.shortcuts import render
from rest_framework.views import APIView	# class based views
from rest_framework.decorators import api_view	# function based views
from API.models.person import Person
from django.contrib.auth import User
from .serializers import PersonSerializer
from API.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

#
# endpoint for creating a new user
@api_view (['POST'])
def create_auth(request):
	serialized = UserSerializer(data=request.DATA)
	if serialized.is_valid():
		UserSerializer.create(serialized)
		return Response(serialized.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)



#
# endpoint for creating an account
"""
@api_view(['GET', 'POST'])
def person_creator(request):
	"""
	Lists the accounts(GET) or creates a new account (POST).
	"""
	if request.method == 'GET':
		persons = Person.objects.all()
		serializer = PersonSerializer(persons, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
