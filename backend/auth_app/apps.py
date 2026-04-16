"""Django app configuration for authentication application."""
from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Configuration for the authentication application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'
