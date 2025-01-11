from django.apps import AppConfig


class DjangoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app'
    verbose_name = 'Лист задач'

    def ready(self):
        import django_app.signals

