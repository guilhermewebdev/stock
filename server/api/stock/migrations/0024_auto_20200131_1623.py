# Generated by Django 3.0.2 on 2020-01-31 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0023_auto_20200131_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='amount',
        ),
        migrations.AlterField(
            model_name='consumer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='consumption', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='delivery', to='stock.Request'),
        ),
    ]
