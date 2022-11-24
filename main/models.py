from django.db import models
from django.contrib.auth.models import User


class UserMapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mappings")
    file = models.FileField()
