from . import models
from rest_framework import serializers, validators
from django.utils.translation import gettext as _
from django.contrib.auth.admin import User

class ProductListSerializer(serializers.ModelSerializer):    
    registration = serializers.DateTimeField(
        read_only=True,
        label=_("Data de registro")
    )
    amount = serializers.IntegerField(
        required=True,
        label=_("Quantidade"),    
    )

    class Meta:
        model = models.Product
        fields = [
            'name',
            'description',
            'brand',
            'bar_code',
            'category',
            'registration',
            'amount',
        ]

class CategoryListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)
    reference = serializers.CharField(
        validators=[
            validators.UniqueValidator(
                queryset=models.Product.objects.all(),
                message=_("A referência já está sendo utilizada")
            )
        ],
        label=_("Referência")
    )
    amount = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = models.Category
        fields = [
            'name',
            'reference',
            'amount',
            'minimum',
            'registration',
            'products'
        ]

class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Consumer
        fields = [
            'type',
            'user',
            'dentist',
            'chamber',
            'other',
        ]

class RequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    consumer = ConsumerSerializer(
        label=_('Consumidor'),
        required=True,
    )
    amount = serializers.IntegerField(
        required=True,
        label=_('Quantidade')
    )

    def create(self, validated_data):
        user = self.context['request'].user
        data = {**validated_data, 'user': user}
        return super(RequestSerializer, self).create(data)
    
    class Meta:
        model = models.Request
        fields = [
            'product',
            'registration',
            'amount',
            'delivered',
            'user',
            'consumer',
        ]