# Generated by Django 3.0.2 on 2020-01-31 19:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0026_auto_20200131_1851'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='ConsumptionRequest',
        ),
    ]