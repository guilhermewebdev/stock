# Generated by Django 3.0.2 on 2020-01-31 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0019_auto_20200131_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='registration',
            field=models.DateTimeField(auto_now=True, verbose_name='Data do cadasto'),
        ),
        migrations.CreateModel(
            name='Removal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Retiradas')),
                ('registration', models.DateTimeField(auto_now=True, verbose_name='Data do cadasto')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='removals', to='stock.Product')),
            ],
        ),
    ]
