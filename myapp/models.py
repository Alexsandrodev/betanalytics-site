from django.conf import settings
from accounts.models import User
from django.db import models

class MyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    description = models.CharField(max_length=100)

