# Generated by Django 4.0.1 on 2022-01-29 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicle', '0002_alter_vehicle_license_plate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_booking', models.DateField(blank=True, null=True)),
                ('date_of_return', models.DateField(blank=True, null=True)),
                ('total_days', models.IntegerField()),
                ('advance_amount', models.IntegerField(blank=True, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('is_bill_paid', models.BooleanField(default=False)),
                ('request_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('D', 'Declined')], default='P', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rented_by', to=settings.AUTH_USER_MODEL)),
                ('respondent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.vehicle')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
