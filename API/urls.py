from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.TestAPIView.as_view(), name='test-api'),
    path('api/userlist/', views.ListUsers.as_view(), name='list-users'),
    path('api/createuser/', views.CreateUser.as_view(), name='create-user'),
    path('api/activateuser/', views.ActivateUser.as_view(), name='activate-user'),
    path('api/getpastevents/', views.GetPastEvents.as_view(), name='get-past-events'),
	path('api/personslist/', views.ListPersons.as_view(), name='list-persons'),
	path('api/createpersonaccount/', views.CreatePersonAccount.as_view(), name='create-person-account')
]
