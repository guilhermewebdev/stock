# Generated by Django 3.0.2 on 2020-01-30 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_remove_category_ideal'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=200, verbose_name='Marca'),
            preserve_default=False,
        ),
    ]
