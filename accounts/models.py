import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    ROLE_CHOICES = (
        ("student", "Student"),
        ("instructor", "Instructor"),
        ("admin", "Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )