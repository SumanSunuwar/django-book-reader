from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ReaderProfile

@receiver(post_save, sender=User)
def create_reader_profile(sender, instance, created, **kwargs):
    if created:
        ReaderProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_reader_profile(sender, instance, **kwargs):
    instance.reader_profile.save()