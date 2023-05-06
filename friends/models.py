from django.db import models
from rest_framework import serializers


class CustomUser(models.Model):
    """Default User model"""
    username = models.CharField(max_length=32, unique=True, null=False)

    def __str__(self) -> str:
        return self.username
