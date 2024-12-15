# backend/authapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(unique=True,max_length=11, blank=True, null=True) 

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username