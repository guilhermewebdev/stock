from django.db import models
from django.utils.translation import gettext as _ 

class Product(models.Model):
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=200,        
    )
    description = models.TextField(
        verbose_name=_("Descrição"),
        max_length=500,
        null=True,
        blank=True,
    )
    reference = models.CharField(
        verbose_name=_("Referência"),
        max_length=30,
        unique=True,
    )
    registration = models.DateTimeField(
        verbose_name=_("Data do cadasto"),
        auto_now=True,
    )
    amount = models.IntegerField(
        verbose_name=_("Quantidade"),
        max_length=100
    )    