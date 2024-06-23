from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'sign'

    def ready(self):
        import sign.signals
