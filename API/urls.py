from django.urls import path
from django.conf.urls import include
from . import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    # ex: /admin/
    path('manage/', views.ManageIndex, name='index'),
    path('manage/event/', views.ManageEvents, name='event'),
    path('api/', get_swagger_view(title="EventFinder API")),
    path('api/test/', views.TestAPIView.as_view(), name='test-api'),
    path('api/userlist/', views.ListUsers.as_view(), name='list-users'),
    path('api/validateemail/', views.ValidateEmail.as_view(), name='validate-emal'),
    path('api/validateusername/', views.ValidateUsername.as_view(), name='valitate-username'),
    path('api/createuser/', views.CreateUser.as_view(), name='create-user'),
    path('api/activateuser/', views.ActivateUser.as_view(), name='activate-user'),
    path('api/getpastevents/', views.GetPastEvents.as_view(), name='get-past-events'),
    path('api/getfutureevents/', views.GetFutureEvents.as_view(), name='get-future-events'),
    path('api/getmyevents/', views.GetMyEvents.as_view(), name='get-my-events'),
    path('api/personslist/', views.ListPersons.as_view(), name='list-persons'),
    path('api/createpersonaccount/', views.CreatePersonAccount.as_view(), name='create-person-account'),
    path('api/updatepersonaccount/', views.UpdatePersonAccount.as_view(), name='update-person-account'),
    path('api/updatepassword/', views.UpdatePassword.as_view(), name='update-password'),
    path('api/login/', obtain_jwt_token),
    path('api/weblogin/', include('rest_framework.urls')),
    path('api/getperson/<int:id>/', views.GetPerson.as_view(), name='get-person-by-id')
]
