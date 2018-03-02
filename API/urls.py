from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'api/test^$', views.TestAPIView.as_view(), name='test-api'),
]
