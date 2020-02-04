from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import generics, mixins
from . import models, serializers

class ListView(generics.ListAPIView,
            mixins.ListModelMixin,
            mixins.CreateModelMixin):
    model = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return get_list_or_404(
            self.model,
            **self.kwargs
        )

class DetailView(generics.GenericAPIView,
            mixins.DestroyModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,):
    model = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):        
        return get_object_or_404(
            self.model,
            **self.kwargs
        )       

class ProductList(ListView):
    model = models.Product
    serializer_class = serializers.ProductListSerializer

class ProductDetail(DetailView):
    model = models.Product
    serializer_class = serializers.ProductListSerializer

class CategoryList(ListView):
    model = models.Category
    serializer_class = serializers.CategoryListSerializer

class CategoryDetail(DetailView):
    model = models.Category
    serializer_class = serializers.CategoryListSerializer

class RequestList(ListView):
    model = models.ConsumptionRequest
    serializer_class = serializers.RequestSerializer

class RequestDetail(DetailView):
    model = models.ConsumptionRequest
    serializer_class = serializers.RequestSerializer

class AddictionsList(ListView):
    serializer_class = serializers.AdditionSerializer
    model = models.Addition

class AddictionsDetail(DetailView):
    serializer_class = serializers.AdditionSerializer
    model = models.Addition

class MassAdditionList(ListView):
    serializer_class = serializers.MassAdditionSerializer
    model = models.Addition

class PurchaseList(ListView):
    serializer_class = serializers.PurchaseSerializer
    model = models.Purchase

class PurchaseDetail(DetailView):
    serializer_class = serializers.PurchaseSerializer
    model = models.Purchase
