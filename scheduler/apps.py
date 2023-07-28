from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler
backgroundscheduler = BackgroundScheduler()


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):

        from syncdata import fullcatalogue, productsstockfull
        backgroundscheduler.add_job(fullcatalogue, 'interval', days=1, start_date='2023-08-01 00:00:00')
        backgroundscheduler.add_job(productsstockfull, 'interval', minutes=15, start_date='2023-08-01 00:00:00')
        backgroundscheduler.start()