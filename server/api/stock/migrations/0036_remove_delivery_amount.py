# Generated by Django 3.0.6 on 2020-06-09 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0035_auto_20200609_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='amount',
        ),
    ]