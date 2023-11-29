# from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings


# @shared_task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер {order_id}'
    message = f'Уважаемый {order.first_name}!\n\nВы успешно разместили заказ на сайте модной одежды Lovelev. Ваш заказ № {order.id}\n\nСпасибо, что выбираете нас!'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          [order.email, settings.EMAIL_HOST_USER])
    return mail_sent



