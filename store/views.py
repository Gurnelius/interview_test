from django.shortcuts import render
from . import models
from django.shortcuts import get_object_or_404
import uuid

def home(request):
    return render(request, "store/home.html", {})

def stores(request):
    stores = models.Store.objects.all()

    return render(request, "store/stores.html", {"stores":stores})


def products(request):
    products = models.Product.objects.all()

    return render(request, "store/products.html", {"products": products})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem

def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(customer=request.user.customer, store=product.store, receipt_number=0)
 
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    order_item.quantity += 1
    order_item.total_amount = order_item.get_total
    order_item.save()
    order.total_amount = order.get_cart_total
    order.tax_amount = int(order.get_cart_total / 3)
    order.save()
    
    return redirect('home')


def order(request):
    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items


def display_orders(request):
    orders = Order.objects.all().select_related('customer', 'store').prefetch_related('orderitem_set__product')
    return render(request, 'store/display_orders.html', {'orders': orders})