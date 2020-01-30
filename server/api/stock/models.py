from django.db import models
from django.utils.translation import gettext as _ 
from django.contrib.auth.admin import User

class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=200,
    )
    reference = models.CharField(
        verbose_name=_("Referência"),
        max_length=30,
        unique=True,
    )
    amount = models.IntegerField(
        verbose_name=_("Quantidade"),
    )
    minimum = models.IntegerField(
        verbose_name=_("Quantidade mínima")
    )
    registration = models.DateTimeField(
        verbose_name=_("Data do cadasto"),
        auto_now=True,
    )
    

class Product(models.Model):
    objects = models.Manager()
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=200,
    )
    bar_code = models.CharField(
        verbose_name=_("Código de barras"),
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Descrição"),
        max_length=500,
        null=True,
        blank=True,
    )
    brand = models.CharField(
        verbose_name=_('Marca'),
        max_length=200,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    registration = models.DateTimeField(
        verbose_name=_("Data do cadasto"),
        auto_now=True,
    )
    amount = models.IntegerField(
        verbose_name=_("Quantidade"),
    )    

class Request(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    registration = models.DateTimeField(
        verbose_name=_('Data da requisição'),
        auto_now=True,
    )
    amount = models.IntegerField(
        verbose_name=_('Quantidade')
    )
    delivered = models.DateTimeField(
        verbose_name=_('Data da entrega'),
        null=True,
        blank=True,
    )