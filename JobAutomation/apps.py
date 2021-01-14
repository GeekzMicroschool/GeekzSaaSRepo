from django.apps import AppConfig

class JobautomationConfig(AppConfig):
    name = 'JobAutomation'
    def ready(self):
        from scheduler import scheduler
        scheduler.start()



