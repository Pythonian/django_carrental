from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerProfile, VendorProfile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_vendor:
        VendorProfile.objects.get_or_create(user=instance)
    else:
        CustomerProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_vendor:
        instance.vendor_profile.save()
    else:
        CustomerProfile.objects.get_or_create(user=instance)
