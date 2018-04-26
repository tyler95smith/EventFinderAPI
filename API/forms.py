from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class NotificationForm(forms.Form):
	sender = forms.CharField()
	username = forms.CharField()
	reciver = forms.CharField()
	message = forms.CharField(max_length=512)
