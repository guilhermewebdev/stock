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
    
    def get_default_amount(self):
        products = list(self.products.all())
        amount = 0
        for product in products:
            amount += product.amount
        return amount

    def set_amount(self, value):
        self.amount = value

    def save(self, *args, **kwargs):
        self.set_amount(self.get_default_amount())
        return super(Category, self).save(*args, **kwargs)

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

class Consumer(models.Model):
    TYPES = (
        ('USER', _('Usuário')),
        ('DENTIST', _('Dentista')),
        ('CHAMBER', _('Consultório')),
        ('OTHER', _('Outro')),
        ('PATIENT', _('Paciente')),
    )
    type = models.CharField(
        verbose_name=_('Tipo de consumidor'),
        max_length=100,
        choices=TYPES
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='consumption'
    )
    dentist = models.CharField(
        verbose_name=_('Dentista'),
        max_length=100,
    )
    chamber = models.CharField(
        verbose_name=_('Consultório'),
        max_length=100,
    )
    patient = models.CharField(
        verbose_name=_('Paciente'),
        max_length=100,
    )
    other = models.CharField(
        verbose_name=_('Outro'),
        max_length=100,
    )

class Request(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name='requests'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
    )
    consumer = models.ForeignKey(
        Consumer,
        on_delete=models.DO_NOTHING,
        related_name='requests'
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