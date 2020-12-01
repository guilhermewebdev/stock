from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.admin import User
from django.core.exceptions import ValidationError
import asyncio


def validator_amount(value):
    if value < 0:
        raise ValidationError(
            _('Não é possível existir um valor negativo')
        )


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
    minimum = models.IntegerField(
        verbose_name=_("Quantidade mínima")
    )
    registration = models.DateTimeField(
        verbose_name=_("Data do cadasto"),
        auto_now=True,
    )
    description = models.TextField(
        verbose_name=_("Descrição"),
        max_length=500,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def amount(self):
        products = list(self.products.values('amount'))
        amount = 0
        for product in products:
            amount += product['amount']
        return amount


class Product(models.Model):
    objects = models.Manager()
    bar_code = models.CharField(
        verbose_name=_("Código de barras"),
        max_length=100,
        unique=True,
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
        validators=[
            validator_amount
        ]
    )

    def __str__(self):
        return f'{self.category} - {self.brand}: {self.amount}'

##################################################################
#############               Additions            #################
##################################################################


class Addition(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='additions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='additions'
    )
    registration = models.DateTimeField(
        verbose_name=_("Data do cadasto"),
        auto_now=True,
    )
    amount = models.IntegerField(
        verbose_name=_("Quantidade"),
        validators=[validator_amount]
    )

    def __str__(self):
        return '+%s %s' % (self.amount, self.product)

    def __add(self):
        if not 'saved' in dir(self):
            self.product.amount += self.amount
            self.product.save(update_fields=['amount'])
            self.saved = True
            return True
        else:
            return False

    def __remove(self):
        if not 'deleted' in dir(self) and (self.product.amount - self.amount >= 0):
            self.product.amount -= self.amount
            self.product.save(update_fields=['amount'])
            self.deleted = True
            return True
        else:
            return False

    def delete(self, *args, **kwargs):
        self.__remove()
        return super(Addition, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.__add()
        return super(Addition, self).save(*args, **kwargs)


class Purchase(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='purchases'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='purchases'
    )
    registration = models.DateTimeField(
        verbose_name=_("Data do compra"),
        auto_now=True,
    )
    amount = models.IntegerField(
        verbose_name=_("Quantidade"),
        validators=[
            validator_amount
        ]
    )
    value = models.FloatField(
        verbose_name=_('Valor'),
    )

    def __str__(self):
        return '+%s %s | R$%s' % (self.amount, self.product, self.value)

    def add(self):
        addittion = Addition(
            product=self.product,
            user=self.user,
            amount=self.amount,
        )
        return addittion.save()

    def save(self, *args, **kwargs):
        self.add()
        return super(Purchase, self).save(*args, **kwargs)


##################################################################
#############               Removals            ##################
##################################################################

class RemovalManager(models.Manager):

    def delete(self, *args, **kwargs):
        async def update():
            for removal in self.all().iterator():
                removal.delete()
        asyncio.run(update())
        super(RemovalManager, self).delete(*args, **kwargs)


class Removal(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='removals',
    )
    amount = models.IntegerField(
        verbose_name=_('Retiradas'),
        validators=[
            validator_amount
        ]
    )
    registration = models.DateTimeField(
        verbose_name=_("Data do cadasto"),
        auto_now=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='removals',
    )

    def __str__(self):
        return '-%s %s' % (self.amount, self.product)

    def save(self, *args, **kwargs):
        if not self.id:
            if self.amount > self.product.amount:
                raise ValidationError(
                    _('Há apenas %(products)s no estoque, mas a requisição exige %(value)s'),
                    params={
                        'products': self.product.amount,
                        'value': self.amount,
                    }
                )
            self.product.amount -= self.amount
            self.product.save(update_fields=['amount'])
        else:
            old = Removal.objects.get(pk=self.pk)
            diff = self.amount - old.amount
            self.product.amount -= diff
            self.product.save(update_fields=['amount'])
        return super(Removal, self).save(*args, **kwargs)


class ConsumptionRequest(models.Model):
    TYPES = (
        ('user', _('Usuário')),
        ('dentist', _('Dentista')),
        ('chamber', _('Consultório')),
        ('patient', _('Paciente')),
        ('other', _('Outro')),
    )
    objects = models.Manager()
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='requests',
    )
    consumer = models.CharField(
        verbose_name=_('Consumidor'),
        max_length=200,
    )
    consumer_type = models.CharField(
        verbose_name=_('Tipo de consumidor'),
        max_length=100,
        choices=TYPES
    )
    registration = models.DateTimeField(
        verbose_name=_('Data da requisição'),
        auto_now=True,
    )
    note = models.CharField(
        verbose_name=_('Observação'),
        max_length=300,
        null=True,
        blank=True,
    )

    def __str__(self):
        consumer = dict(self.TYPES).get(self.consumer, '')
        return f'{consumer} {self.consumer}'


class ProductComsuptionRequest(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    amount = models.IntegerField(
        verbose_name=_('Quantidade'),
        validators=[
            validator_amount
        ]
    )
    request = models.ForeignKey(
        ConsumptionRequest,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return '%s: %s' % (
            self.product,
            self.amount
        )


#  Resolver a questão das entregas
class Delivery(models.Model):
    objects = models.Manager()
    request = models.ForeignKey(
        ConsumptionRequest,
        on_delete=models.DO_NOTHING,
        related_name='deliveries'
    )
    registration = models.DateTimeField(
        verbose_name=_('Data da entrega'),
        auto_now=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='deliveries',
    )

    @property
    def amount():
        return self.product_deliveries.all().aggregate(
            models.Sum('amount')
        )['amount__sum']

    def __str__(self):
        return '%s: %s %s' % (
            self.request,
            self.amount,
            self.product
        )

    def save(self, *args, **kwargs):
        return super(Delivery, self).save(*args, **kwargs)


class DeliveryProduct(models.Model):
    objects = models.Manager()
    product_request = models.ForeignKey(
        ProductComsuptionRequest,
        on_delete=models.CASCADE,
        related_name='deliveries',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='requests'
    )
    amount = models.IntegerField(
        verbose_name=_('Quantidade'),
        validators=[
            validator_amount
        ]
    )
    removal = models.ForeignKey(
        Removal,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name='product_deliveries'
    )

    def __remove(self):
        self.removal = Removal(
            product=self.product,
            amount=self.amount,
            user=self.delivery.user,
        )
        self.removal.save()

    def __str__(self):
        return '%s: %s' % (
            self.product,
            self.amount
        )

    def __update_removal(self):
        self.removal.product = self.product
        self.removal.amount = self.amount
        self.removal.user = self.delivery.user
        self.removal.save(update_fields=['product', 'amount', 'user'])

    def save(self, *args, **kwargs):
        if not self.id:
            self.__remove()
        else:
            self.__update_removal()
        return super(DeliveryProduct, self).save(*args, **kwargs)
