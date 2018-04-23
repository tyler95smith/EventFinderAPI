from django.urls import path
from django.conf.urls import include
from . import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    # ex: /admin/
    path('manage/', views.ManageIndex, name='manage-index'),
    path('manage/events/', views.ManageEvents, name='manage-events'),
    path('manage/events/<int:event_id>/', views.EventDetail, name='event-detail'),
    path('manage/users/', views.ManageUsers, name='manage-users'),
    path('manage/users/<int:user_id>/', views.UserDetail, name='user-detail'),
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
    path('api/updatepassword/', views.UpdatePassword.as_view(), name='update-password'),
    path('api/updateevent/', views.EditEvent.as_view(), name='update-event'),
	path('api/token/login/', obtain_jwt_token),
    path('api/token/validate/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
    path('api/weblogin/', include('rest_framework.urls')),
    path('api/getperson/<int:id>/', views.GetPerson.as_view(), name='get-person-by-id'),
	path('api/createevent/', views.CreateEvent.as_view(), name='create-event'),
	path('api/getrecentevents/<int:count>/', views.GetRecentEvents.as_view(), name='getrecentevents')
]
