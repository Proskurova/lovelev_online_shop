from decimal import Decimal
import copy

from django.conf import settings

from cart.forms import CartAddProductForm
from clothes.models import Product
from django.shortcuts import get_object_or_404


class Cart(object):

    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем ПУСТУЮ корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем товары из базы данных.
        """
        keys = self.cart.keys()

        # получаем товары и добавляем их в корзину

        cart = copy.deepcopy(self.cart)
        for key in keys:
            id_product = (key.split(', '))[0]
            product = get_object_or_404(Product, id=id_product)
            cart[key]['product'] = product
            cart[key]['update_quantity_form'] = CartAddProductForm(pk=product.id, initial={'quantity': cart[key]['quantity'], 'update': True})

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, size, quantity=1, update_quantity=False):
        """
        Добавляем товар в корзину или обновляем его количество.
        """
        key = f"{product.id}, {size}"

        if key not in self.cart:
            self.cart[key] = {'quantity': 0,
                              'size': size,
                              'price': str(product.price)}
        if update_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self.save()

    def save(self):
        # сохраняем товар
        self.session.modified = True

    def remove(self, product, size):
        """
        Удаляем товар
        """
        key = f"{str(product.id)}, {size}"

        if key in self.cart:
            del self.cart[key]
            self.save()

    def get_total_price(self):
        # получаем общую стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # очищаем корзину в сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()

