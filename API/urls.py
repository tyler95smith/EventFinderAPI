from django.urls import path
from . import views

urlpatterns = [
    path('api/test/', views.TestAPIView.as_view(), name='test-api'),
]
