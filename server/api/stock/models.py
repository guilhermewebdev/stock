from django.db import models
from django.utils.translation import gettext as _ 
from django.contrib.auth.admin import User
from django.core.exceptions import ValidationError

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

    def __str__(self):
        return self.name
    
    def amount(self):
        products = list(self.products.values('amount'))
        amount = 0
        for product in products:
            amount += product.amount
        return amount

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
        validators=[
            validator_amount
        ]
    )

    def __str__(self):
        return '%s: %s' % (self.name, self.amount)

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

    def add(self):
        if not 'saved' in dir(self):
            self.product.amount += self.amount
            self.product.save(update_fields=['amount'])
            self.saved = True
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if(self.add()):
            return super(Addition, self).save(*args, **kwargs)
        else:
            return False

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
        return super(Removal, self).save(*args, **kwargs)

class Consumer(models.Model):
    TYPES = (
        ('user', _('Usuário')),
        ('dentist', _('Dentista')),
        ('chamber', _('Consultório')),
        ('patient', _('Paciente')),
        ('other', _('Outro')),
    )
    type = models.CharField(
        verbose_name=_('Tipo de consumidor'),
        max_length=100,
        choices=TYPES
    )
    objects = models.Manager()
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
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
    registration = models.DateTimeField(
        verbose_name=_("Data do cadasto"),
        auto_now=True,
    )

    def __str__(self):
        return '%s: %s' % (self.type, dir(self)[self.type])

class ConsumptionRequest(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name='requests'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='requests',
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
        verbose_name=_('Quantidade'),
        validators=[
            validator_amount
        ]
    )
    note = models.CharField(
        verbose_name=_('Observação'),
        max_length=300,
    )

    def __str__(self):
        return '%s: %s %s' % (
            self.consumer,
            self.amount,
            self.product
        )

class Delivery(models.Model):
    objects = models.Manager()
    request = models.OneToOneField(
        ConsumptionRequest,
        on_delete=models.DO_NOTHING,
        related_name='delivery'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='deliveries'
    )
    registration = models.DateTimeField(
        verbose_name=_('Data da entrega'),
        auto_now=True,
    )
    amount = models.IntegerField(
        verbose_name=_('Retiradas'),
        validators=[
            validator_amount
        ]
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='deliveries',        
    )

    def __str__(self):
        return '%s: %s %s' % (
            self.request,
            self.amount,
            self.product
        )

    def remove(self):
        removal = Removal(
            product=self.product,
            amount=self.amount,
            user=self.user,       
        )
        removal.save()

    def save(self, *args, **kwargs):
        self.remove()
        return super(Delivery, self).save(*args, **kwargs)
