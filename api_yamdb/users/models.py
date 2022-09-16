from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


GROUP_SELECTION = [
    'user', 'moderator', 'admin'
]

for group_name in GROUP_SELECTION:
    group = Group.objects.create (name = group_name) # Добавить группу разрешений



class CustomUser(AbstractUser):
    # email наследуется от AbstractUser
 #   group = models.CharField(max_length=20, choices=GROUP_SELECTION)
    password = models.CharField(required=False)
    # email = models.EmailField(unique = True)
    REQUIRED_FIELDS = ['email', 'username']




from django.core.mail import send_mail
from config import settings

def email_user(self, subject, message, from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
    send_mail(subject, message, from_email, [self.email], fail_silently=False, **kwargs)


в сеттингс надо
AUTH_EMAIL_VERIFICATION