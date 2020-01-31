# Generated by Django 3.0.2 on 2020-01-31 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0013_auto_20200131_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='type',
            field=models.CharField(choices=[('USER', 'Usuário'), ('DENTIST', 'Dentista'), ('CHAMBER', 'Consultório'), ('OTHER', 'Outro')], max_length=100, verbose_name='Tipo de consumidor'),
        ),
    ]
