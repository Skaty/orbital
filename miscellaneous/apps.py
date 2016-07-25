from django.apps import AppConfig


class MiscellaneousConfig(AppConfig):
    name = 'miscellaneous'

    def ready(self):
        import miscellaneous.signals