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
            'brand',
            'bar_code',
            'category',
            'registration',
            'amount',
        ]
        read_only_fields = [
            'pk',
            'registration',
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
            'description',
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
        print('\n\n\n\n\n', validated_data, '\n\n\n\n\n\n\n')
        addition = self.context['view'].get_queryset().create(**validated_data, user=self.context['request'].user)
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
            'consumer',
        ]
        read_only_fields = [
            'pk',
            'user',
        ]

class ComsumRequestSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        required=True,
        label=_('Produto')
    )

    class Meta:
        model = models.ProductComsuptionRequest
        fields = [
            'pk',
            'product',
            'amount',
        ]
        read_only_fields = [
            'pk',
        ]
        extra_kwargs = dict(
            amount=dict(
                required=True,
                label=_('Quantidade')
            ),
            product=dict(
                required=True,
                label=_('Produto')
            )
        )

class RequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    products = ComsumRequestSerializer(
        many=True,
        label=_('Produtos'),
        required=True,
    )
    consumer = serializers.PrimaryKeyRelatedField(
        queryset=models.Consumer.objects.none(),
        label=_('Consumidor'),
        required=True,
    )

    def create(self, validated_data):
        user = self.context['request'].user
        products = validated_data.pop('products')
        data = {**validated_data, 'user': user}
        requests = []
        request = self.Meta.model(**data)
        request.save()
        for product in products:
            requests.append(
               models.ProductComsuptionRequest(
                    **product,
                    request=request
               )
            )
        models.ProductComsuptionRequest.objects.bulk_create(requests)
        return request

    class Meta:
        model = models.ConsumptionRequest
        fields = [
            'pk',
            'products',
            'registration',
            'note',
            'user',
            'consumer',
        ]
        read_only_fields = [
            'pk',
            'user',
            'registration',
        ]

class RemovalSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        data = {**validated_data, 'user': user}
        return super(RemovalSerializer, self).create(data)

    class Meta:
        model = models.Removal
        fields = [
            'pk',
            'product',
            'amount',
            'registration',
            'user',
        ]
        read_only_fields = [
            'pk',
            'user',
            'registration',
        ]

class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Delivery
        fields = [
            'pk',
            'request',
            'product',
            'registration',
            'amount',
            'user',
        ]
        read_only_fields = [
            'pk',
            'user',
            'registration',
        ]