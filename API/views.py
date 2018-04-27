from django.shortcuts import render
from rest_framework.views import APIView	# class based views
from rest_framework.decorators import api_view	# function based views
from API.models import Person
from API.models import ProfilePicture
from API.models import Event
from API.models import Report
from API.models import Rsvp
from API.models import Notification
from API.models import Conversation
from API.models import Message
from django.contrib.auth.models import User
from .serializers import PersonSerializer
from .serializers import PictureSerializer
from .serializers import UserSerializer
from .serializers import EventSerializer
from .serializers import UpdatePasswordSerializer
from .serializers import ReportSerializer
from .serializers import RsvpSerializer
from .serializers import NotificationSerializer
from .serializers import MessageSerializer
from .serializers import ConversationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.decorators import authentication_classes, permission_classes
import datetime # dont remove needed to import this way for the datetime.date.today()

from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
import os
import json
from .forms import NotificationForm
from django.conf import settings

#########################
# Start Manage Views
#########################
def ManageIndex(request):
	event_list = Event.objects.filter(is_hidden=False).annotate(report_count=Count('report',filter=Q(id__in=Report.objects.all()))).filter(report_count__gt=0).order_by('-report_count')[:5]
	user_list = User.objects.filter(person__isBanned=False).annotate(report_count=Count('reported_account', filter=Q(id__in=Report.objects.all()))).filter(report_count__gt=0)[:5]
	context = {'event_list': event_list, 'user_list': user_list}
	return render(request, 'API/manage_home.html', context)

def ManageEvents(request):
	event_list = Event.objects.annotate(report_count=Count('report',filter=Q(id__in=Report.objects.all()))).filter(report_count__gt=0)[:10]
	context={'event_list': event_list}
	return render(request, 'API/manage_events.html', context)

def ManageUsers(request):
	user_list = User.objects.annotate(report_count=Count('reported_account', filter=Q(id__in=Report.objects.all()))).filter(report_count__gt=0)
	context = {'user_list': user_list}
	return render(request, 'API/manage_users.html', context)

