from django.shortcuts import render
from rest_framework import generics, mixins
from . import models, serializers

class ListView(generics.ListAPIView,
            mixins.ListModelMixin,
            mixins.CreateModelMixin):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DetailView(generics.GenericAPIView,
            mixins.DestroyModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProductList(ListView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer

class ProductDetail(DetailView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer

class CategoryList(ListView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryListSerializer

class CategoryDetail(DetailView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryListSerializer

class RequestList(ListView):
    queryset = models.ConsumptionRequest.objects.all()
    serializer_class = serializers.RequestSerializer

class RequestDetail(DetailView):
    queryset = models.ConsumptionRequest.objects.all()
    serializer_class = serializers.RequestSerializer