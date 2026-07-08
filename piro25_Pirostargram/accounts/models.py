from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=30, blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    bio = models.TextField(blank=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )
