# Generated by Django 3.0.2 on 2020-01-31 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0017_auto_20200131_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='note',
            field=models.CharField(max_length=300, verbose_name='Obseervação'),
            preserve_default=False,
        ),
    ]
