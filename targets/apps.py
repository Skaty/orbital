from django.apps import AppConfig


class TargetsConfig(AppConfig):
    name = 'targets'

    def ready(self):
        import targets.signals