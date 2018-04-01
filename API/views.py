from django.shortcuts import render
from rest_framework.views import APIView	# class based views
from rest_framework.decorators import api_view	# function based views
from API.models import Person
from API.models import Event
from django.contrib.auth.models import User
from .serializers import PersonSerializer
from .serializers import UserSerializer
from .serializers import EventSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime
import datetime # dont remove needed to import this way for the datetime.date.today()

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
# api end point to create a user (without account)... 
# to create user send data in following json format via post...	
# {"username": "taylor789", "email": "example@ex.com", "password":"iwejfoiwejfdk"}
class CreateUser(APIView):
	def post(self, request, format='json'):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)

#
# Note: when calling ActivateUser in the future we will need to check whether 
#		the account is a person or business account type. If this were a 
#		business account being activated, u.person would not exist as the
#		account type for the user would be a business account. For now it's 
#		fine since there is only one account type that can belong to a user.
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

#
# api end point to get past events of a specific user
#
# TODO: add error handling for when the provided values are not the correct type
class GetPastEvents(APIView):
	def get(self, request, format='json'):
		# if no 'host' value is sent in the request default to zero
		req_user = request.query_params.get('user', 0)
		# if the host value is not the correct type return error
		#if not isinstance(req_user, int):
		#	return Response("Error: The host value must be an integer id")
		events = Event.objects.filter(attendees=req_user, event_date__lt=datetime.date.today())
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)

#
# api end point to get future events of a specific user
#
# TODO: add error handling for when the provided values are not the correct type
class GetFutureEvents(APIView):
	def get(self, request, format='json'):
		# if no 'host' value is sent in the request default to zero
		req_user = request.query_params.get('user', 0)
		# if the host value is not the correct type return error
		#if not isinstance(req_user, int):
		#	return Response("Error: The host value must be an integer id")
		events = Event.objects.filter(attendees=req_user, event_date__gte=datetime.date.today())
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)
		
#
# api end point to get events hosted by a specific user
#
# TODO: add error handling for when the provided values are not the correct type
class GetMyEvents(APIView):
	def get(self, request, format='json'):
		# if no 'host' value is sent in the request default to zero
		req_user = request.query_params.get('user', 0)
		# if the host value is not the correct type return error
		#if not isinstance(req_user, int):
		#	return Response("Error: The host value must be an integer id")
		events = Event.objects.filter(host=req_user)
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)

#
# api end point to list all accounts of type 'person'... 	
class ListPersons(APIView):	
	def get(self, request, format='json'):
		persons = Person.objects.all()
		serializer = PersonSerializer(persons, many=True)
		return Response(serializer.data)
		
#---------------------------------------------------------------
#
#	CreatePersonAccount(APIView):
#		api end point for creating a new user with a personal
#		account (person). This API post call will create both
#		a new user AND a new person account for that user.
#		
#		Expects a json representation of person object to be 
#		created. The serializer will take care of making sense 
#		of the fields if they are valid.
#		
#		The following format is expected:
#		{
#        "user": {
#            "username": "someusername",
#            "email": "example@exmpl.com",
#            "password": "notagoodpassword"
#        },
#        "date_of_birth": "1998-09-04",
#        "bio": "Yeah. this is a good bio..",
#        "primaryLocation": "San Diego, CA",
#        "currentLocation": "Los Angeles, CA",
#        "hideLocation": false
#    	}
#			
#----------------------------------------------------------------
class CreatePersonAccount(APIView):
	def post(self, request, format='json'):
		serializer = PersonSerializer(data=request.data)
		#TODO: Probably handle cases where username/email exists
		if serializer.is_valid():
			person = serializer.save()
			if person:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response("Input was not valid")	#TODO: May need to return a status code in the event of invalid input

#---------------------------------------------------------------
#
#	UpdatePersonAccount(APIView):
#		api end point for updating a user with a personal
#		account (person). 
#		
#		Expects a json representation of person object to be 
#		created. The serializer will take care of making sense 
#		of the fields if they are valid.
#		
#		The following format is expected:
#		{
#		 "id": "3",
#        "user": {
#            "username": "someusername",
#            "email": "example@exmpl.com",
#            "password": "notagoodpassword"
#        },
#        "date_of_birth": "1998-09-04",
#        "bio": "Yeah. this is a good bio..",
#        "primaryLocation": "San Diego, CA",
#        "currentLocation": "Los Angeles, CA",
#        "hideLocation": false
#    	}
#
#    {"id": "2"}
#			
#----------------------------------------------------------------
class UpdatePersonAccount(APIView):
	def put(self, request, format='json'):
		p_id = request.data.get('id')
		p_instance = Person.objects.get(pk=p_id) #person id not user id

		serializer = PersonSerializer(p_instance,data=request.data)

		if serializer.is_valid():
			person = serializer.save()
			if person:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors)


