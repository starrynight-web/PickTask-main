from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)