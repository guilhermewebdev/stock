# Generated by Django 3.0.3 on 2020-02-20 20:29

from django.db import migrations, models
import django.db.models.deletion
import stock.models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0027_auto_20200131_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumptionrequest',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='consumptionrequest',
            name='product',
        ),
        migrations.CreateModel(
            name='ProductComsuptionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[stock.models.validator_amount], verbose_name='Quantidade')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='requests', to='stock.Category')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='stock.ConsumptionRequest')),
            ],
        ),
    ]
