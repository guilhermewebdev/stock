# Generated by Django 3.0.2 on 2020-01-30 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Descrição')),
                ('reference', models.CharField(max_length=30, unique=True, verbose_name='Referência')),
                ('registration', models.DateTimeField(auto_now=True, verbose_name='Data do cadasto')),
                ('amount', models.IntegerField(max_length=100, verbose_name='Quantidade')),
            ],
        ),
    ]
