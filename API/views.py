from django.shortcuts import render
from rest_framework.views import APIView	# class based views
from rest_framework.decorators import api_view	# function based views
from API.models import Person
from django.contrib.auth.models import User
from .serializers import PersonSerializer
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

#
# To test api
class TestAPIView(APIView):
	def get(self, request, format='json'):
		return Response("It's working! Hello from the API.")

#
# api end point to list all users... 	
class ListUsers(APIView):	
	def get(self, request, format='json'):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

#
# api end point to test creating a user... 
# to create user send data in following json format via post...	
# {"username": "taylor789", "email": "example@ex.com", "password":"iwejfoiwejfdk"}
class TestCreateUser(APIView):
	def post(self, request, format='json'):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
#
# endpoint for creating a new user

class CreateUser(APIView):
    def post(self, request, format='json'):
        pass

class ActivateUser(APIView):
    def get(self, request, format='none'):
        u = User.objects.get(id=request.GET.get('id'))
        if u.person.isBanned:
            return Response("Error: This user has been banned.")
        if u.is_active:
            return Response("Error: This user is already confirmed.")
        else:
            g = PasswordResetTokenGenerator()
            if g.check_token(u, request.GET.get('token')):
                u.is_active = True
                u.last_login = datetime.now() # We need to change something to invalidate the token.
                u.save()
                return Response("Success.  The account for %s is now active!" % (u.username))
            else:
                return Response("Error: This token appears to be old or invalid.")
    
"""
@api_view (['POST'])
def create_auth(request):
	serialized = UserSerializer(data=request.DATA)
	if serialized.is_valid():
		UserSerializer.create(serialized)
		return Response(serialized.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
"""


#
# endpoint for creating an account
"""
@api_view(['GET', 'POST'])
def person_creator(request):

	#Lists the accounts(GET) or creates a new account (POST).

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
