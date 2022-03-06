from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Area(models.Model):
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city


class Vehicle(models.Model):
    SEDAN = 'SE'
    HATCHBACK = 'HB'
    SUV = 'SU'
    CAR_TYPE_CHOICES = (
        (SEDAN, 'Sedan'),
        (HATCHBACK, 'Hatchback'),
        (SUV, 'SUV'),)

    AUTOMATIC = 'A'
    MANUAL = 'M'
    GEAR_TYPE_CHOICES = (
        (AUTOMATIC, 'Automatic'),
        (MANUAL, 'Manual'),)

    PETROL = 'P'
    GASOLINE = 'G'
    DIESEL = 'D'
    FUEL_TYPE_CHOICES = (
        (PETROL, 'Petrol'),
        (GASOLINE, 'Gasoline'),
        (DIESEL, 'Diesel'),)

    vendor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='vendor')
    name = models.CharField(max_length=60)
    model = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20)
    no_of_seats = models.IntegerField()
    description = models.TextField(max_length=5000)
    car_type = models.CharField(max_length=2, choices=CAR_TYPE_CHOICES)
    gear_type = models.CharField(max_length=1, choices=GEAR_TYPE_CHOICES)
    fuel_type = models.CharField(max_length=1, choices=FUEL_TYPE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='vehicle')
    is_available = models.BooleanField(default=True)
    license_plate = models.CharField(max_length=20, unique=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    compares = models.ManyToManyField(
        User, related_name='compare', blank=True, default=None)
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
        return f"{self.customer.name} - {self.vehicle.name}"

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
