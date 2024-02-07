from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import *


def order_create(request):
    cart = Cart(request)
    if cart:
        if request.method == 'POST':
            cart_form = OrderCreateForm(request.POST)
            if cart_form.is_valid():
                order = cart_form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                # очистка корзины
                cart.clear()
                # запуск асинхронной задачи
                order_created.delay(order.id)
                # запуск синхронной задачи
                # order_created(order.id)
                data = {
                    'success': True,
                    'order': order.id
                }
                return JsonResponse(data)
            else:
                data = {
                    'success': False,
                    'errors': cart_form.errors.as_json(),
                }
                return JsonResponse(data)

    else:
        data = {
            'success': False,
            'errors': False,
        }
        return JsonResponse(data)