def EventDetail(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	report_list = Report.objects.filter(rep_event=event_id)
	context={'event': event, 'report_list': report_list}
	return render(request, 'API/manage_event_detail.html', context)

def UserDetail(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	report_list = Report.objects.filter(rep_account=user_id)
	context={'user': user, 'report_list': report_list}
	return render(request, 'API/manage_user_detail.html', context)

def EventUpdate(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	event.is_hidden = not event.is_hidden
	event.save()
	return HttpResponseRedirect('/manage/events/' + str(event_id))

def UserUpdate(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	user.person.isBanned = not user.person.isBanned
	user.person.save()
	return HttpResponseRedirect('/manage/users/' + str(user_id))

def CreateNotif(request, user_id):
	user = User.objects.get(pk=user_id)
	context = {'user': user}
	return render(request, 'API/manage_message_user.html', context)

def SendNotif(request, user_id):
	if request.method == 'POST':
		form = NotificationForm(request.POST)

		if form.is_valid():
			#proccess here
			sender = User.objects.get(pk=form.cleaned_data['sender'])
			reciver = User.objects.get(pk=form.cleaned_data['reciver'])
			message = form.cleaned_data['message']

			notif = Notification.objects.create(
				sender=sender,
				reciver=reciver,
				message=message)
			notif.save()

			return HttpResponseRedirect('/manage/users/' + str(user_id))
	return HttpResponseRedirect('/manage/users/' + str(user_id) + '/message/')

#class TempResult(APIView):
#	def get(self, request, format='json'):
#		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#		return Response(BASE_DIR)
#########################
# End Manage Views
#########################

@permission_classes([])
class GetRsvpList(APIView):
	# get list of Rsvps
	def get(self, request, format='json'):
		rsvps = Rsvp.objects.all()
		serializer = RsvpSerializer(rsvps, many=True)
		return Response(serializer.data)

class SendReport(APIView):
	def post(self, request, format='json'):
		request.data['snitch'] = request.user.id
		s = ReportSerializer(data=request.data)
		if s.is_valid():
			s.save()
			return Response(s.data, status=status.HTTP_201_CREATED)
		else:
			return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

# EX:
# {
# 	"event": 1,
# 	"requester": 3
# }
@permission_classes([])
class CreateRsvp(APIView):
	# when a RSVP is created
	def post(self, request, format='json'):
		serializer = RsvpSerializer(data=request.data)
		if serializer.is_valid():
			rsvp = serializer.save()
			if rsvp:
				# rsvp's are now going to be the notificication not a seperate notification
				# create a notification for the host accept/decline
				#notif = Notification.objects.create(
				#	rsvp=rsvp,
				#	sender=User.objects.get(pk=rsvp.requester.id),
				#	reciver=User.objects.get(pk=rsvp.event.host.id),
				#	message=rsvp.requester.username + " has requested to join your event: " + rsvp.event.event_name
				#	)
				#notif.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# EX:
# {
# 	"id": 1,
# 	"status": 1
# }
@permission_classes([])
class UpdateRsvp(APIView):
	def patch(self, request, format='json'):
		rsvp_id = request.data.get("id")
		rsvp = Rsvp.objects.get(pk=rsvp_id)
		serializer = RsvpSerializer(rsvp,data=request.data, partial=True)
		if serializer.is_valid():
			rsvp = serializer.save()
			if rsvp:
			# create notification for the requester that details the descision
				return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# To test api
@permission_classes([])
class TestAPIView(APIView):
	def get(self, request, format='json'):
		username = 'stranger' if not request.user.username else request.user.username
		return Response("Hi %s! Welcome to the API!!" % username)

#
# api end point to list all users...
class ListUsers(APIView):
	def get(self, request, format='json'):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

'''
 api end point to create a user (without account)...
 to create user send data in following json format via post...
 {"username": "taylor789", "email": "example@ex.com", "password":"iwejfoiwejfdk"}
'''
@permission_classes([])
class CreateUser(APIView):
	def post(self, request, format='json'):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)

'''
 Note: when calling ActivateUser in the future we will need to check whether 
		the account is a person or business account type. If this were a 
		business account being activated, u.person would not exist as the
		account type for the user would be a business account. For now it's 
		fine since there is only one account type that can belong to a user.
'''
@permission_classes([])
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
				u.last_login = datetime.datetime.now() # We need to change something to invalidate the token.
				u.save()
				return Response("Success.  The account for %s is now active!" % (u.username))
			else:
				return Response("Error: This token appears to be old or invalid.")

'''
	End point for getting Person Account info from Person 'id'
		JSON fields expected:

'''

class GetPerson(APIView):
	def get(self, request, id, format='none'):
		try:
			p = Person.objects.get(pk=id)
			serializer = PersonSerializer(p)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Person.DoesNotExist:
			return Response("Person id does not exist.", status=status.HTTP_400_BAD_REQUEST)

'''
	Update User Password Endpoint
		JSON fields expected:
			"id" (user object id)
			"old_password"
			"new_password"
'''
class UpdatePassword(APIView):
	def put(self, request, format='json'):
		serialized = UpdatePasswordSerializer(data=request.data)
		if serialized.is_valid():
			try:
				user = User.objects.get(id=serialized.data.get("id"))
				if not user.check_password(serialized.data.get("old_password")):
					return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
				user.set_password(serialized.data.get("new_password"))
				user.save()
				return Response("Success.", status=status.HTTP_200_OK)
			except User.DoesNotExist:
				return Response("User id does not exist.", status=status.HTTP_404_NOT_FOUND)
		return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class GetMyInfo(APIView):
	'''
	'''
	def get(self, request, format='json'):
		if request.user:
			try:
				p = Person.objects.get(user=request.user)
				serializer = PersonSerializer(p)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except Person.DoesNotExist:
				return Response("Person does not exist for this account.", status=status.HTTP_404_NOT_FOUND)
		return Response("Token is not set or is not valid.", status=status.HTTP_400_BAD_REQUEST)


'''
 api end point to get past events of a specific user
'''
# TODO: add error handling for when the provided values are not the correct type
class GetPastEvents(APIView):
	def get(self, request, format='json'):
		# if no 'host' value is sent in the request default to zero
		req_user = request.query_params.get('user', 0)
		# if the host value is not the correct type return error
		#if not isinstance(req_user, int):
		#	return Response("Error: The host value must be an integer id")
		events = Event.objects.filter(attendees=req_user, event_date__lt=datetime.date.today(),is_hidden=False)
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)

'''
 api end point to get future events of a specific user
'''
# TODO: add error handling for when the provided values are not the correct type
class GetFutureEvents(APIView):
	def get(self, request, format='json'):
		# if no 'host' value is sent in the request default to zero
		req_user = request.query_params.get('user', 0)
		# if the host value is not the correct type return error
		#if not isinstance(req_user, int):
		#	return Response("Error: The host value must be an integer id")
		events = Event.objects.filter(attendees=req_user, event_date__gte=datetime.date.today(),is_hidden=False)
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)
		
'''
 api end point to get events hosted by a specific user
'''
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

'''
 api end point to get n most recently added events
	make call by /getrecentevents/count/ 
	where count is the number of recent events to return
'''
class GetRecentEvents(APIView):
	def get(self, request, count, format='json'):
		events = Event.objects.order_by('-date_created')[:count]
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)

		
#
# api end point to list all accounts of type 'person'...	
class ListPersons(APIView):	
	def get(self, request, format='json'):
		persons = Person.objects.all()
		serializer = PersonSerializer(persons, many=True)
		return Response(serializer.data)
	
