# Generated by Django 3.0.2 on 2020-01-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20200130_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ideal',
            field=models.IntegerField(verbose_name='Quantidade ideal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='minimum',
            field=models.IntegerField(verbose_name='Quantidade mínima'),
            preserve_default=False,
        ),
    ]
