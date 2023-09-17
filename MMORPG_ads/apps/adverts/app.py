from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'apps.adverts.app'

    def ready(self):
        import apps.adverts.signals