from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator


class User(AbstractUser):
    is_vendor = models.BooleanField(default=True)


class VendorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='vendor_profile')
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=600)
    phone_number = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    image = models.ImageField(upload_to='vendor/images')

    def __str__(self):
        return f'{self.user}'


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='customer_profile')
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    government_id = models.FileField(upload_to='identification')
    image = models.ImageField(upload_to='customer/images')
    address = models.CharField(max_length=600)
    dob = models.DateField()
    license = models.ImageField(upload_to='license')
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.username}"
