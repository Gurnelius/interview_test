from django.db import models
from django.db.models import ForeignKey, CharField, DateTimeField, DecimalField, IntegerField
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = CharField(null=False, max_length=40)
    address = CharField(null=False, max_length=40)
    created_date = DateTimeField(auto_now_add=True)
    customer = ForeignKey(Customer, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = CharField(null=False, max_length=40)
    store = ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    price = DecimalField(default=0, max_digits=7, decimal_places=1)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    customer = ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    store = ForeignKey(Store, null=True, on_delete=models.SET_NULL)
    receipt_number = IntegerField(null=False)
    tax_amount = DecimalField(default=0, max_digits=7, decimal_places=1)
    total_amount = DecimalField(default=0, max_digits=7, decimal_places=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    
    @property
    def get_cart_items(self):
            order_items = self.orderitem_set.all()
            total = sum([item.quantity for item in order_items])
            return total

    @property
    def get_items(self):
        order_items = self.orderitem_set.all()
        return order_items

class OrderItem(models.Model):
    product = ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = IntegerField(default=0)
    total_amount = DecimalField(default=0, max_digits=7, decimal_places=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.id)
