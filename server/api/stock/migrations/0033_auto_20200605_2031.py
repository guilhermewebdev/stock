# Generated by Django 3.0.6 on 2020-06-05 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0032_auto_20200603_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomsuptionrequest',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='stock.Category'),
        ),
    ]
