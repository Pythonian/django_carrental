from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city


class Vehicle(models.Model):
    SEDAN = 'SE'
    HATCHBACK = 'HB'
    SUV = 'SU'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (HATCHBACK, 'Hatchback'),
        (SUV, 'SUV'),
    ]
    vendor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='vendor')
    name = models.CharField(max_length=60)
    color = models.CharField(max_length=20)
    no_of_seats = models.IntegerField()
    description = models.TextField(max_length=5000)
    car_type = models.CharField(max_length=2, choices=CAR_TYPE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='vehicle')
    is_available = models.BooleanField(default=True)
    license_plate = models.CharField(max_length=20, unique=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.license_plate} : {self.name}"


class Rent(models.Model):
    PENDING = 'P'
    APPROVED = 'A'
    DECLINED = 'D'
    REQUEST_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    ]
    date_of_booking = models.DateField(blank=True, null=True)
    date_of_return = models.DateField(blank=True, null=True)
    total_days = models.IntegerField()
    advance_amount = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_bill_paid = models.BooleanField(default=False)
    request_status = models.CharField(
        max_length=1, choices=REQUEST_STATUS_CHOICES, default=PENDING)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rented_by')
    vendor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vendor_requested',
        blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.customer.name} - {self.vehicle.name}"
