from django.apps import AppConfig


class LockedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locked'
