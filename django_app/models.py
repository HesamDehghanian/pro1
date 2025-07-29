from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.role})"
# Create your models here.
