from django.test import TestCase
from . import models

class CategoryTestCase(TestCase):
    category = None

    def setUp(self):
        self.category = models.Category(
            name='papel higiênico',
            reference='03423',
            minimum=10,            
        )
        self.category.save()

class ProductTestCase(TestCase):

    def setUp(self):
        models.Product.objects.create(
            name='Papel higiênico',
            bar_code='04543',
            description='serve para limpar',
            amount=10,
            category=models.Category(
                name='papel higiênico',
                reference='03423',
                minimum=10,            
            ),
            brand='Coca cola'
        ).save()

    def test_product_amount_sum(self):
        product = models.Product.objects.create(
            name='Papel higiênico',
            bar_code='04543',
            description='serve para limpar',
            amount=10,
            category=models.Category(
                name='papel higiênico',
                reference='03423',
                minimum=10,            
            ),
            brand='Coca cola'
        )
        product.update(
            amount=(self.product.amount + 5)
        )
        product.save()

    def test_product_amoun_remove(self):
        product = models.Product.objects.create(
            name='Papel higiênico',
            bar_code='04543',
            description='serve para limpar',
            amount=10,
            category=models.Category(
                name='papel higiênico',
                reference='03423',
                minimum=10,            
            ),
            brand='Coca cola'
        )
        product.update(
            amount=(self.product.amount - 5)
        )
        product.save()

