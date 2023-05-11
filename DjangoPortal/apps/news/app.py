from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'apps.news.app'

    def ready(self):
        import apps.news.signals