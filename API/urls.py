from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

app_name = 'api'
urlpatterns = [
    # ex: /admin/
    path('manage/', views.ManageIndex, name='manage-index'),
    path('manage/events/', views.ManageEvents, name='manage-events'),
    path('manage/events/<int:event_id>/', views.EventDetail, name='event-detail'),
    path('manage/events/<int:event_id>/update/', views.EventUpdate, name='event-update'),
    path('manage/users/', views.ManageUsers, name='manage-users'),
    path('manage/users/<int:user_id>/', views.UserDetail, name='user-detail'),
    path('manage/users/<int:user_id>/update/', views.UserUpdate, name='user-update'),
    path('manage/users/<int:user_id>/message/', views.CreateNotif, name='notif-create'),
    path('manage/users/<int:user_id>/message/send', views.SendNotif, name='notif-send'),
    path('api/', get_swagger_view(title="EventFinder API")),
    path('api/test/', views.TestAPIView.as_view(), name='test-api'),
    path('api/userlist/', views.ListUsers.as_view(), name='list-users'),
    path('api/createuser/', views.CreateUser.as_view(), name='create-user'),
    path('api/getmyinfo/', views.GetMyInfo.as_view(), name='get-my-info'),
    path('api/activateuser/', views.ActivateUser.as_view(), name='activate-user'),
    path('api/getpastevents/', views.GetPastEvents.as_view(), name='get-past-events'),
    path('api/getfutureevents/', views.GetFutureEvents.as_view(), name='get-future-events'),
    path('api/getmyevents/', views.GetMyEvents.as_view(), name='get-my-events'),
    path('api/personslist/', views.ListPersons.as_view(), name='list-persons'),
    path('api/createpersonaccount/', views.CreatePersonAccount.as_view(), name='create-person-account'),
    path('api/updatepersonaccount/', views.UpdatePersonAccount.as_view(), name='update-person-account'),
	path('api/setprofilepicture/', views.SetProfilePicture.as_view(), name='set-profile-picture'),
    path('api/updatepassword/', views.UpdatePassword.as_view(), name='update-password'),
    path('api/updateevent/', views.UpdateEvent.as_view(), name='update-event'),
    path('api/rsvplist/', views.GetRsvpList.as_view(), name='get-rsvps'),
    path('api/creatersvp/', views.CreateRsvp.as_view(), name='create-rsvp'),
    path('api/updatersvp/', views.UpdateRsvp.as_view(), name='update-rsvp'),
	path('api/sendreport/', views.SendReport.as_view(), name='send-report'),
	path('api/token/login/', obtain_jwt_token),
    path('api/token/validate/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
    path('api/weblogin/', include('rest_framework.urls')),
    path('api/getperson/<int:id>/', views.GetPerson.as_view(), name='get-person-by-id'),
    path('api/createevent/', views.CreateEvent.as_view(), name='create-event'),
    path('api/getrecentevents/<int:count>/', views.GetRecentEvents.as_view(), name='getrecentevents'),
	path('api/getnotifications/', views.GetNotifications.as_view(), name='getnotifications'),
	path('api/createconversation/', views.CreateConversation.as_view(), name='create-coversation'),
	path('api/createmessage/', views.CreateChatMessage.as_view(), name='create-chat-message')
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
