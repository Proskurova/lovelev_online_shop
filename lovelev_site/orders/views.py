from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


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
                # order_created.delay(order.id)
                return render(request, 'orders/created.html',
                              {'order': order})
    else:
        cart_form = OrderCreateForm
    return render(request, 'cart/detail.html', {'cart': cart, 'cart_form': cart_form})
