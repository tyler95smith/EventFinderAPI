from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # ex: /admin/
    path('manage/', views.ManageIndex, name='index'),
    path('manage/event/', views.ManageEvents, name='event'),
    path('api/test/', views.TestAPIView.as_view(), name='test-api'),
    path('api/userlist/', views.ListUsers.as_view(), name='list-users'),
    path('api/createuser/', views.CreateUser.as_view(), name='create-user'),
    path('api/activateuser/', views.ActivateUser.as_view(), name='activate-user'),
    path('api/getpastevents/', views.GetPastEvents.as_view(), name='get-past-events'),
    path('api/getfutureevents/', views.GetFutureEvents.as_view(), name='get-future-events'),
    path('api/getmyevents/', views.GetMyEvents.as_view(), name='get-my-events'),
	path('api/personslist/', views.ListPersons.as_view(), name='list-persons'),
	path('api/createpersonaccount/', views.CreatePersonAccount.as_view(), name='create-person-account'),
	path('api/updatepersonaccount/', views.UpdatePersonAccount.as_view(), name='update-person-account'),
    path('api/login/', obtain_jwt_token)
]
