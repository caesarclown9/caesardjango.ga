from django.db import models

from products.models import Product
from users.models import User





class Order(models.Model):
    first_name = models.CharField(max_length=50, )
    last_name = models.CharField(max_length=50, )
    address = models.CharField(max_length=250, )
    city = models.CharField(max_length=100, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems', default='')


    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.value * self.qty
