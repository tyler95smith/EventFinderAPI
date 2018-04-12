from django.contrib.auth.models import User, models
User._meta.get_field('email')._unique = True
