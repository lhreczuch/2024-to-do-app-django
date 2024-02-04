from django.apps import AppConfig
from django.conf import settings


class TodoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_app'
