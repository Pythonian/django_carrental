from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CarType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GearType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FuelType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city


class Vehicle(models.Model):
    vendor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='vehicles')
    name = models.CharField(max_length=60)
    model = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20)
    no_of_seats = models.IntegerField()
    description = models.TextField(max_length=5000)
    car_type = models.ForeignKey(
        CarType, on_delete=models.PROTECT,
        blank=True, null=True)
    gear_type = models.ForeignKey(
        GearType, on_delete=models.PROTECT,
        blank=True, null=True)
    fuel_type = models.ForeignKey(
        FuelType, on_delete=models.PROTECT,
        blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='vehicle')
    is_available = models.BooleanField(default=True)
    license_plate = models.CharField(max_length=20, unique=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    compares = models.ManyToManyField(
        User, related_name='compare', blank=True, default=None)
    # status: if car is available or not (out for rent)
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
        User, on_delete=models.CASCADE, related_name='rents')
    # vendor = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='vendor_requested',
    #     blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.vehicle.name}"

    @property
    def total_days(self):
        date_of_booking = self.date_of_booking
        date_of_return = self.date_of_return
        if date_of_booking > date_of_return:
            return
        dates = (date_of_return - date_of_booking)
        return dates.days

    @property
    def get_cost(self):
        return self.vehicle.price

    @property
    def get_total_cost(self):
        return self.get_cost * self.total_days