'''	
	CreatePersonAccount(APIView):
		api end point for creating a new user with a personal
		account (person). This API post call will create both
		a new user AND a new person account for that user.
		
		Expects a json representation of person object to be 
		created. The serializer will take care of making sense 
		of the fields if they are valid.
		
		The following format is expected:
		{
		"user": {
			"username": "someusername",
			"email": "example@exmpl.com",
			"password": "notagoodpassword"
		},
		"date_of_birth": "1998-09-04",
		"bio": "Yeah. this is a good bio..",
		"primaryLocation": "San Diego, CA",
		"currentLocation": "Los Angeles, CA",
		"hideLocation": false
		}			
'''
@permission_classes([])
class CreatePersonAccount(APIView):
	def post(self, request, format='json'):
		serializer = PersonSerializer(data=request.data)
		#TODO: Probably handle cases where username/email exists
		if serializer.is_valid():
			person = serializer.save()
			if person:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response("Input was not valid: %s" % serializer.errors)	#TODO: May need to return a status code in the event of invalid input

'''
	UpdatePersonAccount(APIView):
		api end point for updating a user with a personal
		account (person). 
		
		Expects a json representation of person object to be 
		created. The serializer will take care of making sense 
		of the fields if they are valid.
		
		The following format is expected:
		{
		 "id": "3",
		"user": {
			"name": "John",
			"username": "someusername",
			"email": "example@exmpl.com"
		},
		"date_of_birth": "1998-09-04",
		"bio": "Yeah. this is a good bio..",
		"primaryLocation": "San Diego, CA",
		"currentLocation": "Los Angeles, CA",
		"hideLocation": false
		}


'''		
class UpdatePersonAccount(APIView):
	def patch(self, request, format='json'):
		p = Person.objects.get(user=request.user)
		serializer = PersonSerializer(p, data=request.data)

		if serializer.is_valid():
			p = serializer.save()
			if p:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors)
		#return Response(p_instance.user.first_name)

