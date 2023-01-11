from django.dispatch import receiver

from django.db.models.signals import post_save
from django.contrib.auth.models import User

from profiles.models import Profile

@receiver(post_save,sender=User)
def create_user(sender,created,instance,**kwargs):
    if created:
        profile = Profile.objects.create(user=instance)