# Place any signal handlers here

from django.contrib.auth.models import User
from API.models.person import Person
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@receiver(pre_save, sender=User)
def set_new_user_active_false(sender, instance, *args, **kwargs):
    if not instance.pk and not instance.is_superuser:
        instance.is_active = False

#
# sends email confirmation token in the event that a Person Account is created
@receiver(post_save, sender=Person)
def send_email_confirmation_token(sender, instance, created, **kwargs):
    if created:
        if not instance.user.is_active and not instance.isBanned:
            g = PasswordResetTokenGenerator()
            t = g.make_token(instance.user)
            Subject = 'Welcome to Event Finder - Account Confirmation Required'
            Message = 'Please click the following link to activate your account: https://api.nthbox.com/api/activateuser/?id=%s&token=%s' % (instance.user.id, t)
            From    = 'welcome@api.nthbox.com'
            To      = [instance.user.email]
            send_mail(Subject, Message, From, To)
