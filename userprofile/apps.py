from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userprofile'

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from userprofile.models import user_post_save
        post_save.connect(user_post_save, sender=User)