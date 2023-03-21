from django.apps import AppConfig


class AuthCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_custom'

    # import custom signals
    def ready(self):
        import auth_custom.signals.handler
