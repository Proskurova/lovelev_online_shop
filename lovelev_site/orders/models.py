from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from clothes.models import Product


class Order(models.Model):

    DELIVERY_MINSK = 'minsk'
    DELIVERY_RB = 'rb'
    DELIVERY_CDEK = 'cdek'
    PAYMENT_CARD = 'card'
    PAYMENT_CASH = 'cash          '

    DELIVERY_CHOICES = (
        (DELIVERY_MINSK, 'Доставка курьером по Минску'),
        (DELIVERY_RB, 'Доставка Европочтой по РБ'),
        (DELIVERY_CDEK, 'СДЭК, города РФ')
    )

    PAYMENT_METHOD = (
        (PAYMENT_CARD, 'Банковской картой'),
        (PAYMENT_CASH, 'Оплата при получении')
    )

    first_name = models.CharField(max_length=100, verbose_name="ФИО", blank=False)
    phoneNumber = PhoneNumberField(null=False, blank=False, verbose_name="Телефон")
    email = models.EmailField(blank=False)
    city = models.CharField(max_length=100, verbose_name="Город", blank=False,)
    delivery = models.CharField(
        max_length=100,
        verbose_name="Доставка",
        choices=DELIVERY_CHOICES,
        default=DELIVERY_MINSK,
        blank=False,
    )
    address = models.CharField(max_length=300, verbose_name="Адрес", blank=False,)
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paymentMethod = models.CharField(
        max_length=100,
        verbose_name="Способ оплаты",
        choices=PAYMENT_METHOD,
        default=PAYMENT_CARD,
        blank=False,
    )
    paid = models.BooleanField(default=False, verbose_name="Оплаченный")
    executed = models.BooleanField(default=False, verbose_name="Выполненный")

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