class setEventPicture(APIView):
	parser_classes = (MultiPartParser, FormParser)
	def post(self, request, format='json'):
		mutable = request.POST._mutable
		request.POST._mutable = True
		request.POST._mutable = mutable
		try:
			q = EventPicture.objects.get(user=request.user.id)
			os.remove(os.path.join(settings.BASE_DIR, 'media', q.image.name))
		except:
			pass
		try:
			q = EventPicture.objects.get(user=request.user.id)
			q.delete()
		except:
			pass
		s = EventPictureSerializer(data=request.data)
		if s.is_valid():
			s.save()
			return Response(s.data, status=status.HTTP_201_CREATED)
		else:
			return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)	

class SetProfilePicture(APIView):
	parser_classes = (MultiPartParser, FormParser)
	def post(self, request, format='json'):
		mutable = request.POST._mutable
		request.POST._mutable = True
		request.data["user"] = request.user.id
		request.POST._mutable = mutable
		try:
			q = ProfilePicture.objects.get(user=request.user.id)
			os.remove(os.path.join(settings.BASE_DIR, 'media', q.image.name))
		except:
			pass
		try:	
			q = ProfilePicture.objects.get(user=request.user.id)
			q.delete()
		except:
			pass
		s = PictureSerializer(data=request.data)
		if s.is_valid():
			s.save()
			return Response(s.data, status=status.HTTP_201_CREATED)
		else:
			return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateEvent(APIView):
	def patch(self, request, format='json'):
		Event.objects.filter(pk=request.data.get('id')).update(event_name=request.data.get('event_name'))
		Event.objects.filter(pk=request.data.get('id')).update(event_date=request.data.get('event_date'))
		Event.objects.filter(pk=request.data.get('id')).update(location=request.data.get('location'))
		Event.objects.filter(pk=request.data.get('id')).update(description=request.data.get('description'))
		return Response(request.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors)

class CreateEvent(APIView):
	def post(self, request, format='json'):
		request.data['host']=request.user.id
		request.data['attendees']=[request.user.id]
		serializer = EventSerializer(data=request.data)
		if serializer.is_valid():
			event = serializer.save()
			if event:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class GetNotifications(APIView):
	def get(self, request, format='json'):
		notifs = Notification.objects.filter(receiver=request.user)
		rsvps  = Rsvp.objects.filter(event__host=request.user)
		notif_serializer = NotificationSerializer(notifs, many=True)
		rsvp_serializer = RsvpSerializer(rsvps, many=True)
		request = {"notifications": [], "rsvps": []}
		request["notifications"] = notif_serializer.data
		request["rsvps"] = rsvp_serializer.data
		return Response(request, status=status.HTTP_200_OK)

'''
	CreateConversation
		Expected JSON fields:
		"event": id of event
		"guest": USER id of guest
'''				
class CreateConversation(APIView):
	def post(self, request, format='json'):
		event_id = request.data.get('event')
		guest_id = request.data.get('guest')
		
		#make sure conversation doesn't already exist
		if Conversation.objects.filter(event__id=event_id, guest__id=guest_id).exists():
			conversation = Conversation.objects.filter(event=event_id, guest=guest_id)[:1].get()
			serializer = ConversationSerializer(conversation)
			return Response(serializer.data, status=status.HTTP_200_OK)
		
		#check event exists
		try:
			event = Event.objects.get(pk=event_id)
		except Event.DoesNotExist:
			return Response("Event does not exist.", status=status.HTTP_404_NOT_FOUND)
		
		#check host and guest are different users
		if event.host.id == guest_id:
			return Response("host and guest cannot be the same", status=status.HTTP_409_CONFLICT)
		
		#create new conversation
		request.data["host"] = event.host.id
		serializer = ConversationSerializer(data=request.data)
		if serializer.is_valid():
			conversation = serializer.save()
			if conversation:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

'''
	CreateChatMessage
		Expected JSON fields:
		"conversation": id of conversation
		"message": string message
'''		
class CreateChatMessage(APIView):
	def post(self, request, format='json'):
		request.data["sender"] = request.user.id
		request.data["date_sent"] = datetime.datetime.now()
		serializer = MessageSerializer(data=request.data)
		if serializer.is_valid():
			message = serializer.save()
			if message:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
		

