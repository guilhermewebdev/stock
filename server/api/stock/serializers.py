from . import models
from rest_framework import serializers, validators
from django.utils.translation import gettext as _

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

    class Meta:
        model = models.Category
        fields = [
            'name',
            'reference',
            'amount',
            'minimum',
            'ideal',
            'registration',
        ]