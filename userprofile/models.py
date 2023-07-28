from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    businessname = models.CharField(max_length=100, verbose_name='Business Name')

    def __str__(self) -> str:
        return self.businessname

def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# from django.db.models.signals import post_save
# post_save.connect(Profile.post_save, sender=User)