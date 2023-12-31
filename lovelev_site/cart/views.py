from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from clothes.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartUpdateProductForm
from orders.forms import OrderCreateForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(product.id, request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 size=cd['sizes'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id, size):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, size)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_form = OrderCreateForm
    return render(request, 'cart/detail.html', {'cart': cart, 'cart_form': cart_form, 'title': 'Корзина покупок'})


def cart_update(request, product_id, size):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartUpdateProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 size=size,
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')
