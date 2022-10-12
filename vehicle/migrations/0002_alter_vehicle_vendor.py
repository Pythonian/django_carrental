# Generated by Django 4.1 on 2022-10-12 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vehicles', to=settings.AUTH_USER_MODEL),
        ),
    ]
