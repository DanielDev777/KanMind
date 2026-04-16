"""Custom user model for the kanban application.

Extends Django's AbstractUser to include additional fields like fullname
and uses email as the primary authentication identifier.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with email-based authentication.

    Extends AbstractUser to add a fullname field and make email unique.
    Email is used as the username for authentication.
    """

    fullname = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        """Return the email as the string representation of the user."""
        return self.email
