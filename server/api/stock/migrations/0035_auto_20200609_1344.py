# Generated by Django 3.0.6 on 2020-06-09 13:44

from django.db import migrations, models
import django.db.models.deletion
import stock.models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0034_delivery_removal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='product',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='removal',
        ),
        migrations.AlterField(
            model_name='delivery',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='deliveries', to='stock.ConsumptionRequest'),
        ),
        migrations.CreateModel(
            name='DeliveryProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[stock.models.validator_amount], verbose_name='Quantidade')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_deliveries', to='stock.Delivery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='requests', to='stock.Product')),
                ('product_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='stock.ProductComsuptionRequest')),
                ('removal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='stock.Removal')),
            ],
        ),
    ]
