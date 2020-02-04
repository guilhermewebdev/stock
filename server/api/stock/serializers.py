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
            'pk',
            'name',
            'description',
            'brand',
            'bar_code',
            'category',
            'registration',
            'amount',
        ]
        read_only_fields = [
            'pk'
        ]

class CategoryListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(
        many=True,
        required=False,
    )
    reference = serializers.CharField(
        validators=[
            validators.UniqueValidator(
                queryset=models.Category.objects.all(),
                message=_("A referência já está sendo utilizada")
            )
        ],
        label=_("Referência")
    )    

    class Meta:
        model = models.Category
        fields = [
            'pk',
            'name',
            'reference',
            'amount',
            'minimum',
            'registration',
            'products'
        ]
        read_only_fields = [
            'pk',
            'amount',
            'registration',            
        ]

##################################################################
#############               Additions            #################
##################################################################

class AdditionSerializer(serializers.ModelSerializer):
    registration = serializers.DateTimeField(
        read_only=True,
    )

    def create(self, validated_data):
        addition = self.context['request'].user.additions.all().create(**validated_data)
        addition.save()
        return addition

    class Meta:
        model = models.Addition
        fields = [
            'pk',
            'product',
            'user',
            'amount',
            'registration',
        ]
        read_only_fields = [
            'pk',
            'user'
        ]

class MassAdditionSerializer(serializers.Serializer):
    additions = AdditionSerializer(
        many=True
    )

    def create(self, validated_data):
        additions = []
        for add_data in validated_data:
            additions.append(
                models.Addition(**add_data)
            )
        return models.Addition.objects.bulk_create(additions)

class PurchaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Purchase
        fields = [
            'pk',
            'product',
            'user',
            'registration',
            'amount',
            'value',
        ]
        read_only_fields = [
            'pk',
            'registration',
            'user',
        ]

##################################################################
#############               Removals            ##################
################################################################## 

class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Consumer
        fields = [
            'pk',
            'type',
            'user',
            'dentist',
            'chamber',
            'patient',
            'other',
        ]
        read_only_fields = [
            'pk',
            'user',
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
        model = models.ConsumptionRequest
        fields = [
            'pk',
            'product',
            'registration',
            'amount',
            'note',
            'user',
            'consumer',
        ]
        read_only_fields = [
            'pk',
            'user',
        ]