"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from stock import views as stock

api = [
    path('sessions/', include('rest_auth.urls')),
    path('sessions/registration/', include('rest_auth.registration.urls')),
    path('products/', stock.ProductList.as_view()),
    path('products/<int:pk>/', stock.ProductDetail.as_view()),
    path('products/<int:product>/additions/', stock.AddictionsList.as_view()),
    path('products/<int:product>/additions/<int:pk>/', stock.AddictionsDetail.as_view()),
    path('categories/', stock.CategoryList.as_view()),
    path('categories/<int:pk>/', stock.CategoryDetail.as_view()),
    path('categories/<int:category>/products/', stock.ProductList.as_view()),
    path('categories/<int:category>/products/<int:pk>/', stock.ProductDetail.as_view()),
    path('requests/consum/', stock.ConsumptionRequestList.as_view()),
    path('requests/consum/<int:pk>/', stock.ConsumptionRequestDetail.as_view()),
    path('purchases/', stock.PurchaseList.as_view()),
    path('purchases/<int:pk>/', stock.PurchaseDetail.as_view()),
    path('removals/', stock.RemovalList.as_view()),
    path('removals/<int:pk>/', stock.RemovalDetail.as_view()),
    path('deliveries/', stock.DeliveryList.as_view()),
    path('deliveries/<int:pk>/', stock.DeliveryDetail.as_view()),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]
