from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_question(data):
    """
    Задача для отправки уведомления по электронной почте при успешном создании вопроса.
    """
    username = data['username']
    phone = data['phone']
    question = data['question']
    mail_sent_q = send_mail(
        'Вопрос на сайте Lovelev',
        f'Новое сообщение для обратной связи с пользователем {username} по номеру телефона {phone} по вопросу:\n\n{question}',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    return mail_sent_q