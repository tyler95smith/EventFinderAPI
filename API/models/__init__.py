from .interests import Interests
from .event import Event
from .report import Report
from .conversation import Conversation
from .message import Message
from .notification import Notification
from .person import Person
from .rsvp import Rsvp
from django.contrib.auth.models import User, models
User._meta.get_field('email')._unique = True
