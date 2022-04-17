# Generated by Django 4.0.1 on 2022-04-17 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FuelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GearType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('model', models.CharField(blank=True, max_length=10)),
                ('color', models.CharField(max_length=20)),
                ('no_of_seats', models.IntegerField()),
                ('description', models.TextField(max_length=5000)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(upload_to='vehicle')),
                ('is_available', models.BooleanField(default=True)),
                ('license_plate', models.CharField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vehicle.area')),
                ('car_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vehicle.cartype')),
                ('compares', models.ManyToManyField(blank=True, default=None, related_name='compare', to=settings.AUTH_USER_MODEL)),
                ('fuel_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vehicle.fueltype')),
                ('gear_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vehicle.geartype')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_booking', models.DateField(blank=True, null=True)),
                ('date_of_return', models.DateField(blank=True, null=True)),
                ('advance_amount', models.IntegerField(blank=True, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('is_bill_paid', models.BooleanField(default=False)),
                ('request_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('D', 'Declined')], default='P', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.vehicle')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]