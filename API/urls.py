from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.TestAPIView.as_view(), name='test-api'),
    path('api/userlist/', views.ListUsers.as_view(), name='list-users'),
    path('api/testcreateuser/', views.TestCreateUser.as_view(), name='test-create-user'),
    path('api/createuser/', views.CreateUser.as_view(), name='create-user'),
    path('api/activateuser/', views.ActivateUser.as_view(), name='activate-user')
]
