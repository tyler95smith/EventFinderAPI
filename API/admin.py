from django.contrib import admin

from .models import Conversation,Event,Interests,Message,Notification,Person,Report,Rsvp

# Register your models here.

admin.site.register(Conversation)
admin.site.register(Event)
admin.site.register(Interests)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Person)
admin.site.register(Report)
admin.site.register(Rsvp)

